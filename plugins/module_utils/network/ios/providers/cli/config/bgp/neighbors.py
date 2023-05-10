#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import re

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.providers.providers import (
    CliProvider,
)


class Neighbors(CliProvider):
    def render(self, config=None, nbr_list=None):
        commands = []
        safe_list = []
        if not nbr_list:
            nbr_list = self.get_value("config.neighbors")

        for item in nbr_list:
            neighbor_commands = []
            context = "neighbor %s" % item["neighbor"]
            cmd = "{} remote-as {}".format(context, item["remote_as"])

            if not config or cmd not in config:
                neighbor_commands.append(cmd)

            for key, value in iteritems(item):
                if value is not None:
                    meth = getattr(self, "_render_%s" % key, None)
                    if meth:
                        resp = meth(item, config)
                        if resp:
                            neighbor_commands.extend(to_list(resp))

            commands.extend(neighbor_commands)
            safe_list.append(context)

        if self.params["operation"] == "replace" and config and safe_list:
            commands.extend(self._negate_config(config, safe_list))

        return commands

    def _negate_config(self, config, safe_list=None):
        commands = []
        matches = re.findall(r"(neighbor \S+)", config, re.M)
        for item in set(matches).difference(safe_list):
            commands.append("no %s" % item)
        return commands

    def _render_local_as(self, item, config=None):
        cmd = "neighbor {} local-as {}".format(item["neighbor"], item["local_as"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_port(self, item, config=None):
        cmd = "neighbor {} port {}".format(item["neighbor"], item["port"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_description(self, item, config=None):
        cmd = "neighbor {} description {}".format(item["neighbor"], item["description"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_enabled(self, item, config=None):
        cmd = "neighbor %s shutdown" % item["neighbor"]
        if item["enabled"] is True:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_update_source(self, item, config=None):
        cmd = "neighbor {} update-source {}".format(item["neighbor"], item["update_source"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_password(self, item, config=None):
        cmd = "neighbor {} password {}".format(item["neighbor"], item["password"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_ebgp_multihop(self, item, config=None):
        cmd = "neighbor {} ebgp-multihop {}".format(item["neighbor"], item["ebgp_multihop"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_peer_group(self, item, config=None):
        cmd = "neighbor {} peer-group {}".format(item["neighbor"], item["peer_group"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_timers(self, item, config):
        """Generate bgp timer related configuration."""
        keepalive = item["timers"]["keepalive"]
        holdtime = item["timers"]["holdtime"]
        min_neighbor_holdtime = item["timers"]["min_neighbor_holdtime"]
        neighbor = item["neighbor"]

        if keepalive and holdtime:
            cmd = f"neighbor {neighbor} timers {keepalive} {holdtime}"
            if min_neighbor_holdtime:
                cmd += " %s" % min_neighbor_holdtime
            if not config or cmd not in config:
                return cmd
            return None
        return None


class AFNeighbors(CliProvider):
    def render(self, config=None, nbr_list=None):
        commands = []
        if not nbr_list:
            return None

        for item in nbr_list:
            neighbor_commands = []
            for key, value in iteritems(item):
                if value is not None:
                    meth = getattr(self, "_render_%s" % key, None)
                    if meth:
                        resp = meth(item, config)
                        if resp:
                            neighbor_commands.extend(to_list(resp))

            commands.extend(neighbor_commands)

        return commands

    def _render_advertisement_interval(self, item, config=None):
        cmd = "neighbor {} advertisement-interval {}".format(
            item["neighbor"],
            item["advertisement_interval"],
        )
        if not config or cmd not in config:
            return cmd
        return None

    def _render_route_reflector_client(self, item, config=None):
        cmd = "neighbor %s route-reflector-client" % item["neighbor"]
        if item["route_reflector_client"] is False:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_route_server_client(self, item, config=None):
        cmd = "neighbor %s route-server-client" % item["neighbor"]
        if item["route_server_client"] is False:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_remove_private_as(self, item, config=None):
        cmd = "neighbor %s remove-private-as" % item["neighbor"]
        if item["remove_private_as"] is False:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_next_hop_self(self, item, config=None):
        cmd = "neighbor %s next-hop-self" % item["neighbor"]
        if item["next_hop_self"] is False:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_activate(self, item, config=None):
        cmd = "neighbor %s activate" % item["neighbor"]
        if item["activate"] is False:
            if not config or cmd in config:
                cmd = "no %s" % cmd
                return cmd
            return None
        elif not config or cmd not in config:
            return cmd
        return None

    def _render_maximum_prefix(self, item, config=None):
        cmd = "neighbor {} maximum-prefix {}".format(item["neighbor"], item["maximum_prefix"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_prefix_list_in(self, item, config=None):
        cmd = "neighbor {} prefix-list {} in".format(item["neighbor"], item["prefix_list_in"])
        if not config or cmd not in config:
            return cmd
        return None

    def _render_prefix_list_out(self, item, config=None):
        cmd = "neighbor {} prefix-list {} out".format(item["neighbor"], item["prefix_list_out"])
        if not config or cmd not in config:
            return cmd
        return None
