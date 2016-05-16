from __future__ import absolute_import

import os
from pathlib import Path

from . import term
from .folder_config import FolderConfig

KEY_INCLUDE = 'include'
KEY_EXCLUDE = 'exclude'

class FileConfig(FolderConfig):
    def get_section_value(self, key, optional=False):
        return lnkr.get_section_value('FileConfig', self.values, key, optional)

    def parse(self):
        ok = FolderConfig.parse(self)
        if ok:
            self.include = self.get_section_value(KEY_INCLUDE, False)
            self.exclude = self.get_section_value(KEY_EXCLUDE, True)
        return ok

    def get_file_list(self, from_path):
        includes = Path(from_path).glob(self.include)
        filtered = includes
        if self.exclude:
            term.error("exclude not supported yet!")
        return [os.path.relpath(file_name, from_path) for file_name in filtered]
