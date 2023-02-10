#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The remove_keys plugin code
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible.errors import AnsibleFilterError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'acl_popper': {msg}".format(msg=msg)
    raise AnsibleFilterError(error)


def clear_empty_data(data):
    if isinstance(data, dict):
        # for k in list(data.keys()):
        #     if not data.get(k, {}):
        #         del data[k]
        for k, v in data.items():
            data[k] = clear_empty_data(v)
    if isinstance(data, list):
        temp = []
        for i in data:
            if i:
                temp.append(clear_empty_data(i))
        return temp
    return data


def check_match(ace, match_criteria):
    if ace.get("sequence") == match_criteria.get("sequence"):
        return True
    if ace.get("protocol") == match_criteria.get("protocol"):
        return True
    if ace.get("grant") == match_criteria.get("grant"):
        return True
    if match_criteria.get("source_address"):
        if ace.get("source").get("address") == match_criteria.get("source_address"):
            return True
    if ace.get("destination", {}).get("address") == match_criteria.get("destination_address"):
        return True


def _acl_popper(raw_acl, match_criteria):

    acls_v4, acls_v6 = [], []
    racls_v4, racls_v6 = [], []

    final_acl = {
        "acls": [{"acls": acls_v4, "afi": "ipv4"}, {"acls": acls_v6, "afi": "ipv6"}]
    }  # holds final acl data after removal of aces
    rfinal_acl = {
        "acls": [{"acls": racls_v4, "afi": "ipv4"}, {"acls": racls_v6, "afi": "ipv6"}]
    }  # holds removed acl information

    for acls in raw_acl:  # ["acls"]

        afi = acls.get("afi")  # ipv4 or v6

        for acl in acls.get("acls"):
            _keep = True

            name = acl.get("name")  # filter by acl_name ignores whole acl entries i.e all aces
            if name in match_criteria.get("acl_name"):
                _keep = False

            acl_type = acl.get("acl_type")  # not being used
            aces = acl.get("aces")

            _aces, _acl = [], {}
            _races, _racl = [], {}

            for ace in aces:  # iterate on ace entries
                if _keep and check_match(
                    ace, match_criteria
                ):  # check matching criteria and remove from final dict
                    _races.append(ace)
                    continue

                if not _keep:
                    _races.append(ace)
                else:
                    _aces.append(ace)

            if _aces:  # store filtered aces
                _acl["name"] = name
                _acl["ace"] = _aces
                if afi == "ipv4":
                    acls_v4.append(_acl)
                else:
                    acls_v6.append(_acl)

            if _races:  # store removed aces
                _racl["name"] = name
                _racl["ace"] = _races
                if afi == "ipv4":
                    racls_v4.append(_racl)
                else:
                    racls_v6.append(_racl)

    return final_acl, rfinal_acl


def acl_popper(data, filter_options, match_criteria):
    """Remove unwanted keys recursively from a given data"
    :param data: The data passed in (data|remove_keys(...))
    :type data: raw
    :param target: List of keys on with operation is to be performed
    :type data: list
    :type elements: string
    :param matching_parameter: matching type of the target keys with data keys
    :type data: str
    """
    if not isinstance(data, (list, dict)):
        _raise_error("Input is not valid for attribute removal")
    cleared_data, removed_data = _acl_popper(data, match_criteria)
    data = {
        "acls": cleared_data,
        "removed_acls": removed_data,
    }
    # data = clear_empty_data(data)
    return data
