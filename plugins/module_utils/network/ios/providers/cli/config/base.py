#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list


class ConfigBase:
    argument_spec = {}

    mutually_exclusive = []

    identifier = ()

    def __init__(self, **kwargs) -> None:
        self.values = {}
        self._rendered_configuration = {}
        self.active_configuration = None

        for item in self.identifier:
            self.values[item] = kwargs.pop(item)

        for key, value in iteritems(kwargs):
            if key in self.argument_spec:
                setattr(self, key, value)

        for key, value in iteritems(self.argument_spec):
            if value.get("default") and not getattr(self, key, None):
                setattr(self, key, value.get("default"))

    def __getattr__(self, key):
        if key in self.argument_spec:
            return self.values.get(key)
        return None

    def __setattr__(self, key, value) -> None:
        if key in self.argument_spec:
            if key in self.identifier:
                raise TypeError("cannot set value")
            elif value is not None:
                self.values[key] = value
        else:
            super().__setattr__(key, value)

    def context_config(self, cmd):
        if "context" not in self._rendered_configuration:
            self._rendered_configuration["context"] = []
        self._rendered_configuration["context"].extend(to_list(cmd))

    def global_config(self, cmd):
        if "global" not in self._rendered_configuration:
            self._rendered_configuration["global"] = []
        self._rendered_configuration["global"].extend(to_list(cmd))

    def get_rendered_configuration(self):
        config = []
        for section in ("context", "global"):
            config.extend(self._rendered_configuration.get(section, []))
        return config

    def set_active_configuration(self, config):
        self.active_configuration = config

    def render(self, config=None):
        raise NotImplementedError

    def get_section(self, config, section):
        if config is not None:
            netcfg = NetworkConfig(indent=1, contents=config)
            try:
                config = netcfg.get_block_config(to_list(section))
            except ValueError:
                config = None
            return config
        return None
