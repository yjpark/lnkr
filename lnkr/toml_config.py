from __future__ import absolute_import

import os

import pytoml

from . import term

class TomlConfig:
    def __init__(self, kind, path):
        self.kind = kind
        self.attribs = {}
        path = os.path.abspath(path)
        self.path = path
        self.root_path = os.path.dirname(path)
        self.values = None
        if not os.path.isfile(self.path):
            term.verbose('File Not Exist: %s' % term.format_path(self.path))
            self.valid = False
        else:
            self.valid = self.load() and self.parse()
            if not self.valid:
                term.error('Invalid Config [%s]: %s' % (self.__class__, term.format_path(self.path)))

    def __str__(self):
        if self.valid:
            return '[TomlConfig: %s %s -> %s]' % (self.kind, self.path, self.attribs)
        else:
            return '[Invalid TomlConfig: %s %s -> %s]' % (self.Kind, self.path, self.values)

    def load(self):
        try:
            self.values = pytoml.load(open(self.path, 'rb'))
        except Exception as e:
            term.error('Failed Loading Toml Config: %s -> %s' % (term.format_path(self.path), e))
            return False
        return True

    def parse(self, sections, factory):
        term.info('Parse %s Config: %s' % (self.kind, term.format_path(self.path)))
        for key in self.values:
            value = self.values[key]
            if isinstance(value, dict):
                section = factory(self.path, key, value)
                if section is not None:
                    sections.append(section)
            else:
                self.attribs[key] = value
        for key in self.attribs:
            term.verbose('Parse %s Config Attrib: %s = %s' % (self.kind, term.format_path(key), term.format_param(self.attribs[key])))
        for section in sections:
            term.verbose('Parse %s Config Section: %s' % (self.kind, term.format_param(section.__str__())))
        return len(sections) > 0
