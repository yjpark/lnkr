0.1.5
-----

- Do the attrib conversion for from_path as well
- add `mode_win` for windows platform override

0.1.4
-----

- Not using blessings under windows (still depends on `cp`)

0.1.3
-----

- Bugfix with folder relative symlink

0.1.2
-----

- Detech reltive path for symlink

0.1.1
-----

- Bugfix with symlink file again

0.1.0
-----
Basic functions implemented:
- Support package definition, file name is lnkr-export.toml
  - can export local folder/files
  - can wrap other projects with wrapper definition (file name is lnkr-wrapper.toml)
- Support import definition, file name is lnkr-import.toml
  - support folder, and files
  - support copy mode and symlink mode
- Doc is missing for now
