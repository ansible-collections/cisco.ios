# (c) 2026 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import base64
import hashlib
import textwrap

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.ios.plugins.modules import ios_pki_trustpoints
from ansible_collections.cisco.ios.tests.unit.modules.utils import set_module_args

from .ios_module import TestIosModule


# throwaway CA certificates of the tests, nothing secret
CA_A = """-----BEGIN CERTIFICATE-----
MIIDCjCCAfKgAwIBAgIUP7jXfowlwAd8SiXyBni41gizXOswDQYJKoZIhvcNAQEL
BQAwHTEbMBkGA1UEAwwSTGFiIFRlc3QgUm9vdCBDQSBBMB4XDTIwMDEwMTAwMDAw
MFoXDTQ2MDEwMTAwMDAwMFowHTEbMBkGA1UEAwwSTGFiIFRlc3QgUm9vdCBDQSBB
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwSFkKCsVmlJUDGgU/UcX
KqKWCunJtuDeVh6WC07rgEzZIxbMnX+VJV9XLelqFLOdtYgEcjQBBVuDQj4gtycu
j0qFB6lqk/a2Pgxqg/pg7cjTD2ek5wH3xhA8uw1Az0XqLf2tkyFb1l5wOEvKeoV4
i5+bCoeJwDW9Xe0d/Mx0ROzRZS0BbWIdg3QTcCLqurDa/vtKC5TPINhE74EO81Jg
RoMuCQZWITWDTUnbTBRqBE8YqpxidKJbCOFh6isCAkf4dewPcEaltVWvJVxTI64Y
pQwtKXOBnFqDpUnppCVG3Jsb1qGYtDpXIQw9idP4bj8uxrMyiMnDeInHXn+s3r81
JwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjAdBgNV
HQ4EFgQUKKrWXVTOJrVwyFsC3wkandsjdqcwDQYJKoZIhvcNAQELBQADggEBADq0
r0x1Jz3yZqdBoPNdnjhNaeDTnoAQUTrmJ6cWBvEqs12hhakR167b7B0OdjxRFEXE
nrYxqY2U9IHoMxfjR/RRzp5dOxBndx6ueouc2J38yBIeV9Ri3TsoGPeQwMu1UMxv
VV7sjeSa4gJTmvMCQh2tyvVR4rUG0yyfNMOFvGIt4ics7wcM/dgk//GBNlII/YFS
5TgDLpOSwkcxaJuoELyKXzZjHFFZYRDayHtitfAwjJo+QAuoddGhSSx4YPYCXJAx
fpjd0/Y9BmEmD3ruz3AMgejJhV2KkOlNSIWctHH3W4hleeV2qPjOUfGczeotJbfH
FRaFiDvygh8Q3SqGWrs=
-----END CERTIFICATE-----
"""
CA_B = """-----BEGIN CERTIFICATE-----
MIIDCjCCAfKgAwIBAgIUXJF5ihlb3Vr/cf0LdyR3p1bEl34wDQYJKoZIhvcNAQEL
BQAwHTEbMBkGA1UEAwwSTGFiIFRlc3QgUm9vdCBDQSBCMB4XDTIwMDEwMTAwMDAw
MFoXDTQ2MDEwMTAwMDAwMFowHTEbMBkGA1UEAwwSTGFiIFRlc3QgUm9vdCBDQSBC
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgCfO31juyGXGFFjssBz
Jff7sG4pasb5ApjWF+0PN6OycpO9JPK6aGpJrZ4kr3TZVArkg16jTG1pymCbV83M
VkmdpXUyoEDYIOZBqfiiT2c6FEGeMBIeGzSH932GIWCC4BNbYkIoVK0IwBlnh865
gyultXibD6rIPhwEeSpv/AIvH+pPIBYrrspEiYzWXljw6V9XXxeXxkWl+Gq9X2B/
5W7D4BU3d+3DBFG/jjjy9rFjEiLYGLuqxqvib9fyBKyoLSksAslTcxx+alMwrjAL
ecuc2tbt6eVXSwl+20UMVOiecCEYN3twnVZFYae9kJpKR+O/WUoWBgikyZTU3JuB
2wIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjAdBgNV
HQ4EFgQU+SFiDP3zPnjZ4YZgoBjrlpC0SRkwDQYJKoZIhvcNAQELBQADggEBADQd
GAB77KU6ZdhCMJRweXVaS7mWWIst6pxnKve5Aq0HbJjPVlt0zFC5hmVqsQNz2220
NRublxoPRRuIzcq+ODUnjBVsbk6VAJPnyIwyzJywfPFLmWV4P2a69MQrOG787ABS
W1uL/E5yGBusUZXXAMxICpiCB6/mflI2PzK7ShX9zkgRTfavAXrviv1+4Khh/R7B
uw5UY+IvPSex9MDXlp9dkXz/BESDn6RxpVQiXDIDFfYkNZvvDaEQXRwJOaNzEVAm
93JutXBOrbrtfhHK+fupHceZvZuW26GfEse5hH4+GE9zcNPL9Z19sPxMShynU84z
APhe0upM2HKovhOdZmM=
-----END CERTIFICATE-----
"""


def _der(pem):
    return base64.b64decode("".join(pem.strip().splitlines()[1:-1]))


def _sha1(pem):
    return hashlib.sha1(_der(pem)).hexdigest().upper()


def _chain(name, pem, kind="ca", serial="266FFBF2E589795D91003E4AD0B100DFF4C78563"):
    """The certificate chain of a trustpoint, as the running configuration prints it."""
    words = textwrap.wrap(_der(pem).hex().upper(), 8)
    lines = ["  " + line for line in textwrap.wrap(" ".join(words), 71)]
    return "crypto pki certificate chain %s\n certificate %s%s\n%s\n  \tquit\n" % (
        name,
        (kind + " ") if kind else "",
        serial,
        "\n".join(lines),
    )


SLA = dedent(
    """\
    crypto pki trustpoint SLA-TrustPoint
     enrollment pkcs12
     revocation-check crl
     hash sha256
    crypto pki trustpoint TP-self-signed-1000000001
     enrollment selfsigned
     subject-name cn=IOS-Self-Signed-Certificate-1000000001
     revocation-check none
     rsakeypair TP-self-signed-1000000001
     hash sha256
    """,
)
LAB = (
    dedent(
        """\
    crypto pki trustpoint LAB-CA
     enrollment terminal
     fingerprint %s
     revocation-check none
     hash sha256
    """,
    )
    % _sha1(CA_A)
)


class TestIosPkiTrustpointsModule(TestIosModule):
    module = ios_pki_trustpoints

    def setUp(self):
        super(TestIosPkiTrustpointsModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()
        self.connection = self.get_resource_connection_facts.return_value
        self.connection.get.return_value = "% Certificate successfully imported"

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.pki_trustpoints.pki_trustpoints."
            "Pki_trustpointsFacts.get_pki_trustpoints_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosPkiTrustpointsModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def _run(self, running, args, changed=True, failed=False):
        self.execute_show_command.return_value = running
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def _sent(self):
        """What was sent as configuration."""
        return self.connection.edit_config.call_args[1]["candidate"]

    # ------------------------------------------------------------------ merged

    def test_ios_pki_trustpoints_merged(self):
        result = self._run(
            SLA,
            {
                "config": [
                    {
                        "name": "WEB-CERT",
                        "enrollment": {"type": "selfsigned"},
                        "revocation_check": ["none"],
                        "hash": "sha256",
                        "subject_name": "CN=router.example.com",
                        "subject_alt_name": "router.example.com",
                        "rsakeypair": {"key_label": "web-key", "size": 2048},
                    },
                ],
                "state": "merged",
            },
        )
        expected = [
            "crypto pki trustpoint WEB-CERT",
            "enrollment selfsigned",
            "revocation-check none",
            "hash sha256",
            "subject-name CN=router.example.com",
            "subject-alt-name router.example.com",
            "rsakeypair web-key 2048",
        ]
        self.assertEqual(result["commands"], expected)
        self.assertEqual(self._sent(), expected)
        self.connection.get.assert_not_called()

    def test_ios_pki_trustpoints_merged_idempotent(self):
        result = self._run(
            SLA,
            {
                "config": [
                    {
                        "name": "SLA-TrustPoint",
                        "enrollment": {"type": "pkcs12"},
                        "revocation_check": ["crl"],
                        "hash": "sha256",
                    },
                    {
                        "name": "TP-self-signed-1000000001",
                        "rsakeypair": {"key_label": "TP-self-signed-1000000001"},
                    },
                ],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])
        self.connection.edit_config.assert_not_called()

    def test_ios_pki_trustpoints_merged_keeps_what_is_not_in_the_task(self):
        result = self._run(
            SLA,
            {"config": [{"name": "SLA-TrustPoint", "hash": "sha384"}], "state": "merged"},
        )
        self.assertEqual(
            result["commands"],
            ["crypto pki trustpoint SLA-TrustPoint", "hash sha384"],
        )

    def test_ios_pki_trustpoints_merged_revocation_check_is_an_ordered_list_not_a_union(self):
        result = self._run(
            SLA,
            {
                "config": [{"name": "SLA-TrustPoint", "revocation_check": ["ocsp", "none"]}],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["crypto pki trustpoint SLA-TrustPoint", "revocation-check ocsp none"],
        )

    def test_ios_pki_trustpoints_enrollment_url(self):
        result = self._run(
            "",
            {
                "config": [
                    {
                        "name": "SCEP",
                        "enrollment": {"type": "url", "url": "http://192.0.2.10:80"},
                    },
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["crypto pki trustpoint SCEP", "enrollment url http://192.0.2.10:80"],
        )

    def test_ios_pki_trustpoints_enrollment_terminal_pem(self):
        result = self._run(
            "",
            {
                "config": [{"name": "T", "enrollment": {"type": "terminal", "pem": True}}],
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["crypto pki trustpoint T", "enrollment terminal pem"])

    def test_ios_pki_trustpoints_pem_is_refused_with_a_url(self):
        # the switches refuse "enrollment url <url> pem" (IOS XE 17.12.4 and 17.18.04)
        for state in ("merged", "replaced"):
            result = self._run(
                "",
                {
                    "config": [
                        {
                            "name": "SCEP",
                            "enrollment": {
                                "type": "url",
                                "url": "http://192.0.2.10:80",
                                "pem": True,
                            },
                        },
                    ],
                    "state": state,
                },
                failed=True,
            )
            self.assertIn("only supported with the type terminal", result["msg"], state)

    def test_ios_pki_trustpoints_changing_the_method_does_not_keep_pem(self):
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal pem\n",
            {
                "config": [
                    {"name": "T", "enrollment": {"type": "url", "url": "http://192.0.2.10:80"}},
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["crypto pki trustpoint T", "enrollment url http://192.0.2.10:80"],
        )

    def test_ios_pki_trustpoints_merged_can_turn_pem_off(self):
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal pem\n",
            {
                "config": [{"name": "T", "enrollment": {"type": "terminal", "pem": False}}],
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["crypto pki trustpoint T", "enrollment terminal"])

    def test_ios_pki_trustpoints_terminal_to_terminal_pem_and_back(self):
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal\n",
            {
                "config": [{"name": "T", "enrollment": {"type": "terminal", "pem": True}}],
                "state": "merged",
            },
        )
        self.assertEqual(result["commands"], ["crypto pki trustpoint T", "enrollment terminal pem"])
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal pem\n",
            {
                "config": [{"name": "T", "enrollment": {"type": "terminal", "pem": False}}],
                "state": "replaced",
            },
        )
        self.assertEqual(result["commands"], ["crypto pki trustpoint T", "enrollment terminal"])

    def test_ios_pki_trustpoints_enrollment_url_needs_the_url(self):
        self._run(
            "",
            {"config": [{"name": "SCEP", "enrollment": {"type": "url"}}], "state": "merged"},
            failed=True,
        )

    def test_ios_pki_trustpoints_pem_false_is_the_same_as_no_pem(self):
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal\n",
            {
                "config": [{"name": "T", "enrollment": {"type": "terminal", "pem": False}}],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_ios_pki_trustpoints_fingerprint_is_compared_without_separators_and_case(self):
        result = self._run(
            "crypto pki trustpoint T\n enrollment terminal\n fingerprint 68028C590C6CC086A62DE7D04032477D2AA6CBC2\n",
            {
                "config": [
                    {"name": "T", "fingerprint": "68:02:8c:59 0c6cc086a62de7d04032477d2aa6cbc2"},
                ],
                "state": "merged",
            },
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    # ---------------------------------------------------------------- replaced

    def test_ios_pki_trustpoints_replaced_removes_what_can_be_removed(self):
        result = self._run(
            SLA,
            {
                "config": [
                    {"name": "TP-self-signed-1000000001", "enrollment": {"type": "selfsigned"}},
                ],
                "state": "replaced",
            },
        )
        # enrollment, revocation-check and hash always have a value on IOS: they are not removed
        self.assertEqual(
            result["commands"],
            [
                "crypto pki trustpoint TP-self-signed-1000000001",
                "no subject-name cn=IOS-Self-Signed-Certificate-1000000001",
                "no rsakeypair TP-self-signed-1000000001",
            ],
        )

    def test_ios_pki_trustpoints_replaced_idempotent_and_changes_what_is_in_the_task(self):
        args = {
            "config": [
                {
                    "name": "TP-self-signed-1000000001",
                    "enrollment": {"type": "selfsigned"},
                    "subject_name": "cn=IOS-Self-Signed-Certificate-1000000001",
                    "revocation_check": ["none"],
                    "rsakeypair": {"key_label": "TP-self-signed-1000000001"},
                    "hash": "sha256",
                },
            ],
            "state": "replaced",
        }
        result = self._run(SLA, args, changed=False)
        self.assertEqual(result["commands"], [])
        args["config"][0]["hash"] = "sha512"
        result = self._run(SLA, args)
        self.assertEqual(
            result["commands"],
            ["crypto pki trustpoint TP-self-signed-1000000001", "hash sha512"],
        )

    def test_ios_pki_trustpoints_trustpoints_that_are_not_named_are_never_touched(self):
        for state in ("merged", "replaced"):
            result = self._run(
                SLA + _chain("SLA-TrustPoint", CA_A, serial="01"),
                {"config": [{"name": "OTHER", "enrollment": {"type": "terminal"}}], "state": state},
            )
            self.assertEqual(
                result["commands"],
                ["crypto pki trustpoint OTHER", "enrollment terminal"],
                state,
            )

    # ----------------------------------------------------------------- deleted

    def test_ios_pki_trustpoints_deleted_answers_the_confirmation(self):
        result = self._run(
            SLA + LAB,
            {"config": [{"name": "LAB-CA"}, {"name": "UNKNOWN"}], "state": "deleted"},
        )
        self.assertEqual(result["commands"], ["no crypto pki trustpoint LAB-CA"])
        self.assertEqual(
            self._sent(),
            [
                {
                    "command": "no crypto pki trustpoint LAB-CA",
                    "prompt": r"\[yes/no\]",
                    "answer": "yes",
                },
            ],
        )

    def test_ios_pki_trustpoints_deleted_refuses_a_trustpoint_with_a_ca_certificate(self):
        result = self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {"config": [{"name": "LAB-CA"}], "state": "deleted"},
            failed=True,
        )
        self.assertIn("LAB-CA", result["msg"])
        self.assertIn("hold a CA certificate", result["msg"])
        self.assertIn("delete_certificates", result["msg"])
        self.connection.edit_config.assert_not_called()

    def test_ios_pki_trustpoints_deleted_refuses_when_the_flag_is_false(self):
        self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {"config": [{"name": "LAB-CA", "delete_certificates": False}], "state": "deleted"},
            failed=True,
        )
        self.connection.edit_config.assert_not_called()

    def test_ios_pki_trustpoints_deleted_with_the_flag_removes_it_and_answers_the_confirmation(
        self,
    ):
        result = self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {"config": [{"name": "LAB-CA", "delete_certificates": True}], "state": "deleted"},
        )
        self.assertEqual(result["commands"], ["no crypto pki trustpoint LAB-CA"])
        self.assertEqual(
            self._sent(),
            [
                {
                    "command": "no crypto pki trustpoint LAB-CA",
                    "prompt": r"\[yes/no\]",
                    "answer": "yes",
                },
            ],
        )

    def test_ios_pki_trustpoints_deleted_without_a_certificate_needs_no_flag(self):
        # a trustpoint that holds no CA certificate, here a self-signed one is not a CA certificate either
        result = self._run(
            SLA + _chain("TP-self-signed-1000000001", CA_B, kind="self-signed", serial="01"),
            {"config": [{"name": "TP-self-signed-1000000001"}], "state": "deleted"},
        )
        self.assertEqual(result["commands"], ["no crypto pki trustpoint TP-self-signed-1000000001"])

    def test_ios_pki_trustpoints_deleted_removes_nothing_when_one_of_them_is_refused(self):
        result = self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {"config": [{"name": "SLA-TrustPoint"}, {"name": "LAB-CA"}], "state": "deleted"},
            failed=True,
        )
        # SLA-TrustPoint holds a CA certificate as well, it is named too
        self.assertNotIn("TP-self-signed", result["msg"])
        self.connection.edit_config.assert_not_called()

    def test_ios_pki_trustpoints_deleted_names_only_the_refused_ones(self):
        result = self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {
                "config": [{"name": "TP-self-signed-1000000001"}, {"name": "LAB-CA"}],
                "state": "deleted",
            },
            failed=True,
        )
        self.assertIn("LAB-CA", result["msg"])
        self.assertNotIn("TP-self-signed-1000000001", result["msg"])
        self.connection.edit_config.assert_not_called()

    def test_ios_pki_trustpoints_deleted_in_check_mode_refuses_as_well(self):
        self._run(
            SLA + LAB + _chain("LAB-CA", CA_A),
            {"config": [{"name": "LAB-CA"}], "state": "deleted", "_ansible_check_mode": True},
            failed=True,
        )

    def test_ios_pki_trustpoints_the_flag_does_nothing_in_the_other_states(self):
        entry = {
            "name": "LAB-CA",
            "enrollment": {"type": "terminal"},
            "fingerprint": _sha1(CA_A),
            "revocation_check": ["none"],
            "hash": "sha256",
            "delete_certificates": True,
        }
        for state in ("merged", "replaced"):
            result = self._run(
                SLA + LAB + _chain("LAB-CA", CA_A),
                {"config": [entry], "state": state},
                changed=False,
            )
            self.assertEqual(result["commands"], [], state)

    def test_ios_pki_trustpoints_deleted_needs_the_names(self):
        self._run(SLA, {"state": "deleted"}, failed=True)

    def test_ios_pki_trustpoints_deleted_idempotent(self):
        result = self._run(
            SLA,
            {"config": [{"name": "UNKNOWN"}], "state": "deleted"},
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    # ---------------------------------------------------------- ca_certificate

    def _install_args(self, **overrides):
        entry = {
            "name": "LAB-CA",
            "enrollment": {"type": "terminal"},
            "revocation_check": ["none"],
            "fingerprint": _sha1(CA_A),
            "ca_certificate": CA_A,
        }
        entry.update(overrides)
        return {"config": [entry], "state": "merged"}

    def test_ios_pki_trustpoints_ca_certificate_is_installed_after_the_configuration(self):
        result = self._run(SLA, self._install_args())
        self.assertEqual(
            result["commands"],
            [
                "crypto pki trustpoint LAB-CA",
                "enrollment terminal",
                "revocation-check none",
                "fingerprint %s" % _sha1(CA_A),
                "crypto pki authenticate LAB-CA",
            ],
        )
        # the authentication is not configuration
        self.assertEqual(self._sent(), result["commands"][:-1])
        kwargs = self.connection.get.call_args[1]
        self.assertEqual(kwargs["command"], "crypto pki authenticate LAB-CA")
        self.assertEqual(kwargs["prompt"], r'word "quit" on a line by itself')
        self.assertEqual(
            kwargs["answer"].split("\r"),
            CA_A.strip().splitlines() + ["quit"],
        )

    def test_ios_pki_trustpoints_ca_certificate_is_idempotent(self):
        result = self._run(SLA + LAB + _chain("LAB-CA", CA_A), self._install_args(), changed=False)
        self.assertEqual(result["commands"], [])
        self.connection.get.assert_not_called()

    def test_ios_pki_trustpoints_ca_certificate_is_installed_in_a_trustpoint_that_exists(self):
        result = self._run(SLA + LAB, self._install_args())
        self.assertEqual(result["commands"], ["crypto pki authenticate LAB-CA"])
        self.connection.edit_config.assert_not_called()
        self.connection.get.assert_called_once()

    def test_ios_pki_trustpoints_another_ca_certificate_is_an_error(self):
        result = self._run(SLA + LAB + _chain("LAB-CA", CA_B), self._install_args(), failed=True)
        self.assertIn("already holds another CA certificate", result["msg"])
        self.connection.get.assert_not_called()

    def test_ios_pki_trustpoints_ca_certificate_needs_the_fingerprint(self):
        args = self._install_args()
        del args["config"][0]["fingerprint"]
        result = self._run("", args, failed=True)
        self.assertIn("needs a fingerprint", result["msg"])
        self.assertIn(_sha1(CA_A), result["msg"])

    def test_ios_pki_trustpoints_fingerprint_must_match_the_certificate(self):
        result = self._run("", self._install_args(fingerprint=_sha1(CA_B)), failed=True)
        self.assertIn("does not match", result["msg"])

    def test_ios_pki_trustpoints_ca_certificate_needs_enrollment_terminal(self):
        result = self._run("", self._install_args(enrollment={"type": "selfsigned"}), failed=True)
        self.assertIn("enrollment type terminal", result["msg"])

    def test_ios_pki_trustpoints_ca_certificate_must_be_pem(self):
        result = self._run("", self._install_args(ca_certificate="not a certificate"), failed=True)
        self.assertIn("not a PEM certificate", result["msg"])

    def test_ios_pki_trustpoints_a_failed_import_is_reported(self):
        self.connection.get.return_value = "% Error in saving certificate: status = FAIL"
        result = self._run("", self._install_args(), failed=True)
        self.assertIn("failed, the configuration was applied", result["msg"])
        self.assertIn("status = FAIL", result["response"])

    def test_ios_pki_trustpoints_check_mode_sends_nothing(self):
        args = self._install_args()
        args["_ansible_check_mode"] = True
        result = self._run(SLA, args)
        self.assertEqual(result["commands"][-1], "crypto pki authenticate LAB-CA")
        self.connection.edit_config.assert_not_called()
        self.connection.get.assert_not_called()

    def test_ios_pki_trustpoints_rendered(self):
        set_module_args(
            {
                "config": [
                    {
                        "name": "LAB-CA",
                        "enrollment": {"type": "terminal", "pem": True},
                        "fingerprint": _sha1(CA_A),
                        "ca_certificate": CA_A,
                    },
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "crypto pki trustpoint LAB-CA",
                "enrollment terminal pem",
                "fingerprint %s" % _sha1(CA_A),
                "crypto pki authenticate LAB-CA",
            ],
        )

    # ------------------------------------------------------------------- facts

    def test_ios_pki_trustpoints_parsed(self):
        running = (
            SLA
            + dedent(
                """\
                crypto pki trustpoint SCEP
                 enrollment url http://192.0.2.10:80 pem
                 fingerprint 68:02:8C:59
                 revocation-check crl ocsp none
                 subject-alt-name router.example.com
                 rsakeypair web-key 2048 2048
                 hash sha1
                """,
            )
            + LAB
            + _chain("SLA-TrustPoint", CA_B, serial="01")
            + _chain("TP-self-signed-1000000001", CA_B, kind="self-signed", serial="01")
            + _chain("LAB-CA", CA_A)
        )
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        parsed = {entry["name"]: entry for entry in result["parsed"]}
        self.assertEqual(
            sorted(parsed),
            ["LAB-CA", "SCEP", "SLA-TrustPoint", "TP-self-signed-1000000001"],
        )
        self.assertEqual(
            parsed["SCEP"],
            {
                "name": "SCEP",
                "enrollment": {"type": "url", "url": "http://192.0.2.10:80", "pem": True},
                "fingerprint": "68028C59",
                "revocation_check": ["crl", "ocsp", "none"],
                "subject_alt_name": "router.example.com",
                "rsakeypair": {"key_label": "web-key", "size": 2048},
                "hash": "sha1",
            },
        )
        # the certificate of the chain is returned as a PEM, a self-signed one is not a CA certificate
        self.assertEqual(parsed["LAB-CA"]["ca_certificate"], CA_A)
        self.assertEqual(parsed["SLA-TrustPoint"]["ca_certificate"], CA_B)
        self.assertNotIn("ca_certificate", parsed["TP-self-signed-1000000001"])
        self.assertEqual(parsed["SLA-TrustPoint"]["enrollment"], {"type": "pkcs12"})

    def test_ios_pki_trustpoints_gathered(self):
        self.execute_show_command.return_value = LAB + _chain("LAB-CA", CA_A)
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["gathered"],
            [
                {
                    "name": "LAB-CA",
                    "enrollment": {"type": "terminal"},
                    "fingerprint": _sha1(CA_A),
                    "revocation_check": ["none"],
                    "hash": "sha256",
                    "ca_certificate": CA_A,
                },
            ],
        )

    def test_ios_pki_trustpoints_other_lines_do_not_break_the_facts(self):
        running = (
            "crypto pki trustpool policy\n cabundle url http://ca.example.com/bundle.p7b\n"
            + SLA
            + " serial-number none\n crl cache none\n"
            + _chain("SLA-TrustPoint", CA_B, serial="01")
        )
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            [e["name"] for e in result["parsed"]],
            ["SLA-TrustPoint", "TP-self-signed-1000000001"],
        )
