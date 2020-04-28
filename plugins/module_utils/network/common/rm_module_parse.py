import re
from copy import deepcopy
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import dict_merge, Template
import q

class RmModuleParse(object):
    def __init__(self, lines, tmplt):
        self._lines = lines
        self._tmplt = tmplt
        self._template = Template()

    def _deepformat(self, tmplt, data):
        wtmplt = deepcopy(tmplt)
        if isinstance(tmplt, str):
            res = self._template(value=tmplt, variables=data,
                                 fail_on_undefined=False)
            return res
        if isinstance(tmplt, dict):
            for tkey, tval in tmplt.items():
                ftkey = self._template(tkey, data)
                if ftkey != tkey:
                    wtmplt.pop(tkey)
                if isinstance(tval, dict):
                    wtmplt[ftkey] = self._deepformat(tval, data)
                elif isinstance(tval, list):
                    wtmplt[ftkey] = [self._deepformat(x, data) for x in tval]
                elif isinstance(tval, str):
                    wtmplt[ftkey] = self._deepformat(tval, data)
                    if wtmplt[ftkey] is None:
                        wtmplt.pop(ftkey)
        return wtmplt

    def parse(self):
        """ parse
        """
        result = {}
        shared = {}
        for line in self._lines:
            for parser in self._tmplt.PARSERS:
                cap = re.match(parser['getval'], line)
                if cap:
                    capdict = cap.groupdict()
                    capdict = {k: v for k, v in capdict.items()
                               if v is not None}
                    if parser.get('shared'):
                        shared = capdict
                    vals = dict_merge(capdict, shared)
                    res = self._deepformat(deepcopy(parser['result']), vals)
                    result = dict_merge(result, res)
                    break
        return result
