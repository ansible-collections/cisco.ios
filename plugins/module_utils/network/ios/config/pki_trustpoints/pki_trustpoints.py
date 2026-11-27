# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios_pki_trustpoints config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.pki_trustpoints import (
    Pki_trustpointsTemplate,
    der_to_pem,
    fingerprints,
    normalize_fingerprint,
    pem_to_der,
)


AUTHENTICATE = "crypto pki authenticate "
DELETE = "no crypto pki trustpoint "
OPTIONS = (
    "enrollment",
    "revocation_check",
    "hash",
    "fingerprint",
    "subject_name",
    "subject_alt_name",
    "rsakeypair",
)
# these always have a value on IOS, "no hash sha256" is printed back as "hash sha256":
# they are changed when they are in the task and never removed
ALWAYS_SET = ("enrollment", "revocation_check", "hash")


class Pki_trustpoints(ResourceModule):
    """
    The ios_pki_trustpoints config class
    """

    def __init__(self, module):
        super(Pki_trustpoints, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="pki_trustpoints",
            tmplt=Pki_trustpointsTemplate(),
        )
        self.parsers = list(OPTIONS)
        self._certificates = {}

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self._by_name(self.want)
        haved = self._by_name(self.have)

        if self.state == "deleted":
            # only what is named, a trustpoint with a CA certificate only when the task allows it
            named = [name for name in wantd if name in haved]
            refused = [
                n
                for n in named
                if haved[n].get("ca_certificate") and not wantd[n].get("delete_certificates")
            ]
            if refused:
                self._module.fail_json(
                    msg="The trustpoint(s) %s hold a CA certificate, state deleted removes them with the certificate "
                    "only when delete_certificates is true in the task. Nothing was removed."
                    % ", ".join(refused),
                )
            self.commands.extend(DELETE + name for name in named)
            return

        for name, want in wantd.items():
            self._compare(want, haved.get(name, {}))

    @staticmethod
    def _by_name(trustpoints):
        result = {}
        for entry in deepcopy(trustpoints) or []:
            if entry.get("fingerprint"):
                entry["fingerprint"] = normalize_fingerprint(entry["fingerprint"])
            result[entry["name"]] = entry
        return result

    def _compare(self, want, have):
        """Generate the commands of one trustpoint."""
        name = want["name"]
        pem = want.pop("ca_certificate", None)
        have_pem = have.pop("ca_certificate", None)
        wanted = self._wanted(want, have)
        enrollment = wanted.get("enrollment") or {}
        if enrollment.get("pem") is False:
            # no "pem" is the same as pem: false, after the merge so that merged can turn it off
            enrollment.pop("pem")
        if enrollment.get("pem") and enrollment["type"] != "terminal":
            self._module.fail_json(
                msg="enrollment pem of the trustpoint %s is only supported with the type terminal, "
                "IOS XE 17.12 and 17.18 refuse it with a url." % name,
            )

        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=wanted, have=have)
        if len(self.commands) != begin or not have:
            self.commands.insert(begin, self._tmplt.render(wanted, "name", False))

        if pem:
            self._compare_certificate(name, wanted, pem, have_pem)

    def _wanted(self, want, have):
        if self.state == "merged":
            wanted = deepcopy(have)
            for key, value in want.items():
                if key == "enrollment" and (have.get(key) or {}).get("type") != value["type"]:
                    # another method does not keep the options of the previous one, pem for instance
                    wanted[key] = value
                elif isinstance(value, dict):
                    wanted[key] = dict_merge(wanted.get(key) or {}, value)
                else:
                    wanted[key] = value
            return wanted
        wanted = deepcopy(want)
        for key in ALWAYS_SET:
            if key not in wanted and key in have:
                wanted[key] = have[key]
        return wanted

    def _compare_certificate(self, name, wanted, pem, have_pem):
        """The CA certificate is installed when the trustpoint does not hold it."""
        der = pem_to_der(pem)
        if der is None:
            self._module.fail_json(
                msg="ca_certificate of the trustpoint %s is not a PEM certificate "
                "(-----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----)." % name,
            )
        installed = pem_to_der(have_pem) if have_pem else None
        if installed == der:
            return
        if installed is not None:
            self._module.fail_json(
                msg="The trustpoint %s already holds another CA certificate. IOS does not replace it, "
                "remove the trustpoint first with state deleted." % name,
            )
        if (wanted.get("enrollment") or {}).get("type") != "terminal":
            self._module.fail_json(
                msg="ca_certificate of the trustpoint %s needs enrollment type terminal." % name,
            )
        digests = fingerprints(der)
        pin = wanted.get("fingerprint")
        if not pin:
            self._module.fail_json(
                msg="ca_certificate of the trustpoint %s needs a fingerprint, IOS does not authenticate "
                "a CA certificate otherwise. The SHA-1 fingerprint of the certificate is %s."
                % (name, digests["sha1"]),
            )
        if pin not in (digests["sha1"], digests["md5"]):
            self._module.fail_json(
                msg="The fingerprint of the trustpoint %s does not match ca_certificate. "
                "SHA-1: %s, MD5: %s." % (name, digests["sha1"], digests["md5"]),
            )
        self.commands.append(AUTHENTICATE + name)
        self._certificates[name] = pem

    def run_commands(self):
        """Send the configuration, then install the certificates, they are not configuration commands."""
        if not self.commands or self.state not in self.ACTION_STATES:
            return
        if not self._module.check_mode:
            config = [self._with_answer(c) for c in self.commands if not c.startswith(AUTHENTICATE)]
            if config:
                self._connection.edit_config(candidate=config)
            for name, pem in self._certificates.items():
                self._install(name, pem)
        self.changed = True

    @staticmethod
    def _with_answer(command):
        """Removing a trustpoint asks for a confirmation, as it destroys the certificates it holds."""
        if command.startswith(DELETE):
            return {"command": command, "prompt": r"\[yes/no\]", "answer": "yes"}
        return command

    def _install(self, name, pem):
        """crypto pki authenticate: the certificate is pasted, the paste ends with "quit"."""
        lines = der_to_pem(pem_to_der(pem)).splitlines()
        response = self._connection.get(
            command=AUTHENTICATE + name,
            prompt=r'word "quit" on a line by itself',
            answer="\r".join(lines + ["quit"]),
        )
        if "successfully imported" not in (response or "").lower():
            self._module.fail_json(
                msg="crypto pki authenticate of the trustpoint %s failed, the configuration was applied."
                % name,
                response=response,
            )
