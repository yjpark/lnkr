from __future__ import absolute_import

import os

from . import term
from .toml_config import TomlConfig
from .import_section import ImportSection, new_import_section

class ImportConfig(TomlConfig):
    def __init__(self, kind, path):
        self.import_sections = []
        TomlConfig.__init__(self, kind, path)

    def parse(self):
        return TomlConfig.parse(self, self.import_sections, new_import_section);

    def log_detail(self, prefix):
        term.info('\n%s%s -> %s' % (prefix, term.format_path(self.path), term.format_param(str(self))))
        for section in self.import_sections:
            term.info('\n\t%s%s -> %s' % (prefix, term.format_path(section.key), term.format_param(str(section))))

    def get_import_section(self, key):
        for section in self.import_sections:
            if section.key == key:
                return section
        return None
