from __future__ import absolute_import

import os
import sys

from . import util
from . import term

KEY_LOCAL = 'local'
KEY_REMOTE = 'remote'
KEY_MODE = 'mode'

MODE_COPY = 'copy'
MODE_LINK = 'link'
MODE_SYMLINK = 'symlink'

windows_mode = sys.platform.startswith('win')

class ImportSection:
    def __init__(self, path, key, values):
        self.path = path
        self.key = key
        self.values = values
        self.valid = self.parse()
        self.loaded = False
        self.package_config = None
        self.wrapper_config = None

    def __str__(self):
        if self.valid:
            return '[ImportSection: %s -> {local = "%s", remote = "%s", mode = "%s"}]' % (self.key, self.local, self.remote, self.mode)
        else:
            return '[Invalid ImportSection: %s -> %s]' % (self.key, self.values)

    def log_detail(self, prefix):
        term.info('\n%s%s -> %s' % (prefix, term.format_path(self.path), term.format_param(str(self))))
        if self.package_config is not None:
            self.package_config.log_detail(prefix + "\t")
        if self.wrapper_config is not None:
            self.wrapper_config.log_detail(prefix + "\t")
        if self.package_config is None and self.wrapper_config is None:
            term.error('\n%sInvalid ImportSection: %s -> %s' % (prefix, term.format_path(self.path), term.format_param(self.key)))

    def get_section_value(self, key, optional=False):
        return util.get_section_value('ImportSection', self.values, key, optional)

    def get_mode(self):
        return self.get_section_value(KEY_MODE, True)

    def parse(self):
        self.local = self.get_section_value(KEY_LOCAL, True)
        self.remote = self.get_section_value(KEY_REMOTE, True)
        self.mode = self.get_mode()

        if self.local is None and self.remote is None:
            term.error('Need to provide either "local" or "remote": %s' % term.format_param(self.key))
            return False

        return True

    def do_load(self, package_path):
        from . import package_config
        self.package_config = package_config.load_package_config(package_path)
        if self.package_config is None:
            term.error("Failed to load package config %s" % package_path)
            return False

        from . import wrapper_config
        self.wrapper_config = wrapper_config.load_wrapper_config(package_path)
        if self.wrapper_config is not None:
            self.wrapper_config.set_mode(self.mode)

        return self.package_config is not None

    def load_local(self):
        return self.do_load(os.path.join(self.path, self.local))

    def load_remote(self):
        term.info('Not Implemented: Import Remote Package')
        return False

    def check_mode(self):
        if self.mode == MODE_COPY:
            return True
        elif self.mode == MODE_LINK:
            return True
        elif self.mode == MODE_SYMLINK:
            return True

        return False

    def load(self):
        term.info('Load Import Section: %s -> %s' % (term.format_path(self.path), term.format_param(self.key)))
        if not self.check_mode():
            return False

        if self.local is not None:
            self.loaded = self.load_local()
        elif self.remote is not None:
            self.loaded = self.load_remote()
        if not self.loaded:
            term.error('Load Import Section Failed: %s -> %s' % (term.format_path(self.path), term.format_param(self.key)))

    def get_component(self, key):
        #TODO: It's messy about the dependencies, quick fix for now
        if not self.loaded:
            self.load()

        if self.package_config is not None:
            export_section = self.package_config.get_export_section(key)
            if export_section is not None:
                return export_section
        if self.wrapper_config is not None:
            wrapper_section = self.wrapper_config.get_wrapper_section(key)
            if wrapper_section is not None:
                return wrapper_section
        return None

def new_import_section(path, key, values):
    section = ImportSection(os.path.dirname(path), key, values)
    if section.valid:
        return section
    else:
        term.error('Invalid Import Section: %s -> %s' % (key, values))
