# -*- coding: utf-8 -*-

# Format expected by pyproject.toml and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 3
_version_minor = 3
_version_micro = 0
_version_extra = 'rc2'

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_micro]
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__

__BIDSversion__ = "v1.11.1"