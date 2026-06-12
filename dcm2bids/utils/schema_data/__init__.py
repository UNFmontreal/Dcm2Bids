# inspiration from
# https://learn.scientific-python.org/development/patterns/data-files/#using-the-init

"""
Bundled _stable_ BIDS schema resources available upon dcm2bids release.

This module exposes:

- `file`: a pointer to the json.
"""

from importlib import resources

file = resources.files(__name__)
