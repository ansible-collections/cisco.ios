# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The ios pki_trustpoints fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import binascii
import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.pki_trustpoints.pki_trustpoints import (
    Pki_trustpointsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.pki_trustpoints import (
    Pki_trustpointsTemplate,
    der_to_pem,
    normalize_fingerprint,
)


class Pki_trustpointsFacts(object):
    """The ios pki_trustpoints facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Pki_trustpointsArgs.argument_spec

    def get_pki_trustpoints_data(self, connection):
        return connection.get(
            "show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain",
        )

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Pki_trustpoints network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_pki_trustpoints_data(connection)

        trustpoint_lines, chains = self._split(data)
        parser = Pki_trustpointsTemplate(lines=trustpoint_lines, module=self._module)
        parsed = parser.parse()

        objs = []
        for name in sorted(parsed):
            entry = parsed[name]
            if entry.get("revocation_check"):
                entry["revocation_check"] = entry["revocation_check"].split()
            if entry.get("fingerprint"):
                entry["fingerprint"] = normalize_fingerprint(entry["fingerprint"])
            ca_certificates = [c for c in chains.get(name, []) if c["kind"] == "ca"]
            if ca_certificates:
                entry["ca_certificate"] = der_to_pem(ca_certificates[0]["der"])
            objs.append(entry)

        ansible_facts["ansible_network_resources"].pop("pki_trustpoints", None)

        params = utils.remove_empties(
            parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["pki_trustpoints"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _split(data):
        """The lines of the trustpoints, and the certificates of the chains.

        A chain is "certificate ca <serial>" followed by the certificate as hexadecimal words and a "quit".
        """
        trustpoint_lines = []
        chains = {}
        mode = None
        name = None
        current = None
        for line in data.splitlines():
            if line.startswith("crypto pki trustpoint "):
                mode, current = "trustpoint", None
                trustpoint_lines.append(line)
            elif line.startswith("crypto pki certificate chain "):
                mode, current = "chain", None
                name = line.split()[-1]
                chains.setdefault(name, [])
            elif line and not line[0].isspace():
                mode, current = None, None
            elif mode == "trustpoint":
                trustpoint_lines.append(line)
            elif mode == "chain":
                match = re.match(
                    r"^\scertificate\s(?:(?P<kind>ca|self-signed)\s)?(?P<serial>\S+)\s*$",
                    line,
                )
                if match:
                    current = {
                        "kind": match.group("kind") or "device",
                        "serial": match.group("serial"),
                        "hex": "",
                    }
                    chains[name].append(current)
                elif current is not None and re.match(r"^\s+[0-9A-Fa-f ]+$", line):
                    current["hex"] += line.replace(" ", "").strip()
        for certificates in chains.values():
            for certificate in certificates:
                try:
                    certificate["der"] = binascii.unhexlify(certificate.pop("hex"))
                except (binascii.Error, ValueError):
                    certificate["der"] = b""
        return trustpoint_lines, chains
