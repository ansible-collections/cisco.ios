# Copyright (c) 2020 Ansible
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import contextlib as _contextlib
import json

from unittest import TestCase
from unittest.mock import patch

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


try:
    from ansible.module_utils.common.messages import WarningSummary as _WarningSummary
except ImportError:
    _WarningSummary = None


@_contextlib.contextmanager
def set_module_args(args):
    """
    Context manager that sets module arguments for AnsibleModule
    """
    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    try:
        from ansible.module_utils.testing import patch_module_args
    except ImportError:
        # Before data tagging support was merged, this was the way to go:
        serialized_args = to_bytes(json.dumps({"ANSIBLE_MODULE_ARGS": args}))
        with patch.object(basic, "_ANSIBLE_ARGS", serialized_args):
            yield
    else:
        # With data tagging support, we have a new helper for this:
        with patch_module_args(args):
            yield


class AnsibleExitJson(Exception):
    """
    Exception raised by exit_json() to signal that the module exited successful.
    """

    pass


class AnsibleFailJson(Exception):
    """
    Exception raised by fail_json() to signal that the module failed.
    """

    pass


def exit_json(*args, **kwargs):
    """
    Mock replacement for AnsibleModule.exit_json() that raises AnsibleExitJson.
    """
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """
    Mock replacement for AnsibleModule.fail_json() that raises AnsibleFailJson.
    """
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class ModuleTestCase(TestCase):
    """
    Provides some infrastructure for using unittest.TestCase.

    Note that unittest.TestCase is not the recommended way of writing Ansible unit tests, but there
    still are a lot of existing tests in this form.
    """

    def setUp(self):
        self.mock_module = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
        )
        self.mock_module.start()
        self.mock_sleep = patch("time.sleep")
        self.mock_sleep.start()
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_sleep.stop)


def extract_warnings_texts(result):
    """
    Given the results dictionary of a module, extracts the warnings as a list of strings.
    """
    warnings = []
    if result.get("warnings"):
        for warning in result["warnings"]:
            if _WarningSummary and isinstance(warning, _WarningSummary):
                warnings.append(warning.details[0].msg)
                continue
            warnings.append(warning)
    return warnings
