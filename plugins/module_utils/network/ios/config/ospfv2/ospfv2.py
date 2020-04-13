#
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The ios_ospfv2 class
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to it's desired end-state is
created
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.ospfv2 import Ospfv2Template
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import dict_merge

from ansible_collections.cisco.ios.plugins.module_utils.network.common.rm_module import RmModule
from ansible_collections.cisco.ios.plugins.module_utils.network.common.rm_utils import (
    get_from_dict,
    compare_partial_dict
)


class Ospfv2(RmModule):
    """
    The ios_ospfv2 class
    """

    gather_subset = [
        '!all',
        '!min',
    ]

    gather_network_resources = [
        'ospfv2',
    ]

    def __init__(self, module):
        # super(Ospfv2, self).__init__(module)
        super(Ospfv2, self).__init__(empty_fact_val={},
                                   facts_module=Facts(module),
                                   module=module, resource='ospfv2',
                                   tmplt=Ospfv2Template())

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        self.gen_config()
        self.run_commands()
        return self.result

    def gen_config(self):
        """ Select the appropriate function based on the state provided

        :rtype: A list
        :returns: the commands necessary to migrate the current configuration
                  to the desired configuration
        """

        wantd = {(entry['id'], entry.get('vrf')): entry
                 for entry in self.want.get('processes', [])}
        haved = {(entry['id'], entry.get('vrf')): entry
                 for entry in self.have.get('processes', [])}

        # turn all lists of dicts into dicts prior to merge
        for thing in wantd, haved:
            for _pid, proc in thing.items():
                for area in proc.get('areas', []):
                    area['ranges'] = {entry['range']: entry
                                      for entry in area.get('ranges', [])}
                proc['areas'] = {entry['area']: entry
                                 for entry in proc.get('areas', [])}

        # if state is merged, merge want onto have
        if self.state == 'merged':
            wantd = dict_merge(haved, wantd)

        # if state is deleted, limit the have to anything in want
        # set want to nothing
        if self.state == 'deleted':
            haved = {k: v for k, v in haved.items()
                     if k in wantd or not wantd}
            wantd = {}

        # delete processes first so we do run into "more than one" errs
        if self.state in ['overridden', 'deleted']:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)
                    self.addcmd(have, 'process_id', True)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        # begin = len(self.commands)
        parsers = ['adjacency.exchange_start.threshold',
                   'auto_cost.reference_bandwidth', 'bfd.all_interfaces',
                   'compatible.rfc1583', 'distance.external',
                   'distance.intra_area', 'distance.inter_area',
                   'distribute_list', 'dn_bit_ignore',
                   'graceful_restart.helper']

        self.addcmd(want or have, 'process_id', False)
        self.compare(parsers, want, have)
        self._areas_compare(want, have)
        self._default_information_compare(want, have)
        self._graceful_restart_compare(want, have)

    # def get_ospfv2_facts(self):
    #     """ Get the 'facts' (the current configuration)
    #
    #     :rtype: A dictionary
    #     :returns: The current configuration as a dictionary
    #     """
    #     facts, _warnings = Facts(self._module).get_facts(self.gather_subset, self.gather_network_resources)
    #     ospfv2_facts = facts['ansible_network_resources'].get('ospfv2')
    #     if not ospfv2_facts:
    #         return []
    #     return ospfv2_facts
    #
    # def execute_module(self):
    #     """ Execute the module
    #
    #     :rtype: A dictionary
    #     :returns: The result from module execution
    #     """
    #     result = {'changed': False}
    #     warnings = list()
    #     commands = list()
    #
    #     existing_ospfv2_facts = self.get_ospfv2_facts()
    #     commands.extend(self.set_config(existing_ospfv2_facts))
    #     if commands:
    #         if not self._module.check_mode:
    #             self._connection.edit_config(commands)
    #         result['changed'] = True
    #     result['commands'] = commands
    #
    #     changed_ospfv2_facts = self.get_ospfv2_facts()
    #
    #     result['before'] = existing_ospfv2_facts
    #     if result['changed']:
    #         result['after'] = changed_ospfv2_facts
    #
    #     result['warnings'] = warnings
    #     return result
    #
    # def set_config(self, existing_ospfv2_facts):
    #     """ Collect the configuration from the args passed to the module,
    #         collect the current configuration (as a dict from facts)
    #
    #     :rtype: A list
    #     :returns: the commands necessary to migrate the current configuration
    #               to the desired configuration
    #     """
    #     want = self._module.params['config']
    #     have = existing_ospfv2_facts
    #     resp = self.set_state(want, have)
    #     return to_list(resp)
    #
    # def set_state(self, want, have):
    #     """ Select the appropriate function based on the state provided
    #
    #     :param want: the desired configuration as a dictionary
    #     :param have: the current configuration as a dictionary
    #     :rtype: A list
    #     :returns: the commands necessary to migrate the current configuration
    #               to the desired configuration
    #     """
    #     state = self._module.params['state']
    #     if state == 'overridden':
    #         kwargs = {}
    #         commands = self._state_overridden(**kwargs)
    #     elif state == 'deleted':
    #         kwargs = {}
    #         commands = self._state_deleted(**kwargs)
    #     elif state == 'merged':
    #         kwargs = {}
    #         commands = self._state_merged(**kwargs)
    #     elif state == 'replaced':
    #         kwargs = {}
    #         commands = self._state_replaced(**kwargs)
    #     return commands
    # @staticmethod
    # def _state_replaced(**kwargs):
    #     """ The command generator when state is replaced
    #
    #     :rtype: A list
    #     :returns: the commands necessary to migrate the current configuration
    #               to the desired configuration
    #     """
    #     commands = []
    #     return commands
    #
    # @staticmethod
    # def _state_overridden(**kwargs):
    #     """ The command generator when state is overridden
    #
    #     :rtype: A list
    #     :returns: the commands necessary to migrate the current configuration
    #               to the desired configuration
    #     """
    #     commands = []
    #     return commands
    #
    # @staticmethod
    # def _state_merged(**kwargs):
    #     """ The command generator when state is merged
    #
    #     :rtype: A list
    #     :returns: the commands necessary to merge the provided into
    #               the current configuration
    #     """
    #     commands = []
    #     return commands
    #
    # @staticmethod
    # def _state_deleted(**kwargs):
    #     """ The command generator when state is deleted
    #
    #     :rtype: A list
    #     :returns: the commands necessary to remove the current configuration
    #               of the provided objects
    #     """
    #     commands = []
    #     return commands
