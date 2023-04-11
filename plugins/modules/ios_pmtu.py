#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = """
module: ios_pmtu
short_description: Finds Path MTU (PMTU) from Cisco IOS network devices
description:
- Tests reachability using ping from Cisco IOS device to a remote destination.
- To find path MTU the binary search algorithm is used.
- The range of search of PMTU is between ( max_size - max_range) and ( max_size ).
author:
- Vladimir Krapovnitskiy (@vovilla)
options:
  dest:
    description:
    - The IP Address or hostname of the remote node.
    required: true
    type: str
  max_size:
    description:
    - Max size of packets to send.
    type: int
  max_range:
    description:
    - Range of pmtu to check (power of 2).
    type: int
  source:
    description:
    - The source IP Address or interface.
    type: str
  vrf:
    description:
    - The VRF to use for forwarding.
    type: str
"""
EXAMPLES = """
- name: Test reachability to 10.10.10.10 using default vrf
  cisco.ios.ios_pmtu:
    dest: 10.10.10.10

- name: Test reachability to 10.20.20.20 using NOC vrf
  cisco.ios.ios_pmtu:
    dest: 10.20.20.20
    vrf: NOC

- name: Test reachability to 10.40.40.40 using NOC vrf and setting source
  cisco.ios.ios_pmtu:
    dest: 10.40.40.40
    source: Loopback 0
    vrf: NOC
"""
RETURN = """
pmtu:
  description: Show the pmtu.
  returned: always
  type: int
  sample: 1600
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import (
    run_commands,
)
import re


def do_ping(module, ping_params):
    commands = [build_ping(ping_params)]
    ping_results = run_commands(module, commands=commands)
    ping_results_list = ping_results[0].split("\n")
    stats = ""
    for line in ping_results_list:
        if line.startswith("Success"):
            stats = line
    success = parse_ping(stats)
    loss = abs(100 - int(success))
    return loss


def build_ping(ping_params):
    """
    Function to build the command to send to the terminal to execute.
    All args come from the module's unique params.
    """
    vrf = ping_params["vrf"]
    dest = ping_params["dest"]
    repeat = ping_params["repeat"]
    size = ping_params["size"]
    df_bit = ping_params["df_bit"]
    source = ping_params["source"]

    if vrf is not None:
        cmd = f"ping vrf {vrf} {dest}"
    else:
        cmd = f"ping {dest}"
    if repeat is not None:
        cmd += f" repeat {repeat}"
    if size is not None:
        cmd += f" size {size}"
    if df_bit:
        cmd += " df-bit"
    if source is not None:
        cmd += f" source {source}"
    return cmd


def parse_ping(ping_stats):
    rate_re = re.compile(
        "^\\w+\\s+\\w+\\s+\\w+\\s+(?P<pct>\\d+)\\s+\\w+\\s+\\((?P<rx>\\d+)/(?P<tx>\\d+)\\)"
    )
    rate = rate_re.match(ping_stats)
    return rate.group("pct")


def main():

    # Constants for MTU size
    ETH_MIN_MTU_SIZE = 64
    # Fragmentation and Reassembly.
    ETH_MAX_MTU_SIZE = 9000  # Size of inet header's total length field is

    # Choices for max_size
    MAX_RANGE_CHOICES = [0] + list(map(lambda x: 2**x, range(1, 14)))

    # Create the module instance.
    argument_spec = dict(
        dest=dict(type="str", required=True),
        max_size=dict(type="int", required=False, default=1600),
        max_range=dict(
            type="int", required=False, choices=MAX_RANGE_CHOICES, default=512
        ),
        source=dict(type="str", required=False, default=None),
        vrf=dict(type="str", required=False, default=None),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    ping_params = dict(module.params)
    ping_params["repeat"] = 5
    results = {}

    # max_size must be between ETH_MIN_MTU_SIZE and ETH_MAX_MTU_SIZE
    if (
        ping_params["max_size"] < ETH_MIN_MTU_SIZE
        or ping_params["max_size"] > ETH_MAX_MTU_SIZE
    ):
        module.fail_json(
            msg=f"The value of the max_size option({ping_params['max_size']}) "
            f"must be between {ETH_MIN_MTU_SIZE} and {ETH_MAX_MTU_SIZE}.",
            **results,
        )

    # Set initial results values. Assume failure until we know it's success.
    results = {"changed": False, "failed": True, "pmtu": 0}

    # Execute a minimally-sized ping just to verify basic connectivity.
    ping_params["size"] = ETH_MIN_MTU_SIZE
    ping_params["df_bit"] = False

    loss = do_ping(module, ping_params)
    if loss == 100:
        module.fail_json(
            msg=f"Basic connectivity to {ping_params['dest']} failed.", **results
        )

    # Initialize test_size and step
    test_size = ping_params["max_size"]
    step = ping_params["max_range"]
    min_test_size = test_size - (ping_params["max_range"] - 1)
    if min_test_size < ETH_MIN_MTU_SIZE:
        min_test_size = ETH_MIN_MTU_SIZE
    ping_params["df_bit"] = True
    while True:
        if test_size < ETH_MIN_MTU_SIZE:
            test_size = ETH_MIN_MTU_SIZE
        if test_size > ping_params["max_size"]:
            test_size = ping_params["max_size"]
        step = step // 2 if step >= 2 else 0
        ping_params["size"] = str(test_size)
        loss = do_ping(module, ping_params)
        if loss < 100 and test_size == ping_params["max_size"]:
            # ping success with max test_size, save and break
            results["failed"] = False
            results["pmtu"] = test_size
            break
        elif loss < 100:
            # ping success, increase test_size
            results["failed"] = False
            results["pmtu"] = test_size
            test_size += step
        else:
            # ping fail, lower size
            test_size -= step
        if step < 1:
            break

    if results.get("pmtu", 0) == 0:
        module.fail_json(
            msg=f"The MTU of the path to {ping_params['dest']} is less than "
            f"the minimum tested size({min_test_size}). Try "
            f"decreasing max_size({ping_params['max_size']}) or increasing "
            f"max_range({ping_params['max_range']}).",
            **results,
        )

    # Return results.
    module.exit_json(**results)


if __name__ == "__main__":
    main()