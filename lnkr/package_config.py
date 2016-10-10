from __future__ import absolute_import
import os

from . import term
from . import util
from .toml_config import TomlConfig
from .export_section import ExportSection, new_export_section

all_package_configs = {}

class PackageConfig(TomlConfig):
    def __init__(self, path):
        self.export_sections = []
        TomlConfig.__init__(self, 'Package', path)

    def parse(self):
        return TomlConfig.parse(self, self.export_sections, new_export_section);

    def log_detail(self, prefix):
        term.info('\n%s%s -> %s' % (prefix, term.format_path(self.path), term.format_param(str(self))))
        for section in self.export_sections:
            term.info('\n\t%s%s -> %s' % (prefix, term.format_path(section.key), term.format_param(str(section))))

    def get_export_section(self, key):
        for section in self.export_sections:
            if section.key == key:
                return section
        return None

def load_package_config(path):
    package_path = os.path.join(path, util.PACKAGE_CONFIG_FILE_NAME)
    if package_path in all_package_configs:
        return all_package_configs[package_path]

    config = PackageConfig(package_path)
    if config.valid:
        all_package_configs[package_path] = config
        return config
    else:
        return None

