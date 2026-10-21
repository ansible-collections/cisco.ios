# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Flow_monitor parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Flow_monitorTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Flow_monitorTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        # ── flow record block ───────────────────────────────────────────
        {
            "name": "flow_record",
            "getval": re.compile(r"^flow record (?P<name>\S+)$"),
            "setval": "flow record {{ name }}",
            "result": {"records": {"{{ name }}": {"name": "{{ name }}"}}},
            "shared": True,
        },
        {
            "name": "flow_record.match.ipv4_tos",
            "getval": re.compile(r"^\s+match ipv4 tos$"),
            "setval": " match ipv4 tos",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_tos": True}}}},
        },
        {
            "name": "flow_record.match.ipv4_protocol",
            "getval": re.compile(r"^\s+match ipv4 protocol$"),
            "setval": " match ipv4 protocol",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_protocol": True}}}},
        },
        {
            "name": "flow_record.match.ipv4_source_address",
            "getval": re.compile(r"^\s+match ipv4 source address$"),
            "setval": " match ipv4 source address",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_source_address": True}}}},
        },
        {
            "name": "flow_record.match.ipv4_destination_address",
            "getval": re.compile(r"^\s+match ipv4 destination address$"),
            "setval": " match ipv4 destination address",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_destination_address": True}}}},
        },
        {
            "name": "flow_record.match.transport_source_port",
            "getval": re.compile(r"^\s+match transport source-port$"),
            "setval": " match transport source-port",
            "result": {"records": {"{{ name }}": {"match": {"transport_source_port": True}}}},
        },
        {
            "name": "flow_record.match.transport_destination_port",
            "getval": re.compile(r"^\s+match transport destination-port$"),
            "setval": " match transport destination-port",
            "result": {"records": {"{{ name }}": {"match": {"transport_destination_port": True}}}},
        },
        {
            "name": "flow_record.match.flow_direction",
            "getval": re.compile(r"^\s+match flow direction$"),
            "setval": " match flow direction",
            "result": {"records": {"{{ name }}": {"match": {"flow_direction": True}}}},
        },
        {
            "name": "flow_record.match.interface_input",
            "getval": re.compile(r"^\s+match interface input$"),
            "setval": " match interface input",
            "result": {"records": {"{{ name }}": {"match": {"interface_input": True}}}},
        },
        {
            "name": "flow_record.match.interface_output",
            "getval": re.compile(r"^\s+match interface output$"),
            "setval": " match interface output",
            "result": {"records": {"{{ name }}": {"match": {"interface_output": True}}}},
        },
        {
            "name": "flow_record.match.routing_vrf_input",
            "getval": re.compile(r"^\s+match routing vrf input$"),
            "setval": " match routing vrf input",
            "result": {"records": {"{{ name }}": {"match": {"routing_vrf_input": True}}}},
        },
        # ── flow record match additions ──────────────────────────────────
        {
            "name": "flow_record.match.ipv4_ttl",
            "getval": re.compile(r"^\s+match ipv4 ttl$"),
            "setval": " match ipv4 ttl",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_ttl": True}}}},
        },
        {
            "name": "flow_record.match.ipv4_version",
            "getval": re.compile(r"^\s+match ipv4 version$"),
            "setval": " match ipv4 version",
            "result": {"records": {"{{ name }}": {"match": {"ipv4_version": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_source_address",
            "getval": re.compile(r"^\s+match ipv6 source address$"),
            "setval": " match ipv6 source address",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_source_address": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_destination_address",
            "getval": re.compile(r"^\s+match ipv6 destination address$"),
            "setval": " match ipv6 destination address",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_destination_address": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_hop_limit",
            "getval": re.compile(r"^\s+match ipv6 hop-limit$"),
            "setval": " match ipv6 hop-limit",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_hop_limit": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_protocol",
            "getval": re.compile(r"^\s+match ipv6 protocol$"),
            "setval": " match ipv6 protocol",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_protocol": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_traffic_class",
            "getval": re.compile(r"^\s+match ipv6 traffic-class$"),
            "setval": " match ipv6 traffic-class",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_traffic_class": True}}}},
        },
        {
            "name": "flow_record.match.ipv6_version",
            "getval": re.compile(r"^\s+match ipv6 version$"),
            "setval": " match ipv6 version",
            "result": {"records": {"{{ name }}": {"match": {"ipv6_version": True}}}},
        },
        {
            "name": "flow_record.match.transport_icmp_ipv4_code",
            "getval": re.compile(r"^\s+match transport icmp ipv4 code$"),
            "setval": " match transport icmp ipv4 code",
            "result": {"records": {"{{ name }}": {"match": {"transport_icmp_ipv4_code": True}}}},
        },
        {
            "name": "flow_record.match.transport_icmp_ipv4_type",
            "getval": re.compile(r"^\s+match transport icmp ipv4 type$"),
            "setval": " match transport icmp ipv4 type",
            "result": {"records": {"{{ name }}": {"match": {"transport_icmp_ipv4_type": True}}}},
        },
        {
            "name": "flow_record.match.transport_icmp_ipv6_code",
            "getval": re.compile(r"^\s+match transport icmp ipv6 code$"),
            "setval": " match transport icmp ipv6 code",
            "result": {"records": {"{{ name }}": {"match": {"transport_icmp_ipv6_code": True}}}},
        },
        {
            "name": "flow_record.match.transport_icmp_ipv6_type",
            "getval": re.compile(r"^\s+match transport icmp ipv6 type$"),
            "setval": " match transport icmp ipv6 type",
            "result": {"records": {"{{ name }}": {"match": {"transport_icmp_ipv6_type": True}}}},
        },
        {
            "name": "flow_record.match.datalink_dot1q_priority",
            "getval": re.compile(r"^\s+match datalink dot1q priority$"),
            "setval": " match datalink dot1q priority",
            "result": {"records": {"{{ name }}": {"match": {"datalink_dot1q_priority": True}}}},
        },
        {
            "name": "flow_record.match.datalink_dot1q_vlan_input",
            "getval": re.compile(r"^\s+match datalink dot1q vlan input$"),
            "setval": " match datalink dot1q vlan input",
            "result": {"records": {"{{ name }}": {"match": {"datalink_dot1q_vlan_input": True}}}},
        },
        {
            "name": "flow_record.match.datalink_dot1q_vlan_output",
            "getval": re.compile(r"^\s+match datalink dot1q vlan output$"),
            "setval": " match datalink dot1q vlan output",
            "result": {"records": {"{{ name }}": {"match": {"datalink_dot1q_vlan_output": True}}}},
        },
        {
            "name": "flow_record.match.datalink_ethertype",
            "getval": re.compile(r"^\s+match datalink ethertype$"),
            "setval": " match datalink ethertype",
            "result": {"records": {"{{ name }}": {"match": {"datalink_ethertype": True}}}},
        },
        {
            "name": "flow_record.match.datalink_mac_destination_input",
            "getval": re.compile(r"^\s+match datalink mac destination address input$"),
            "setval": " match datalink mac destination address input",
            "result": {"records": {"{{ name }}": {"match": {"datalink_mac_destination_input": True}}}},
        },
        {
            "name": "flow_record.match.datalink_mac_destination_output",
            "getval": re.compile(r"^\s+match datalink mac destination address output$"),
            "setval": " match datalink mac destination address output",
            "result": {"records": {"{{ name }}": {"match": {"datalink_mac_destination_output": True}}}},
        },
        {
            "name": "flow_record.match.datalink_mac_source_input",
            "getval": re.compile(r"^\s+match datalink mac source address input$"),
            "setval": " match datalink mac source address input",
            "result": {"records": {"{{ name }}": {"match": {"datalink_mac_source_input": True}}}},
        },
        {
            "name": "flow_record.match.datalink_mac_source_output",
            "getval": re.compile(r"^\s+match datalink mac source address output$"),
            "setval": " match datalink mac source address output",
            "result": {"records": {"{{ name }}": {"match": {"datalink_mac_source_output": True}}}},
        },
        {
            "name": "flow_record.match.datalink_vlan_input",
            "getval": re.compile(r"^\s+match datalink vlan input$"),
            "setval": " match datalink vlan input",
            "result": {"records": {"{{ name }}": {"match": {"datalink_vlan_input": True}}}},
        },
        {
            "name": "flow_record.match.datalink_vlan_output",
            "getval": re.compile(r"^\s+match datalink vlan output$"),
            "setval": " match datalink vlan output",
            "result": {"records": {"{{ name }}": {"match": {"datalink_vlan_output": True}}}},
        },
        {
            "name": "flow_record.match.application_name",
            "getval": re.compile(r"^\s+match application name$"),
            "setval": " match application name",
            "result": {"records": {"{{ name }}": {"match": {"application_name": True}}}},
        },
        # ── flow record collect additions ────────────────────────────────
        {
            "name": "flow_record.collect.routing_source_as_peer",
            "getval": re.compile(r"^\s+collect routing source as peer$"),
            "setval": " collect routing source as peer",
            "result": {"records": {"{{ name }}": {"collect": {"routing_source_as_peer": True}}}},
        },
        {
            "name": "flow_record.collect.routing_destination_as_peer",
            "getval": re.compile(r"^\s+collect routing destination as peer$"),
            "setval": " collect routing destination as peer",
            "result": {"records": {"{{ name }}": {"collect": {"routing_destination_as_peer": True}}}},
        },
        {
            "name": "flow_record.collect.routing_next_hop_ipv6",
            "getval": re.compile(r"^\s+collect routing next-hop address ipv6$"),
            "setval": " collect routing next-hop address ipv6",
            "result": {"records": {"{{ name }}": {"collect": {"routing_next_hop_ipv6": True}}}},
        },
        {
            "name": "flow_record.collect.counter_bytes_long",
            "getval": re.compile(r"^\s+collect counter bytes long$"),
            "setval": " collect counter bytes long",
            "result": {"records": {"{{ name }}": {"collect": {"counter_bytes_long": True}}}},
        },
        {
            "name": "flow_record.collect.counter_bytes_layer2",
            "getval": re.compile(r"^\s+collect counter bytes layer2$"),
            "setval": " collect counter bytes layer2",
            "result": {"records": {"{{ name }}": {"collect": {"counter_bytes_layer2": True}}}},
        },
        {
            "name": "flow_record.collect.counter_packets_long",
            "getval": re.compile(r"^\s+collect counter packets long$"),
            "setval": " collect counter packets long",
            "result": {"records": {"{{ name }}": {"collect": {"counter_packets_long": True}}}},
        },
        {
            "name": "flow_record.collect.timestamp_absolute_first",
            "getval": re.compile(r"^\s+collect timestamp absolute first$"),
            "setval": " collect timestamp absolute first",
            "result": {"records": {"{{ name }}": {"collect": {"timestamp_absolute_first": True}}}},
        },
        {
            "name": "flow_record.collect.timestamp_absolute_last",
            "getval": re.compile(r"^\s+collect timestamp absolute last$"),
            "setval": " collect timestamp absolute last",
            "result": {"records": {"{{ name }}": {"collect": {"timestamp_absolute_last": True}}}},
        },
        {
            "name": "flow_record.collect.transport_destination_port",
            "getval": re.compile(r"^\s+collect transport destination-port$"),
            "setval": " collect transport destination-port",
            "result": {"records": {"{{ name }}": {"collect": {"transport_destination_port": True}}}},
        },
        {
            "name": "flow_record.collect.transport_source_port",
            "getval": re.compile(r"^\s+collect transport source-port$"),
            "setval": " collect transport source-port",
            "result": {"records": {"{{ name }}": {"collect": {"transport_source_port": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_source_address",
            "getval": re.compile(r"^\s+collect ipv4 source address$"),
            "setval": " collect ipv4 source address",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_source_address": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_source_mask",
            "getval": re.compile(r"^\s+collect ipv4 source mask$"),
            "setval": " collect ipv4 source mask",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_source_mask": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_source_prefix",
            "getval": re.compile(r"^\s+collect ipv4 source prefix$"),
            "setval": " collect ipv4 source prefix",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_source_prefix": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_destination_address",
            "getval": re.compile(r"^\s+collect ipv4 destination address$"),
            "setval": " collect ipv4 destination address",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_destination_address": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_destination_mask",
            "getval": re.compile(r"^\s+collect ipv4 destination mask$"),
            "setval": " collect ipv4 destination mask",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_destination_mask": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_destination_prefix",
            "getval": re.compile(r"^\s+collect ipv4 destination prefix$"),
            "setval": " collect ipv4 destination prefix",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_destination_prefix": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_protocol",
            "getval": re.compile(r"^\s+collect ipv4 protocol$"),
            "setval": " collect ipv4 protocol",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_protocol": True}}}},
        },
        {
            "name": "flow_record.collect.ipv4_version",
            "getval": re.compile(r"^\s+collect ipv4 version$"),
            "setval": " collect ipv4 version",
            "result": {"records": {"{{ name }}": {"collect": {"ipv4_version": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_source_address",
            "getval": re.compile(r"^\s+collect ipv6 source address$"),
            "setval": " collect ipv6 source address",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_source_address": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_source_mask",
            "getval": re.compile(r"^\s+collect ipv6 source mask$"),
            "setval": " collect ipv6 source mask",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_source_mask": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_source_prefix",
            "getval": re.compile(r"^\s+collect ipv6 source prefix$"),
            "setval": " collect ipv6 source prefix",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_source_prefix": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_destination_address",
            "getval": re.compile(r"^\s+collect ipv6 destination address$"),
            "setval": " collect ipv6 destination address",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_destination_address": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_destination_mask",
            "getval": re.compile(r"^\s+collect ipv6 destination mask$"),
            "setval": " collect ipv6 destination mask",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_destination_mask": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_destination_prefix",
            "getval": re.compile(r"^\s+collect ipv6 destination prefix$"),
            "setval": " collect ipv6 destination prefix",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_destination_prefix": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_protocol",
            "getval": re.compile(r"^\s+collect ipv6 protocol$"),
            "setval": " collect ipv6 protocol",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_protocol": True}}}},
        },
        {
            "name": "flow_record.collect.ipv6_version",
            "getval": re.compile(r"^\s+collect ipv6 version$"),
            "setval": " collect ipv6 version",
            "result": {"records": {"{{ name }}": {"collect": {"ipv6_version": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_dot1q_vlan_input",
            "getval": re.compile(r"^\s+collect datalink dot1q vlan input$"),
            "setval": " collect datalink dot1q vlan input",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_dot1q_vlan_input": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_dot1q_vlan_output",
            "getval": re.compile(r"^\s+collect datalink dot1q vlan output$"),
            "setval": " collect datalink dot1q vlan output",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_dot1q_vlan_output": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_mac_destination_input",
            "getval": re.compile(r"^\s+collect datalink mac destination address input$"),
            "setval": " collect datalink mac destination address input",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_mac_destination_input": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_mac_destination_output",
            "getval": re.compile(r"^\s+collect datalink mac destination address output$"),
            "setval": " collect datalink mac destination address output",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_mac_destination_output": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_mac_source_input",
            "getval": re.compile(r"^\s+collect datalink mac source address input$"),
            "setval": " collect datalink mac source address input",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_mac_source_input": True}}}},
        },
        {
            "name": "flow_record.collect.datalink_mac_source_output",
            "getval": re.compile(r"^\s+collect datalink mac source address output$"),
            "setval": " collect datalink mac source address output",
            "result": {"records": {"{{ name }}": {"collect": {"datalink_mac_source_output": True}}}},
        },
        {
            "name": "flow_record.collect.flow_sampler",
            "getval": re.compile(r"^\s+collect flow sampler$"),
            "setval": " collect flow sampler",
            "result": {"records": {"{{ name }}": {"collect": {"flow_sampler": True}}}},
        },
        {
            "name": "flow_record.collect.routing_source_as_4octet",
            "getval": re.compile(r"^\s+collect routing source as 4-octet$"),
            "setval": " collect routing source as 4-octet",
            "result": {"records": {"{{ name }}": {"collect": {"routing_source_as_4octet": True}}}},
        },
        {
            "name": "flow_record.collect.routing_destination_as_4octet",
            "getval": re.compile(r"^\s+collect routing destination as 4-octet$"),
            "setval": " collect routing destination as 4-octet",
            "result": {"records": {"{{ name }}": {"collect": {"routing_destination_as_4octet": True}}}},
        },
        {
            "name": "flow_record.collect.routing_next_hop_ipv4",
            "getval": re.compile(r"^\s+collect routing next-hop address ipv4$"),
            "setval": " collect routing next-hop address ipv4",
            "result": {"records": {"{{ name }}": {"collect": {"routing_next_hop_ipv4": True}}}},
        },
        {
            "name": "flow_record.collect.transport_tcp_flags",
            "getval": re.compile(r"^\s+collect transport tcp flags$"),
            "setval": " collect transport tcp flags",
            "result": {"records": {"{{ name }}": {"collect": {"transport_tcp_flags": True}}}},
        },
        {
            "name": "flow_record.collect.timestamp_sys_uptime_first",
            "getval": re.compile(r"^\s+collect timestamp sys-uptime first$"),
            "setval": " collect timestamp sys-uptime first",
            "result": {"records": {"{{ name }}": {"collect": {"timestamp_sys_uptime_first": True}}}},
        },
        {
            "name": "flow_record.collect.timestamp_sys_uptime_last",
            "getval": re.compile(r"^\s+collect timestamp sys-uptime last$"),
            "setval": " collect timestamp sys-uptime last",
            "result": {"records": {"{{ name }}": {"collect": {"timestamp_sys_uptime_last": True}}}},
        },
        {
            "name": "flow_record.collect.interface_input",
            "getval": re.compile(r"^\s+collect interface input$"),
            "setval": " collect interface input",
            "result": {"records": {"{{ name }}": {"collect": {"interface_input": True}}}},
        },
        {
            "name": "flow_record.collect.interface_output",
            "getval": re.compile(r"^\s+collect interface output$"),
            "setval": " collect interface output",
            "result": {"records": {"{{ name }}": {"collect": {"interface_output": True}}}},
        },
        # ── flow exporter block ──────────────────────────────────────────
        {
            "name": "flow_exporter",
            "getval": re.compile(r"^flow exporter (?P<name>\S+)$"),
            "setval": "flow exporter {{ name }}",
            "result": {"exporters": {"{{ name }}": {"name": "{{ name }}"}}},
            "shared": True,
        },
        {
            "name": "flow_exporter.destination",
            "getval": re.compile(
                r"^\s+destination (?P<destination>\S+)"
                r"(?:\s+vrf (?P<vrf>\S+))?$",
            ),
            "setval": " destination {{ destination }}"
                      "{{ (' vrf ' + vrf) if vrf is defined else '' }}",
            "result": {
                "exporters": {
                    "{{ name }}": {
                        "destination": "{{ destination }}",
                        "vrf": "{{ vrf }}",
                    },
                },
            },
        },
        {
            "name": "flow_exporter.source",
            "getval": re.compile(r"^\s+source (?P<source>\S+)$"),
            "setval": " source {{ source }}",
            "result": {"exporters": {"{{ name }}": {"source": "{{ source }}"}}},
        },
        {
            "name": "flow_exporter.transport",
            "getval": re.compile(
                r"^\s+transport (?P<protocol>udp|tcp) (?P<port>\d+)$",
            ),
            "setval": " transport {{ transport.protocol }} {{ transport.port }}",
            "result": {
                "exporters": {
                    "{{ name }}": {
                        "transport": {
                            "protocol": "{{ protocol }}",
                            "port": "{{ port | int }}",
                        },
                    },
                },
            },
        },
        {
            "name": "flow_exporter.options.sampler_table_timeout",
            "getval": re.compile(
                r"^\s+option sampler-table timeout (?P<sampler_table_timeout>\d+)$",
            ),
            "setval": " option sampler-table timeout {{ options.sampler_table_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {
                        "options": {"sampler_table_timeout": "{{ sampler_table_timeout | int }}"},
                    },
                },
            },
        },
        {
            "name": "flow_exporter.options.template_data_timeout",
            "getval": re.compile(
                r"^\s+option template data timeout (?P<template_data_timeout>\d+)$",
            ),
            "setval": " option template data timeout {{ options.template_data_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {
                        "options": {"template_data_timeout": "{{ template_data_timeout | int }}"},
                    },
                },
            },
        },
        # ── flow exporter additions ──────────────────────────────────────
        {
            "name": "flow_exporter.description",
            "getval": re.compile(r"^\s+description (?P<description>.+)$"),
            "setval": " description {{ description }}",
            "result": {"exporters": {"{{ name }}": {"description": "{{ description }}"}}},
        },
        {
            "name": "flow_exporter.export_protocol",
            "getval": re.compile(r"^\s+export-protocol (?P<export_protocol>\S+)$"),
            "setval": " export-protocol {{ export_protocol }}",
            "result": {"exporters": {"{{ name }}": {"export_protocol": "{{ export_protocol }}"}}},
        },
        {
            "name": "flow_exporter.template_data_timeout",
            "getval": re.compile(r"^\s+template data timeout (?P<template_data_timeout>\d+)$"),
            "setval": " template data timeout {{ template_data_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {"template_data_timeout": "{{ template_data_timeout | int }}"},
                },
            },
        },
        {
            "name": "flow_exporter.ttl",
            "getval": re.compile(r"^\s+ttl (?P<ttl>\d+)$"),
            "setval": " ttl {{ ttl }}",
            "result": {"exporters": {"{{ name }}": {"ttl": "{{ ttl | int }}"}}},
        },
        {
            "name": "flow_exporter.dscp",
            "getval": re.compile(r"^\s+dscp (?P<dscp>\d+)$"),
            "setval": " dscp {{ dscp }}",
            "result": {"exporters": {"{{ name }}": {"dscp": "{{ dscp | int }}"}}},
        },
        {
            "name": "flow_exporter.options.interface_table_timeout",
            "getval": re.compile(r"^\s+option interface-table timeout (?P<timeout>\d+)$"),
            "setval": " option interface-table timeout {{ options.interface_table_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {"options": {"interface_table_timeout": "{{ timeout | int }}"}},
                },
            },
        },
        {
            "name": "flow_exporter.options.exporter_stats_timeout",
            "getval": re.compile(r"^\s+option exporter-stats timeout (?P<timeout>\d+)$"),
            "setval": " option exporter-stats timeout {{ options.exporter_stats_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {"options": {"exporter_stats_timeout": "{{ timeout | int }}"}},
                },
            },
        },
        {
            "name": "flow_exporter.options.application_table_timeout",
            "getval": re.compile(r"^\s+option application-table timeout (?P<timeout>\d+)$"),
            "setval": " option application-table timeout {{ options.application_table_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {"options": {"application_table_timeout": "{{ timeout | int }}"}},
                },
            },
        },
        {
            "name": "flow_exporter.options.vrf_table_timeout",
            "getval": re.compile(r"^\s+option vrf-table timeout (?P<timeout>\d+)$"),
            "setval": " option vrf-table timeout {{ options.vrf_table_timeout }}",
            "result": {
                "exporters": {
                    "{{ name }}": {"options": {"vrf_table_timeout": "{{ timeout | int }}"}},
                },
            },
        },
        # ── sampler additions ────────────────────────────────────────────
        {
            "name": "sampler.description",
            "getval": re.compile(r"^\s+description (?P<description>.+)$"),
            "setval": " description {{ description }}",
            "result": {"samplers": {"{{ name }}": {"description": "{{ description }}"}}},
        },
        # ── flow monitor additions ───────────────────────────────────────
        {
            "name": "flow_monitor.description",
            "getval": re.compile(r"^\s+description (?P<description>.+)$"),
            "setval": " description {{ description }}",
            "result": {"monitors": {"{{ name }}": {"description": "{{ description }}"}}},
        },
        {
            "name": "flow_monitor.cache.type",
            "getval": re.compile(r"^\s+cache type (?P<cache_type>\S+)$"),
            "setval": " cache type {{ cache.type }}",
            "result": {
                "monitors": {"{{ name }}": {"cache": {"type": "{{ cache_type }}"}}},
            },
        },
        {
            "name": "flow_monitor.cache.entries",
            "getval": re.compile(r"^\s+cache entries (?P<entries>\d+)$"),
            "setval": " cache entries {{ cache.entries }}",
            "result": {
                "monitors": {"{{ name }}": {"cache": {"entries": "{{ entries | int }}"}}},
            },
        },
        {
            "name": "flow_monitor.cache.timeout_update",
            "getval": re.compile(r"^\s+cache timeout update (?P<timeout_update>\d+)$"),
            "setval": " cache timeout update {{ cache.timeout_update }}",
            "result": {
                "monitors": {
                    "{{ name }}": {"cache": {"timeout_update": "{{ timeout_update | int }}"}},
                },
            },
        },
        # ── sampler block ────────────────────────────────────────────────
        {
            "name": "sampler",
            "getval": re.compile(r"^sampler (?P<name>\S+)$"),
            "setval": "sampler {{ name }}",
            "result": {"samplers": {"{{ name }}": {"name": "{{ name }}"}}},
            "shared": True,
        },
        {
            "name": "sampler.mode",
            "getval": re.compile(
                r"^\s+mode (?P<mode>random|deterministic) 1 out-of (?P<window_size>\d+)$",
            ),
            "setval": " mode {{ mode }} 1 out-of {{ window_size }}",
            "result": {
                "samplers": {
                    "{{ name }}": {
                        "mode": "{{ mode }}",
                        "window_size": "{{ window_size | int }}",
                    },
                },
            },
        },
        # ── flow monitor block ───────────────────────────────────────────
        {
            "name": "flow_monitor",
            "getval": re.compile(r"^flow monitor (?P<name>\S+)$"),
            "setval": "flow monitor {{ name }}",
            "result": {"monitors": {"{{ name }}": {"name": "{{ name }}"}}},
            "shared": True,
        },
        {
            "name": "flow_monitor.record",
            "getval": re.compile(r"^\s+record (?P<record>\S+)$"),
            "setval": " record {{ record }}",
            "result": {"monitors": {"{{ name }}": {"record": "{{ record }}"}}},
        },
        {
            "name": "flow_monitor.cache.timeout_inactive",
            "getval": re.compile(r"^\s+cache timeout inactive (?P<timeout_inactive>\d+)$"),
            "setval": " cache timeout inactive {{ cache.timeout_inactive }}",
            "result": {
                "monitors": {
                    "{{ name }}": {
                        "cache": {"timeout_inactive": "{{ timeout_inactive | int }}"},
                    },
                },
            },
        },
        {
            "name": "flow_monitor.cache.timeout_active",
            "getval": re.compile(r"^\s+cache timeout active (?P<timeout_active>\d+)$"),
            "setval": " cache timeout active {{ cache.timeout_active }}",
            "result": {
                "monitors": {
                    "{{ name }}": {
                        "cache": {"timeout_active": "{{ timeout_active | int }}"},
                    },
                },
            },
        },
        # Note: flow monitor exporter lines are handled by the custom parser
        # in facts (multi-exporter list) and directly in config command generation.
        {
            "name": "flow_monitor.exporter",
            "getval": re.compile(r"^\s+exporter (?P<exporter_name>\S+)$"),
            "setval": " exporter {{ exporter_name }}",
            "result": {"monitors": {"{{ name }}": {"_exporter_line": "{{ exporter_name }}"}}},
        },
    ]
    # fmt: on
