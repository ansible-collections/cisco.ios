#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_pki_trustpoints
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: ios_pki_trustpoints
short_description: Resource module to configure PKI trustpoints.
description:
  - This module configures and manages the attributes of PKI trustpoints on Cisco IOS.
version_added: 11.8.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against Cisco IOS XE Software, Version 17.12.4 and 17.18.4 on a Catalyst 9300.
  - This module works with connection C(network_cli).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html)
  - Only the trustpoints named in the task are touched, the others (for example C(SLA-TrustPoint) and the
    self-signed trustpoint of the web server) are left alone in every state.
  - Options of a trustpoint that are not listed here are not changed. C(enrollment), C(revocation_check) and C(hash)
    always have a value on IOS, they are changed when they are in the task and never removed.
options:
  config:
    description: A list of trustpoints.
    type: list
    elements: dict
    suboptions:
      name:
        description: Name of the trustpoint.
        type: str
        required: true
      enrollment:
        description: How the certificate of the CA is obtained (C(enrollment)).
        type: dict
        suboptions:
          type:
            description: The method, C(terminal) for a certificate that is pasted, as with I(ca_certificate).
            type: str
            required: true
            choices: ["terminal", "selfsigned", "pkcs12", "url"]
          url:
            description:
              - URL of the CA, required when I(type=url).
              - IOS resolves a host name when the command is entered, it must resolve on the device. An IP address always works.
            type: str
          pem:
            description:
              - Use PEM boundaries in the certificate requests (C(enrollment terminal pem)).
              - Only with I(type=terminal), IOS XE 17.12 and 17.18 refuse C(pem) after a url.
            type: bool
      revocation_check:
        description:
          - Methods used to check the revocation of a certificate, in the order they are tried (C(revocation-check)).
        type: list
        elements: str
        choices: ["crl", "ocsp", "none"]
      hash:
        description: Hash algorithm of the certificate requests and of the self-signed certificate (C(hash)).
        type: str
        choices: ["sha1", "sha256", "sha384", "sha512"]
      fingerprint:
        description:
          - Fingerprint of the certificate of the CA, hexadecimal. Colons and spaces are ignored (C(fingerprint)).
          - IOS refuses to authenticate a CA certificate unless the trustpoint pins its fingerprint, it is required with I(ca_certificate).
        type: str
      subject_name:
        description: Subject name of the certificate of the device (C(subject-name)).
        type: str
      subject_alt_name:
        description: Subject alternative name of the certificate of the device (C(subject-alt-name)).
        type: str
      rsakeypair:
        description: The RSA key pair of the trustpoint (C(rsakeypair)).
        type: dict
        suboptions:
          key_label:
            description: Name of the key pair.
            type: str
            required: true
          size:
            description: Size of the key pair, when the key pair is generated.
            type: int
      delete_certificates:
        description:
          - Allow state I(deleted) to remove the trustpoint although it holds a CA certificate, it is refused otherwise. Default C(false).
        type: bool
      ca_certificate:
        description:
          - The certificate of the CA, PEM. It is installed with C(crypto pki authenticate) when the trustpoint does not hold it yet.
          - Needs I(enrollment.type=terminal) and a I(fingerprint) that matches the certificate, SHA-1 or MD5.
          - It is never removed or replaced by this module, a trustpoint that holds another certificate of a CA is an error,
            remove the trustpoint first with state I(deleted).
          - It is returned by the state I(gathered) as it is in the configuration of the device.
        type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the IOS device by
        executing the command B(show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With state I(merged), the provided options are added to the trustpoints named in the task. Nothing is removed.
      - With state I(replaced), the trustpoints named in the task are made to match, the options that can be removed
        and that are not in the task are removed.
      - With state I(deleted), the trustpoints named in the task are removed. A trustpoint that holds a CA certificate is only removed with
        I(delete_certificates), nothing is removed when one of them is refused. I(config) is required.
      - With state I(gathered), the configuration is read from the device and returned in I(gathered).
      - With state I(rendered), the task configuration is returned as device commands in I(rendered)
        without connecting to the device.
      - With state I(parsed), I(running_config) is returned as structured data in I(parsed).
    type: str
    choices:
      - merged
      - replaced
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# router#show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain
# router#

- name: Add the root CA of the company to the trust store
  cisco.ios.ios_pki_trustpoints:
    config:
      - name: COMPANY-ROOT-CA
        enrollment:
          type: terminal
        revocation_check:
          - none
        fingerprint: 68028C590C6CC086A62DE7D04032477D2AA6CBC2
        ca_certificate: "{{ lookup('ansible.builtin.file', 'company-root-ca.pem') }}"
    state: merged

# Task Output
# -----------
#
# commands:
#   - crypto pki trustpoint COMPANY-ROOT-CA
#   - enrollment terminal
#   - revocation-check none
#   - fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2
#   - crypto pki authenticate COMPANY-ROOT-CA

# After state:
# ------------
#
# router#show running-config | section ^crypto pki trustpoint|^crypto pki certificate chain
# crypto pki trustpoint COMPANY-ROOT-CA
#  enrollment terminal
#  fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2
#  revocation-check none
# crypto pki certificate chain COMPANY-ROOT-CA
#  certificate ca 266FFBF2E589795D91003E4AD0B100DFF4C78563
#   30820306 308201EE A0030201 02021426 6FFBF2E5 89795D91 003E4AD0 B100DFF4
#   ...
#         quit

# Using replaced

# Before state:
# -------------
#
# crypto pki trustpoint WEB-CERT
#  enrollment terminal
#  subject-name CN=router.example.com
#  revocation-check none
#  rsakeypair web-key

- name: Replace the options of a trustpoint
  cisco.ios.ios_pki_trustpoints:
    config:
      - name: WEB-CERT
        enrollment:
          type: terminal
        revocation_check:
          - crl
          - none
        rsakeypair:
          key_label: web-key
    state: replaced

# Task Output
# -----------
#
# commands:
#   - crypto pki trustpoint WEB-CERT
#   - revocation-check crl none
#   - no subject-name CN=router.example.com

# Using deleted

- name: Remove a trustpoint and the CA certificate it holds
  cisco.ios.ios_pki_trustpoints:
    config:
      - name: COMPANY-ROOT-CA
        delete_certificates: true
    state: deleted

# Task Output
# -----------
#
# commands:
#   - no crypto pki trustpoint COMPANY-ROOT-CA

# Using gathered

- name: Gather the trustpoints
  cisco.ios.ios_pki_trustpoints:
    state: gathered

# Task Output
# -----------
#
# gathered:
#   - name: COMPANY-ROOT-CA
#     enrollment:
#       type: terminal
#     revocation_check:
#       - none
#     fingerprint: 68028C590C6CC086A62DE7D04032477D2AA6CBC2
#     ca_certificate: |
#       -----BEGIN CERTIFICATE-----
#       MIIDCjCCAfKgAwIBAgIU...
#       -----END CERTIFICATE-----

# Using rendered

- name: Render the commands of a trustpoint
  cisco.ios.ios_pki_trustpoints:
    config:
      - name: WEB-CERT
        enrollment:
          type: selfsigned
        hash: sha256
        subject_name: CN=router.example.com
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - crypto pki trustpoint WEB-CERT
#   - enrollment selfsigned
#   - hash sha256
#   - subject-name CN=router.example.com

# Using parsed

- name: Parse the trustpoints
  cisco.ios.ios_pki_trustpoints:
    running_config: |
      crypto pki trustpoint WEB-CERT
       enrollment terminal
       revocation-check crl none
       hash sha256
    state: parsed

# Task Output
# -----------
#
# parsed:
#   - name: WEB-CERT
#     enrollment:
#       type: terminal
#     revocation_check:
#       - crl
#       - none
#     hash: sha256
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: when I(state) is C(merged), C(replaced) or C(deleted)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description:
    - The set of commands pushed to the remote device.
    - C(crypto pki authenticate) is not a configuration command, it is run after the configuration is applied.
  returned: when I(state) is C(merged), C(replaced) or C(deleted)
  type: list
  sample:
    - crypto pki trustpoint COMPANY-ROOT-CA
    - enrollment terminal
    - fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2
    - crypto pki authenticate COMPANY-ROOT-CA
rendered:
  description: The provided configuration in the task rendered in device native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - crypto pki trustpoint WEB-CERT
    - enrollment selfsigned
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    emit_warnings,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.pki_trustpoints.pki_trustpoints import (
    Pki_trustpointsArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.pki_trustpoints.pki_trustpoints import (
    Pki_trustpoints,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Pki_trustpointsArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "deleted", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Pki_trustpoints(module).execute_module()
    emit_warnings(module, result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
