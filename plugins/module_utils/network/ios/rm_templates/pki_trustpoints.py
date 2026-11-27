# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Pki_trustpoints parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import base64
import binascii
import hashlib
import re
import textwrap

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_NAME = "{{ name }}"


def _enrollment(data):
    enrollment = data["enrollment"]
    command = "enrollment " + (
        "url " + enrollment["url"] if enrollment["type"] == "url" else enrollment["type"]
    )
    if enrollment.get("pem"):
        command += " pem"
    return command


def _revocation_check(data):
    return "revocation-check " + " ".join(data["revocation_check"])


def _rsakeypair(data):
    keypair = data["rsakeypair"]
    command = "rsakeypair " + keypair["key_label"]
    if keypair.get("size"):
        command += " " + str(keypair["size"])
    return command


def pem_to_der(pem):
    """The DER bytes of a PEM certificate, None when it is not one."""
    lines = [line.strip() for line in (pem or "").strip().splitlines() if line.strip()]
    if (
        len(lines) < 3
        or lines[0] != "-----BEGIN CERTIFICATE-----"
        or lines[-1] != "-----END CERTIFICATE-----"
    ):
        return None
    try:
        return base64.b64decode("".join(lines[1:-1]), validate=True)
    except (binascii.Error, ValueError):
        return None


def der_to_pem(der):
    """A PEM certificate, in the form of "openssl x509"."""
    body = base64.b64encode(der).decode("ascii")
    lines = textwrap.wrap(body, 64)
    return "\n".join(["-----BEGIN CERTIFICATE-----"] + lines + ["-----END CERTIFICATE-----"]) + "\n"


def fingerprints(der):
    """The fingerprints IOS asks for, hexadecimal without separators."""
    return {
        "md5": hashlib.md5(der).hexdigest().upper(),  # nosec - a fingerprint, not a signature
        "sha1": hashlib.sha1(der).hexdigest().upper(),  # nosec - a fingerprint, not a signature
        "sha256": hashlib.sha256(der).hexdigest().upper(),
    }


def normalize_fingerprint(value):
    """ "68:02 8C" and "68028c" are the same fingerprint."""
    return re.sub(r"[^0-9A-Fa-f]", "", value or "").upper()


class Pki_trustpointsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Pki_trustpointsTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(r"^crypto\spki\strustpoint\s(?P<name>\S+)$"),
            "setval": "crypto pki trustpoint {{ name }}",
            "result": {_NAME: {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "enrollment",
            "getval": re.compile(r"^\senrollment\s(?P<type>terminal|selfsigned|pkcs12)(?:\s(?P<pem>pem))?$"),
            "setval": _enrollment,
            "remval": _enrollment,
            "result": {_NAME: {"enrollment": {"type": "{{ type }}", "pem": "{{ True if pem is defined }}"}}},
        },
        {
            "name": "enrollment_url",
            "getval": re.compile(r"^\senrollment\surl\s(?P<url>\S+)(?:\s(?P<pem>pem))?$"),
            "setval": _enrollment,
            "remval": _enrollment,
            "result": {_NAME: {"enrollment": {"type": "url", "url": "{{ url }}", "pem": "{{ True if pem is defined }}"}}},
        },
        {
            "name": "revocation_check",
            "getval": re.compile(r"^\srevocation-check\s(?P<methods>(?:crl|ocsp|none)(?:\s(?:crl|ocsp|none))*)$"),
            "setval": _revocation_check,
            "remval": _revocation_check,
            # the methods are in the order they are tried, the facts turn the string into a list
            "result": {_NAME: {"revocation_check": "{{ methods }}"}},
        },
        {
            "name": "hash",
            "getval": re.compile(r"^\shash\s(?P<hash>sha1|sha256|sha384|sha512)$"),
            "setval": "hash {{ hash }}",
            "remval": "hash {{ hash }}",
            "result": {_NAME: {"hash": "{{ hash }}"}},
        },
        {
            "name": "fingerprint",
            "getval": re.compile(r"^\sfingerprint\s(?P<fingerprint>[0-9A-Fa-f: ]+)$"),
            "setval": "fingerprint {{ fingerprint }}",
            "remval": "fingerprint {{ fingerprint }}",
            "result": {_NAME: {"fingerprint": "{{ fingerprint }}"}},
        },
        {
            "name": "subject_name",
            "getval": re.compile(r"^\ssubject-name\s(?P<subject_name>.+)$"),
            "setval": "subject-name {{ subject_name }}",
            "remval": "subject-name {{ subject_name }}",
            "result": {_NAME: {"subject_name": "{{ subject_name }}"}},
        },
        {
            "name": "subject_alt_name",
            "getval": re.compile(r"^\ssubject-alt-name\s(?P<subject_alt_name>.+)$"),
            "setval": "subject-alt-name {{ subject_alt_name }}",
            "remval": "subject-alt-name {{ subject_alt_name }}",
            "result": {_NAME: {"subject_alt_name": "{{ subject_alt_name }}"}},
        },
        {
            # the label is not called "name", that is the shared name of the trustpoint
            "name": "rsakeypair",
            "getval": re.compile(r"^\srsakeypair\s(?P<key_label>\S+)(?:\s(?P<size>\d+))?(?:\s\d+)?$"),
            "setval": _rsakeypair,
            "remval": _rsakeypair,
            "result": {_NAME: {"rsakeypair": {"key_label": "{{ key_label }}", "size": "{{ size | int if size is defined }}"}}},
        },
    ]
    # fmt: on
