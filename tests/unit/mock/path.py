from __future__ import absolute_import, division, print_function


__metaclass__ = type
from ansible.utils.path import unfrackpath

from ansible_collections.cisco.ios.tests.unit.compat.mock import MagicMock


mock_unfrackpath_noop = MagicMock(
    spec_set=unfrackpath,
    side_effect=lambda x, *args, **kwargs: x,
)
