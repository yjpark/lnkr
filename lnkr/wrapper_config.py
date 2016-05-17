from __future__ import absolute_import
import os

from . import util
from . import term
from .import_config import ImportConfig

all_wrapper_configs = {}

class WrapperConfig(ImportConfig):
    def __init__(self, path):
        ImportConfig.__init__(self, 'Wrapper', path)

    def set_mode(self, mode):
        for section in self.import_sections:
            section.mode = mode

    def get_wrapper_section(self, key):
        return self.get_import_section(key)

def load_wrapper_config(path):
    wrapper_path = os.path.join(path, util.WRAPPER_CONFIG_FILE_NAME)
    if wrapper_path in all_wrapper_configs:
        return all_wrapper_configs[wrapper_path]

    config = WrapperConfig(wrapper_path)
    if config.valid:
        all_wrapper_configs[wrapper_path] = config
        return config
    else:
        return None
