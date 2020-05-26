# CHANGELOG

## 3.0.0

- The anonymizer option is back

## 2.1.5

## 2.1.4 - 2019-04-04

- Add a tutorial to the documentation
- Update BIDS version in dcm2bids_scaffold
- Bug fix when intendedFor was equal to 0
- Restructuring of the documentation and add version description

## 2.1.3 - 2019-04-02

- dicom_dir can be a list or str

## 2.1.2 - 2019-04-01

- Add documentation with mkdocs
- Bug fix in dcm2niix_version

## 2.1.1 - 2019-03-29

- Bug fix

## 2.1.0 - 2019-03-28

- Checking if a new version of dcm2bids or dcm2niix is available on github
- dcm2niix output is now log to file as debug
- Add dcm2bids version to sidecars
- intendedFor option can also be a list

## 2.0.0 - 2019-03-10

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

## 1.1.8 - 2018-02-02

- Add dcm2bids as runscript inside Singularity
- Remove logger from dcm2bids_helper

## 1.1.7 - 2018-02-01

## 1.1.6 - 2018-02-01

## 1.1.4 - 2017-11-09

## 1.1.3 - 2017-11-09

## 1.1.2 - 2017-11-03

## 1.0.1 - 2017-11-01
