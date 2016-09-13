from __future__ import absolute_import

import os

from . import term
from .import_config import ImportConfig

class AppConfig(ImportConfig):
    def __init__(self, path):
        self.loaded_components = {}
        self.linked_components = {}
        ImportConfig.__init__(self, 'App', path)
        self.all_attribs = {}
        self.append_all_attribs(self)

    def mark_loaded_component(self, key, section):
        self.loaded_components[key] = section

    def is_component_loaded(self, key):
        return key in self.loaded_components

    def mark_linked_component(self, key, section):
        self.linked_components[key] = section

    def is_component_linked(self, key):
        return key in self.linked_components

    def append_all_attribs(self, holder):
        if not hasattr(holder, 'attribs'):
            term.verbose('Bypass Attrib Holder: %s' % holder)
            return;

        term.verbose('Use Attrib Holder: %s' % holder)
        for key in holder.attribs:
            value = holder.attribs[key]
            if key in self.all_attribs:
                old_value = self.all_attribs[key]
                if old_value != value:
                    term.error('Attrib Overrided: %s, %s -> %s' % (term.format_path(key), term.format_param(value), term.format_param(old_value)))
            else:
                term.verbose('Attrib Defined: %s = %s' % (term.format_path(key), term.format_param(value)))
                self.all_attribs[key] = value
