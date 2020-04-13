from ansible.module_utils.network.common.utils import Template


class RmModuleRender(object):
    """ RmModuleRender
    """
    def __init__(self, tmplt):
        self._tmplt = tmplt
        self._template = Template()

    def get_parser(self, name):
        """ get_parsers
        """
        res = [p for p in self._tmplt.PARSERS if p['name'] == name]
        return res[0]

    def _render(self, tmplt, data, negate):
        try:
            if callable(tmplt):
                res = tmplt(data)
            else:
                res = self._template(value=tmplt, variables=data,
                                     fail_on_undefined=False)
        except KeyError:
            return None
        if res and negate:
            return 'no ' + res
        return res

    def render(self, data, parser_name, negate=False):
        """ render
        """
        if negate:
            tmplt = self.get_parser(parser_name).get('remval') or \
                    self.get_parser(parser_name)['setval']
        else:
            tmplt = self.get_parser(parser_name)['setval']
        command = self._render(tmplt, data, negate)
        return command
