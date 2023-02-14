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


def fail_missing(racl, fail):
    if fail and racl == []:
        _raise_error("no entries removed on the provided match_criteria")


def _acl_popper(raw_acl, failed_when, match_criteria):
    acls_v4, acls_v6 = [], []
    racls_v4, racls_v6 = [], []

    fail_if_no_match = True if failed_when == "missing" else False

    final_acl = {
        "acls": [{"acls": acls_v4, "afi": "ipv4"}, {"acls": acls_v6, "afi": "ipv6"}],
    }  # holds final acl data after removal of aces
    rfinal_acl = {
        "acls": [{"acls": racls_v4, "afi": "ipv4"}, {"acls": racls_v6, "afi": "ipv6"}],
    }  # holds removed acl information

    for acls in raw_acl:  # ["acls"]
        afi = acls.get("afi")  # ipv4 or v6

        for acl in acls.get("acls"):
            _aces, _acl = [], {}
            _races, _racl = [], {}

            aces = acl.get("aces")
            name = acl.get("name")  # filter by acl_name ignores whole acl entries i.e all aces

            _afi = match_criteria.get(afi)
            _matched_acl = _afi.get(name, [])

            for ace in aces:  # iterate on ace entries
                if ace["sequence"] in _matched_acl:
                    _races.append(ace)
                else:
                    _aces.append(ace)

            if _aces:  # store filtered aces
                _acl["name"], _acl["ace"] = name, _aces
                acls_v4.append(_acl) if afi == "ipv4" else acls_v6.append(_acl)

            if _races:  # store removed aces
                _racl["name"], _racl["ace"] = name, _races
                racls_v4.append(_racl) if afi == "ipv4" else racls_v6.append(_racl)

    fail_missing(racls_v4 + racls_v6, fail_if_no_match)

    return final_acl, rfinal_acl


def acl_popper(data, failed_when, match_criteria):
    if not isinstance(data, (list, dict)):
        _raise_error("Input is not valid for acl_popper")
    cleared_data, removed_data = _acl_popper(data, failed_when, match_criteria)
    data = {
        "acls": cleared_data,
        "removed_acls": removed_data,
    }
    # data = clear_empty_data(data)
    return data
