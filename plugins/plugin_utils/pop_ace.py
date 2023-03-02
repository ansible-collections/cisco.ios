#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The pop_ace plugin code
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.errors import AnsibleFilterError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'pop_ace': {msg}".format(msg=msg)
    raise AnsibleFilterError(error)


def fail_missing(racl, fail):
    if fail and racl == []:
        _raise_error("no entries removed on the provided match_criteria")


def check_match(ace, match_criteria, match_all, name, afi):
    check_arr = []
    for k, v in match_criteria.items():
        if v:
            if k not in ["source", "destination", "acl_name", "afi"]:
                check_arr.append(True) if ace.get(k, "NA") == match_criteria.get(
                    k,
                ) else check_arr.append(False)
            elif k == "acl_name":
                check_arr.append(True) if name == match_criteria.get(
                    k,
                ) else check_arr.append(False)
            elif k == "afi":
                check_arr.append(True) if afi == match_criteria.get(
                    k,
                ) else check_arr.append(False)
            else:  # for source and destination address
                _sub = "source" if "source" in k else "destination"
                _valid = []
                _valid.append(True) if ace.get(_sub, {}).get("address", "NA") == match_criteria.get(
                    k,
                ) else _valid.append(False)
                _valid.append(True) if ace.get(_sub, {}).get("host", "NA") == match_criteria.get(
                    k,
                ) else _valid.append(False)
                _valid.append(True) if ace.get(_sub, {}).get("any", "NA") == (
                    match_criteria.get(k) == "any"
                ) else _valid.append(False)
                check_arr.append(any(_valid))

    if match_all:  # forces all criteria to match
        return all(check_arr)
    else:
        return any(check_arr)


def _pop_ace(raw_acl, filter_options, match_criteria):
    acls_v4, acls_v6 = [], []
    racls_v4, racls_v6 = [], []

    remove_first_ace_only = True if filter_options.get("remove") == "first" else False
    fail_if_no_match = True if filter_options.get("failed_when") == "missing" else False
    match_all = True if filter_options.get("match_all") is True else False

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
            _races, _racl, _rstop = [], {}, True

            aces = acl.get("aces", {})
            name = acl.get("name", "")  # filter by acl_name ignores whole acl entries i.e all aces

            for ace in aces:  # iterate on ace entries
                jude = check_match(
                    ace=ace,
                    match_criteria=match_criteria,
                    match_all=match_all,
                    name=name,
                    afi=afi,
                )
                if jude:  # check matching criteria and remove from final dict
                    if remove_first_ace_only and _rstop:  # removes one ace entry per acl
                        _races.append(ace)
                        _rstop = False
                        continue
                    elif not remove_first_ace_only:  # for remove all
                        _races.append(ace)
                        continue

                _aces.append(
                    ace,
                )

            if _aces:  # store filtered aces
                _acl["name"], _acl["aces"] = name, _aces
                acls_v4.append(_acl) if afi == "ipv4" else acls_v6.append(_acl)

            if _races:  # store removed aces
                _racl["name"], _racl["aces"] = name, _races
                racls_v4.append(_racl) if afi == "ipv4" else racls_v6.append(_racl)

    fail_missing(racls_v4 + racls_v6, fail_if_no_match)

    return final_acl, rfinal_acl


def pop_ace(data, filter_options, match_criteria):
    if not isinstance(data, (list, dict)):
        _raise_error("Input is not valid for pop_ace")
    cleared_data, removed_data = _pop_ace(data, filter_options, match_criteria)
    data = {
        "clean_acls": cleared_data,
        "removed_aces": removed_data,
    }
    return data
