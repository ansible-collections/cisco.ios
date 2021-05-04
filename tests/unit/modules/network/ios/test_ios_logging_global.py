#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.ios.tests.unit.compat.mock import patch
from ansible_collections.cisco.ios.plugins.modules import ios_logging_global
from ansible_collections.cisco.ios.tests.unit.modules.utils import (
    set_module_args,
)
from .ios_module import TestIosModule, load_fixture

# import debugpy
# debugpy.listen(3000)
# debugpy.wait_for_client()

class TestIosLoggingGlobalModule(TestIosModule):
    module = ios_logging_global

    def setUp(self):
        super(TestIosLoggingGlobalModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base."
            "get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers.CliProvider.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.logging_global.logging_global."
            "Logging_globalFacts.get_logging_data"
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestIosLoggingGlobalModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    # def load_fixtures(self, commands=None):
    #     def load_from_file(*args, **kwargs):
    #         return load_fixture("ios_logging_global.cfg")

    #     self.execute_show_command.side_effect = load_from_file
        
        
    # def test_ios_logging_global_mergedx(self):    
    #     playbook = dict(
    #         config=[
    #             dict(logging_on="enable"),
    #         ]
    #     )
        
    #     merged = [
    #         "logging on",
    #     ]
    #     playbook["state"] = "merged"
    #     set_module_args(playbook)
    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(merged))
        
    def test_ios_logging_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            logging buginf
            logging userinfo
            logging esm config
            logging server-arp
            logging trap errors
            logging delimiter tcp
            logging reload alerts
            logging host 10.0.1.1
            logging exception 4099
            logging history alerts
            logging facility local5
            logging snmp-trap errors
            logging monitor warnings
            logging origin-id hostname
            logging host 10.0.1.11 xml
            logging cns-events warnings
            logging queue-limit esm 150
            logging dmvpn rate-limit 10
            logging message-counter log
            logging console xml critical
            logging message-counter debug
            logging persistent batch 4444
            logging host 10.0.1.25 filtered
            logging source-interface GBit1/0
            logging source-interface CTunnel2
            logging policy-firewall rate-limit 10
            logging buffered xml 5099 notifications
            logging rate-limit all 2 except warnings
            logging host 10.0.1.10 filtered stream 10
            logging host 10.0.1.13 transport tcp port 514
            logging discriminator msglog01 severity includes 5
            logging filter tftp://10.0.2.18/ESM/elate.tcl args TESTInst2
            logging filter tftp://10.0.2.14/ESM/escalate.tcl args TESTInst
            """
        )
        playbook = dict(
            config=[
                dict(logging_on="enable"),
                dict(
                    buffered=dict(
                        size=5099,
                        severity="notifications",
                        xml=True,
                    )
                ),
                dict(buginf=True),
                dict(cns_events="warnings"),
                dict(
                    console=dict(
                        severity="critical",
                        xml=True,
                    )
                ),
                dict(count=True),
                dict(
                    delimiter=dict(
                        tcp=True,
                    )
                ),
                dict(discriminator=["msglog01 severity includes 5",]),
                dict(
                    dmvpn=dict(
                        rate_limit=10,
                    )
                ),
                dict(
                    esm=dict(
                        config=True,
                    )
                ),
                dict(exception=4099),
                dict(facility="local5"),
                dict(
                    filter=[
                        dict(
                            url="tftp://10.0.2.18/ESM/elate.tcl",
                            args="TESTInst2",
                        ),
                        dict(
                            url="tftp://10.0.2.14/ESM/escalate.tcl",
                            args="TESTInst",
                        ),
                    ]
                ),
                dict(
                    history=dict(
                        severity="alerts",
                    )
                ),
                dict(
                    hosts=[
                        dict(
                            hostname="10.0.1.1",
                        ),
                        dict(
                            hostname="10.0.1.11",
                            xml=True,
                        ),
                        dict(
                            hostname="10.0.1.25",
                            filtered=True,
                        ),
                        dict(
                            hostname="10.0.1.10",
                            stream=10,
                            filtered=True,
                        ),
                        dict(
                            hostname="10.0.1.13",
                            transport=dict(
                                tcp=dict(
                                    port=514,
                                ),
                            )
                        ),
                    ]
                ),
                dict(message_counter=["log","debug",]),
                dict(
                    monitor=dict(
                        severity="warnings",
                    )
                ),
                dict(
                    origin_id=dict(
                        tag="hostname",
                    )
                ),
                dict(
                    persistent=dict(
                        batch=4444,
                    )
                ),
                dict(
                    policy_firewall=dict(
                        rate_limit=10,
                    )
                ),
                dict(
                    queue_limit=dict(
                        esm=150,
                    ),
                ),
                dict(
                    rate_limit=dict(
                        all=True,
                        size=2,
                        except_severity="warnings",
                    )
                ),
                dict(
                    reload=dict(
                        severity="alerts",
                    ),
                ),
                dict(server_arp=True),
                dict(snmp_trap=["errors",]),
                dict(
                    source_interface=[
                        dict(
                            interface="GBit1/0",
                        ),
                        dict(
                            interface="CTunnel2",
                        ),
                    ]
                ),
                dict(trap="errors"),
                dict(userinfo=True),
            ]
        )
        merged = []
        mergedX = [
            "logging on",
            "logging buffered xml 5099 notifications",
            "logging buginf",
            "logging cns-events warnings",
            "logging console xml critical",
            "logging count",
            "logging delimiter tcp",
            "logging discriminator msglog01 severity includes 5",
            "logging dmvpn rate-limit 10",
            "logging esm config",
            "logging exception 4099",
            "logging facility local5",
            "logging filter tftp://10.0.2.18/ESM/elate.tcl args TESTInst2",
            "logging filter tftp://10.0.2.14/ESM/escalate.tcl args TESTInst",
            "logging history alerts",
            "logging host 10.0.1.1",
            "logging host 10.0.1.11 xml",
            "logging host 10.0.1.25 filtered",
            "logging host 10.0.1.10 filtered stream 10",
            "logging host 10.0.1.13 transport tcp port 514",
            "logging message-counter log",
            "logging message-counter debug",
            "logging monitor warnings",
            "logging origin-id hostname",
            "logging persistent batch 4444",
            "logging policy-firewall rate-limit 10",
            "logging queue-limit esm 150",
            "logging rate-limit all 2",
            "logging reload alerts",
            "logging server-arp",
            "logging snmp-trap errors",
            "logging source-interface GBit1/0",
            "logging source-interface CTunnel2",
            "logging trap errors",
            "logging userinfo",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(merged))
        
    def test_ios_logging_global_merged_2(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            logging buginf
            logging userinfo
            logging esm config
            logging server-arp
            logging trap errors
            logging delimiter tcp
            logging reload alerts
            logging host 10.0.1.1
            logging exception 4099
            logging history alerts
            logging facility local5
            logging snmp-trap errors
            logging monitor warnings
            logging origin-id hostname
            logging host 10.0.1.11 xml
            logging cns-events warnings
            logging queue-limit esm 150
            logging dmvpn rate-limit 10
            logging message-counter log
            logging console xml critical
            logging message-counter debug
            logging persistent batch 4444
            logging host 10.0.1.25 filtered
            logging source-interface GBit1/0
            logging source-interface CTunnel2
            logging policy-firewall rate-limit 10
            logging buffered xml 5099 notifications
            logging rate-limit all 2 except warnings
            logging host 10.0.1.10 filtered stream 10
            logging host 10.0.1.13 transport tcp port 514
            logging discriminator msglog01 severity includes 5
            logging filter tftp://10.0.2.18/ESM/elate.tcl args TESTInst2
            logging filter tftp://10.0.2.14/ESM/escalate.tcl args TESTInst
            """
        )
        playbook = dict(
            config=[
                dict(logging_on="enable"),
                dict(
                    buffered=dict(
                        size=5099,
                        severity="notifications",
                        xml=True,
                    )
                ),
                dict(buginf=True),
                dict(cns_events="warnings"),
                dict(
                    console=dict(
                        severity="critical",
                        xml=True,
                    )
                ),
                dict(count=True),
                dict(
                    delimiter=dict(
                        tcp=True,
                    )
                ),
                dict(discriminator=["msglog01 severity includes 5",]),
                dict(
                    dmvpn=dict(
                        rate_limit=10,
                    )
                ),
                dict(
                    esm=dict(
                        config=True,
                    )
                ),
                dict(exception=4099),
                dict(facility="local5"),
                dict(
                    filter=[
                        dict(
                            url="tftp://10.0.2.18/ESM/elate.tcl",
                            args="TESTInst2",
                        ),
                        dict(
                            url="tftp://10.0.2.14/ESM/escalate.tcl",
                            args="TESTInst",
                        ),
                    ]
                ),
                dict(
                    history=dict(
                        severity="alerts",
                    )
                ),
                dict(
                    hosts=[
                        dict(
                            hostname="10.0.1.1",
                        ),
                        dict(
                            hostname="10.0.1.11",
                            xml=True,
                        ),
                        dict(
                            hostname="10.0.1.25",
                            filtered=True,
                        ),
                        dict(
                            hostname="10.0.1.10",
                            stream=10,
                            filtered=True,
                        ),
                        dict(
                            hostname="10.0.1.13",
                            transport=dict(
                                tcp=dict(
                                    port=514,
                                ),
                            )
                        ),
                    ]
                ),
                dict(message_counter=["log","debug",]),
                dict(
                    monitor=dict(
                        severity="warnings",
                    )
                ),
                dict(
                    origin_id=dict(
                        tag="hostname",
                    )
                ),
                dict(
                    persistent=dict(
                        batch=4444,
                    )
                ),
                dict(
                    policy_firewall=dict(
                        rate_limit=10,
                    )
                ),
                dict(
                    queue_limit=dict(
                        esm=150,
                    ),
                ),
                dict(
                    rate_limit=dict(
                        all=True,
                        size=2,
                        except_severity="warnings",
                    )
                ),
                dict(
                    reload=dict(
                        severity="alerts",
                    ),
                ),
                dict(server_arp=True),
                dict(snmp_trap=["errors",]),
                dict(
                    source_interface=[
                        dict(
                            interface="GBit1/0",
                        ),
                        dict(
                            interface="CTunnel2",
                        ),
                    ]
                ),
                dict(trap="errors"),
                dict(userinfo=True),
            ]
        )
        merged = [
            "logging on",
            "logging buffered xml 5099 notifications",
            "logging buginf",
            "logging cns-events warnings",
            "logging console xml critical",
            "logging count",
            "logging delimiter tcp",
            "logging discriminator msglog01 severity includes 5",
            "logging dmvpn rate-limit 10",
            "logging esm config",
            "logging exception 4099",
            "logging facility local5",
            "logging filter tftp://10.0.2.18/ESM/elate.tcl args TESTInst2",
            "logging filter tftp://10.0.2.14/ESM/escalate.tcl args TESTInst",
            "logging history alerts",
            "logging host 10.0.1.1",
            "logging host 10.0.1.11 xml",
            "logging host 10.0.1.25 filtered",
            "logging host 10.0.1.10 filtered stream 10",
            "logging host 10.0.1.13 transport tcp port 514",
            "logging message-counter log",
            "logging message-counter debug",
            "logging monitor warnings",
            "logging origin-id hostname",
            "logging persistent batch 4444",
            "logging policy-firewall rate-limit 10",
            "logging queue-limit esm 150",
            "logging rate-limit all 2 except warnings",
            "logging reload alerts",
            "logging server-arp",
            "logging snmp-trap errors",
            "logging source-interface GBit1/0",
            "logging source-interface CTunnel2",
            "logging trap errors",
            "logging userinfo",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module()

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(merged))
        
    def test_ios_logging_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            logging on
            logging count
            """
        )
        playbook = dict(
            config=[
                dict(logging_on="enable"),
                dict(count=True),
            ]
        )
        deleted = [
            "no logging on",
            "no logging count",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)

        self.maxDiff = None
        self.assertEqual(sorted(result["commands"]), sorted(deleted))
