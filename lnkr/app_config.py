from __future__ import absolute_import

import os

from . import term
from .import_config import ImportConfig

class AppConfig(ImportConfig):
    def __init__(self, path):
        self.loaded_components = {}
        ImportConfig.__init__(self, 'App', path)

    def mark_loaded_component(self, key, section):
        self.loaded_components[key] = section

    def is_component_loaded(self, key):
        return key in self.loaded_components

