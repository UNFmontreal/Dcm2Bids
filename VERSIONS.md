## Versions

2.0.0
 - The anonymizer option no longer exists from the script dcm2bids. It is still possible to deface the anatomical nifti images using the "defaceTpl" key in the congifuration file.
 - Acquisitions are now sorted using the sidecar data instead of only the sidecar filename. The default behaviour is to sort by `SeriesNumber` then by `AcquisitionTime` then by the `SidecarFilename`. You can change this behaviour setting the key "compKeys" inside the configuration file.
 - Add an option to use `re` for more flexibility for matching criteria. Set the key "searchMethod" to "re" in the config file. fnmatch is still the default.
 - Design fix in matching with list in the sidecar.
 - Sidecar modification using "sidecarChanges" in the configuration file.
 - intendedFor option for fieldmap in the configuration file
 - log improvement
 - major code refactoring
 - add docstrings
 - add tests with pytest


1.1.8
 - Add dcm2bids as runscript inside Singularity
 - Remove logger from dcm2bids_helper
