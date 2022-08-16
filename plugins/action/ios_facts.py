from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase
import json
from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils import basic
from ansible.module_utils.connection import ConnectionError as AnsibleConnectionError
from ansible.errors import AnsibleActionFail
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    convert_doc_to_ansible_module_kwargs,
)

# from ansible_collections.junipernetworks.junos.plugins.modules.junos_facts import DOCUMENTATION
from ansible_collections.cisco.ios.plugins.modules.ios_facts import DOCUMENTATION
from ansible.module_utils.basic import AnsibleModule

# from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.facts.facts import (
#     Facts,
#     FACT_RESOURCE_SUBSETS,
# )
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.facts.facts import (
    Facts,
    FACT_RESOURCE_SUBSETS,
)

# from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.junos import (
#     junos_argument_spec,
# )
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.ios import ios_argument_spec


class ActionModule(ActionBase):
    """ action module
    """

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._result = {}

    def _fail_json(self, msg):
        """ Replace the AnsibleModule fail_json here
        :param msg: The message for the failure
        :type msg: str
        """
        msg = msg.replace("(basic.py)", self._task.action)
        raise AnsibleActionFail(msg)

    def _debug(self, msg):
        """Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> [get][action] {msg}".format(phost=self._playhost, msg=msg)
        self._display.vvvv(msg)

    def _check_argspec(self):
        """ Load the doc and convert
        Add the root conditionals to what was returned from the conversion
        and instantiate an AnsibleModule to validate
        """
        argspec = convert_doc_to_ansible_module_kwargs(DOCUMENTATION)
        basic._ANSIBLE_ARGS = to_bytes(json.dumps({"ANSIBLE_MODULE_ARGS": self._task.args}))
        basic.AnsibleModule.fail_json = self._fail_json
        basic.AnsibleModule(**argspec)

    def run(self, tmp=None, task_vars=None):
        argument_spec = (convert_doc_to_ansible_module_kwargs(DOCUMENTATION))["argument_spec"]
        argument_spec.update(ios_argument_spec)
        self._check_argspec()
        result = super(ActionModule, self).run(tmp, task_vars)
        if not (
            hasattr(self._connection, "socket_path") and self._connection.socket_path is not None
        ):
            raise AnsibleConnectionError("netconf connection to remote host in not active")
        if self._result.get("failed"):
            return self._result

        module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
        (module._socket_path) = self._connection.socket_path
        warnings = []
        if task_vars["gather_subset"] == "!config":
            warnings.append(
                "default value for `gather_subset` will be changed to `min` from `!config` v2.11 onwards"
            )
        ansible_facts = {}
        if task_vars.get("available_network_resources"):
            ansible_facts["available_network_resources"] = sorted(FACT_RESOURCE_SUBSETS.keys())

        ansible_network_resources = {}

        restorun_subsets = Facts(module).get_restorun()
        result = Facts(module).get_legacy_facts()
        additional_facts, additional_warnings = result
        ansible_facts.update(additional_facts)
        warnings.extend(additional_warnings)

        if restorun_subsets:
            for rmodule in restorun_subsets:
                name = rmodule
                rmodule = (
                    self._task.collections[0]
                    + "."
                    + self._task.collections[0].split(".")[1]
                    + "_"
                    + rmodule
                )
                if not self._shared_loader_obj.module_loader.has_plugin(rmodule):
                    result.update({"failed": True, "msg": "Could not find %s module." % rmodule})
                else:
                    self._display.vvvv("Running %s module to fetch data from remote host" % rmodule)
                    result = self._execute_module(
                        module_name=rmodule,
                        module_args={"state": "gathered"},
                        task_vars=task_vars,
                        wrap_async=self._task.async_val,
                    )
                    if result.get("failed"):
                        return result

                    if result.get("gathered"):
                        ansible_network_resources[name] = result["gathered"]

        ansible_facts.update({"ansible_network_resources": ansible_network_resources})
        ansible_facts["ansible_net_gather_network_resources"] = self._task.args.get(
            "gather_network_resources"
        )
        ansible_facts["gather_subset"] = module.params.get("gather_subset")
        return ansible_facts
