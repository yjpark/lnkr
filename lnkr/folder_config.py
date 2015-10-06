import os

import lnkr
import term

KEY_FROM = 'from'
KEY_TO = 'to'

class FolderConfig:
    def __init__(self, values):
        self.values = values
        self.valid = self.parse()

    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('FolderConfig', self.values, key, optional)

    def parse(self):
        self.from_value = self.get_section_value(KEY_FROM, True)
        self.to_value = self.get_section_value(KEY_TO, True)

        if self.from_value is None or self.to_value is None:
            term.error('Need to provide both "from" and "to": %s' % term.format_param(self.key))
            return False

        return True

    def convert_path(self, path, attribs_holders):
        attribs = lnkr.get_attribs(attribs_holders)
        for key in attribs:
            old_path = path
            path = path.replace('${%s}' % key, attribs[key])
            term.verbose('\nUpdate Path: %s = %s\n\tFrom: %s\n\tTo: %s' % (term.format_param(key), term.format_param(attribs[key]), term.format_path(old_path), term.format_path(path)))
        return path

    def get_from_path(self, root_path, attribs_holders):
        from_path = os.path.join(root_path, self.from_value)
        return self.convert_path(from_path, attribs_holders)

    def get_to_path(self, root_path, attribs_holders):
        to_path = os.path.join(root_path, self.to_value)
        return self.convert_path(to_path, attribs_holders)
