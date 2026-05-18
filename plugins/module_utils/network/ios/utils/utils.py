#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# utils

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import socket

from itertools import count, groupby

from ansible.module_utils.common.network import is_masklen, to_netmask


def remove_command_from_config_list(interface, cmd, commands):
    # To delete the passed config
    if interface not in commands:
        commands.insert(0, interface)
    commands.append("no %s" % cmd)
    return commands


def add_command_to_config_list(interface, cmd, commands):
    # To set the passed config
    if interface not in commands:
        commands.insert(0, interface)
    commands.append(cmd)


def reverify_diff_py35(want, have):
    """Function to re-verify the set diff for py35 as it doesn't maintains dict order which results
        into unexpected set diff
    :param config: want and have set config
    :returns: True/False post checking if there's any actual diff b/w want and have sets
    """
    if not have:
        return True
    for each_want in want:
        diff = True
        for each_have in have:
            if each_have == sorted(each_want) or sorted(each_have) == sorted(each_want):
                diff = False
        if diff:
            return True
    return False


def check_n_return_valid_ipv6_addr(module, input_list, filtered_ipv6_list):
    # To verify the valid ipv6 address
    try:
        for each in input_list:
            if "::" in each:
                if "/" in each:
                    each = each.split("/")[0]
                if socket.inet_pton(socket.AF_INET6, each):
                    filtered_ipv6_list.append(each)
        return filtered_ipv6_list
    except socket.error:
        module.fail_json(msg="Incorrect IPV6 address!")


def new_dict_to_set(input_dict, temp_list, test_set, count=0):
    # recursive function to convert input dict to set for comparision
    test_dict = dict()
    if isinstance(input_dict, dict):
        input_dict_len = len(input_dict)
        for k, v in sorted(input_dict.items()):
            count += 1
            if isinstance(v, list):
                temp_list.append(k)
                for each in v:
                    if isinstance(each, dict):
                        if [True for i in each.values() if isinstance(i, list)]:
                            new_dict_to_set(each, temp_list, test_set, count)
                        else:
                            new_dict_to_set(each, temp_list, test_set, 0)
            else:
                if v is not None:
                    test_dict.update({k: v})
                try:
                    if tuple(test_dict.items()) not in test_set and count == input_dict_len:
                        test_set.add(tuple(test_dict.items()))
                        count = 0
                except TypeError:
                    temp_dict = {}

                    def expand_dict(dict_to_expand):
                        temp = dict()
                        for k, v in dict_to_expand.items():
                            if isinstance(v, dict):
                                expand_dict(v)
                            else:
                                if v is not None:
                                    temp.update({k: v})
                                temp_dict.update(tuple(temp.items()))

                    new_dict = {k: v}
                    expand_dict(new_dict)
                    if tuple(temp_dict.items()) not in test_set:
                        test_set.add(tuple(temp_dict.items()))
    return test_dict


def dict_to_set(sample_dict, sort_dictionary=False):
    if sort_dictionary:
        sample_dict = sort_dict(sample_dict)
    # Generate a set with passed dictionary for comparison
    test_dict = dict()
    if isinstance(sample_dict, dict):
        for k, v in sample_dict.items():
            if v is not None:
                if isinstance(v, list):
                    if isinstance(v[0], dict):
                        li = []
                        for each in v:
                            for key, value in each.items():
                                if isinstance(value, list):
                                    each[key] = tuple(value)
                            li.append(tuple(each.items()))
                        v = tuple(li)
                    else:
                        v = tuple(v)
                elif isinstance(v, dict):
                    li = []
                    for key, value in v.items():
                        if isinstance(value, list):
                            v[key] = tuple(value)
                    li.extend(tuple(v.items()))
                    v = tuple(li)
                test_dict.update({k: v})
        return_set = set(tuple(test_dict.items()))
    else:
        return_set = set(sample_dict)
    return return_set


def filter_dict_having_none_value(want, have):
    # Generate dict with have dict value which is None in want dict
    test_dict = dict()
    name = want.get("name")
    if name:
        test_dict["name"] = name
    diff_ip = False
    for k, v in want.items():
        if isinstance(v, dict):
            for key, value in v.items():
                test_key_dict = dict()
                if value is None:
                    if have.get(k):
                        dict_val = have.get(k).get(key)
                        test_key_dict.update({key: dict_val})
                elif k == "ipv6" and value.lower() != have.get(k)[0].get(key).lower():
                    # as multiple IPV6 address can be configured on same
                    # interface, for replace state in place update will
                    # actually create new entry, which isn't as expected
                    # for replace state, so in case of IPV6 address
                    # every time 1st delete the existing IPV6 config and
                    # then apply the new change
                    dict_val = have.get(k)[0].get(key)
                    test_key_dict.update({key: dict_val})
                if test_key_dict:
                    test_dict.update({k: test_key_dict})
        if isinstance(v, list):
            for key, value in v[0].items():
                test_key_dict = dict()
                if value is None:
                    if have.get(k) and key in have.get(k):
                        dict_val = have.get(k)[0].get(key)
                        test_key_dict.update({key: dict_val})
                elif have.get(k):
                    if k == "ipv6" and value.lower() != have.get(k)[0].get(key).lower():
                        dict_val = have.get(k)[0].get(key)
                        test_key_dict.update({key: dict_val})
                if test_key_dict:
                    test_dict.update({k: test_key_dict})
            # below conditions checks are added to check if
            # secondary IP is configured, if yes then delete
            # the already configured IP if want and have IP
            # is different else if it's same no need to delete
            for each in v:
                if each.get("secondary"):
                    want_ip = each.get("address").split("/")
                    have_ip = have.get("ipv4")
                    if len(want_ip) > 1 and have_ip and have_ip[0].get("secondary"):
                        have_ip = have_ip[0]["address"].split(" ")[0]
                        if have_ip != want_ip[0]:
                            diff_ip = True
                    if each.get("secondary") and diff_ip is True:
                        test_key_dict.update({"secondary": True})
                    test_dict.update({"ipv4": test_key_dict})
        if v is None:
            val = have.get(k)
            test_dict.update({k: val})
    return test_dict


def remove_duplicate_interface(commands):
    # Remove duplicate interface from commands
    set_cmd = []
    for each in commands:
        if "interface" in each:
            if each not in set_cmd:
                set_cmd.append(each)
        else:
            set_cmd.append(each)

    return set_cmd


def flatten_dict(x):
    result = {}
    if not isinstance(x, dict):
        return result

    for key, value in x.items():
        if isinstance(value, dict):
            result.update(flatten_dict(value))
        else:
            result[key] = value

    return result


def flatten_config(data, context):
    """Flatten different contexts in
        the running-config for easier parsing.
    :param data: dict
    :param context: str
    :returns: flattened running config
    """
    data = data.split("\n")
    in_cxt = False
    cur = {}

    for index, x in enumerate(data):
        cur_indent = len(x) - len(x.lstrip())
        if x.strip().startswith(context):
            in_cxt = True
            cur["context"] = x
            cur["indent"] = cur_indent
        elif cur and (cur_indent <= cur["indent"]):
            in_cxt = False
        elif in_cxt:
            data[index] = cur["context"] + " " + x.strip()
    return "\n".join(data)


def validate_ipv4(value, module):
    if value:
        address = value.split("/")
        if len(address) != 2:
            module.fail_json(
                msg="address format is <ipv4 address>/<mask>, got invalid format {0}".format(
                    value,
                ),
            )

        if not is_masklen(address[1]):
            module.fail_json(
                msg="invalid value for mask: {0}, mask should be in range 0-32".format(
                    address[1],
                ),
            )


def validate_n_expand_ipv4(module, want):
    # Check if input IPV4 is valid IP and expand IPV4 with its subnet mask
    ip_addr_want = want.get("address")
    if len(ip_addr_want.split(" ")) > 1:
        return ip_addr_want
    validate_ipv4(ip_addr_want, module)
    ip = ip_addr_want.split("/")
    if len(ip) == 2:
        ip_addr_want = "{0} {1}".format(ip[0], to_netmask(ip[1]))

    return ip_addr_want


def netmask_to_cidr(netmask):
    # convert netmask to cidr and returns the cidr notation
    return str(sum([bin(int(x)).count("1") for x in netmask.split(".")]))


def is_valid_ip(ip_str):
    valid = True
    try:
        if "::" in ip_str:
            socket.inet_pton(socket.AF_INET6, ip_str)  # for IPv6
        else:
            socket.inet_pton(socket.AF_INET, ip_str)  # for IPv4
    except socket.error:
        valid = False
    return valid


def normalize_interface(name):
    """Return the normalized interface name"""
    if not name:
        return

    def _get_number(name):
        digits = ""
        for char in name:
            if char.isdigit() or char in "/.":
                digits += char
        return digits

    if name.lower().startswith("gi"):
        if_type = "GigabitEthernet"
    elif name.lower().startswith("twe"):
        if_type = "TwentyFiveGigE"
    elif name.lower().startswith("tw"):
        if_type = "TwoGigabitEthernet"
    elif name.lower().startswith("te"):
        if_type = "TenGigabitEthernet"
    elif name.lower().startswith("fa"):
        if_type = "FastEthernet"
    elif name.lower().startswith("fourhundredgige"):
        if_type = "FourHundredGigE"
    elif name.lower().startswith("fiftygige"):
        if_type = "FiftyGigE"
    elif name.lower().startswith("fou"):
        if_type = "FourHundredGigabitEthernet"
    elif name.lower().startswith("fo"):
        if_type = "FortyGigabitEthernet"
    elif name.lower().startswith("fiv"):
        if_type = "FiveGigabitEthernet"
    elif name.lower().startswith("fif"):
        if_type = "FiftyGigabitEthernet"
    elif name.lower().startswith("long"):
        if_type = "LongReachEthernet"
    elif name.lower().startswith("et"):
        if_type = "Ethernet"
    elif name.lower().startswith("vl"):
        if_type = "Vlan"
    elif name.lower().startswith("lo"):
        if_type = "loopback"
    elif name.lower().startswith("po"):
        if_type = "Port-channel"
    elif name.lower().startswith("nv"):
        if_type = "nve"
    elif name.lower().startswith("hu"):
        if_type = "HundredGigE"
    elif name.lower().startswith("virtual-te"):
        if_type = "Virtual-Template"
    elif name.lower().startswith("tu"):
        if_type = "Tunnel"
    elif name.lower().startswith("se"):
        if_type = "Serial"
    else:
        if_type = None

    number_list = name.split(" ")
    if len(number_list) == 2:
        number = number_list[-1].strip()
    else:
        number = _get_number(name)

    if if_type:
        proper_interface = if_type + number
    else:
        proper_interface = name

    return proper_interface


def get_interface_type(interface):
    """Gets the type of interface"""

    if interface.upper().startswith("GI"):
        return "GigabitEthernet"
    elif interface.upper().startswith("TW"):
        return "TwoGigabitEthernet"
    elif interface.upper().startswith("TE"):
        return "TenGigabitEthernet"
    elif interface.upper().startswith("FA"):
        return "FastEthernet"
    elif interface.upper().startswith("FOURHUNDREDGIGE"):
        return "FourHundredGigE"
    elif interface.upper().startswith("FIFTYGIGE"):
        return "FiftyGigE"
    elif interface.upper().startswith("FOU"):
        return "FourHundredGigabitEthernet"
    elif interface.upper().startswith("FO"):
        return "FortyGigabitEthernet"
    elif interface.upper().startswith("FI"):
        return "FiveGigabitEthernet"
    elif interface.upper().startswith("LON"):
        return "LongReachEthernet"
    elif interface.upper().startswith("ET"):
        return "Ethernet"
    elif interface.upper().startswith("VL"):
        return "Vlan"
    elif interface.upper().startswith("LO"):
        return "loopback"
    elif interface.upper().startswith("PO"):
        return "Port-channel"
    elif interface.upper().startswith("NV"):
        return "nve"
    elif interface.upper().startswith("TWE"):
        return "TwentyFiveGigE"
    elif interface.upper().startswith("HU"):
        return "HundredGigE"
    elif interface.upper().startswith("VIRTUAL-TE"):
        return "Virtual-Template"
    elif interface.upper().startswith("TU"):
        return "Tunnel"
    elif interface.upper().startswith("SE"):
        return "Serial"
    else:
        return "unknown"


def get_ranges(data):
    """
    Returns a generator object that yields lists of
    consecutive integers from a list of integers.
    """
    for k, group in groupby(data, lambda t, c=count(): int(t) - next(c)):
        yield list(group)


def numerical_sort(string_int_list):
    """Sorts list of integers that are digits in numerical order."""

    as_int_list = []

    for vlan in string_int_list:
        as_int_list.append(int(vlan))
    as_int_list.sort()
    return as_int_list


def vlan_list_to_range(cmd):
    """
    Converts a comma separated list of vlan IDs
    into ranges.
    """
    ranges = []
    for v in get_ranges(cmd):
        ranges.append("-".join(map(str, (v[0], v[-1])[: len(v)])))
    return ",".join(ranges)


def vlan_range_to_list(vlans):
    result = []
    if vlans:
        for part in vlans:
            if part == "none":
                break
            if "-" in part:
                a, b = part.split("-")
                a, b = int(a), int(b)
                result.extend(range(a, b + 1))
            else:
                a = int(part)
                result.append(a)
        return numerical_sort(result)
    return result


def sort_dict(dictionary):
    sorted_dict = dict()
    for key, value in sorted(dictionary.items()):
        if isinstance(value, dict):
            sorted_dict[key] = sort_dict(value)
        else:
            sorted_dict[key] = value
    return sorted_dict


def generate_switchport_trunk(type, add, vlans_range):
    """
    Generates a list of switchport commands based on the trunk type and VLANs range.
    Ensures that the length of VLANs lexeme in a command does not exceed 220 characters.
    """

    def append_command():
        command_prefix = f"switchport trunk {type} vlan "
        if add or commands:
            command_prefix += "add "
        commands.append(command_prefix + ",".join(current_chunk))

    commands = []
    current_chunk = []
    current_length = 0

    for vrange in vlans_range.split(","):
        next_addition = vrange if not current_chunk else "," + vrange
        if current_length + len(next_addition) <= 220:
            current_chunk.append(vrange)
            current_length += len(next_addition)
        else:
            append_command()
            current_chunk = [vrange]
            current_length = len(vrange)

    if current_chunk:
        append_command()

    return commands
