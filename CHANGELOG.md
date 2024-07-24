# CHANGELOG

## [3.1.1](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/3.1.1) - 2023-10-12

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.1.1)

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.1.1)

Here is the newest release of dcm2bids ! 🎉 🥳

No new feature but two useful fixes !
Hope you like this new feature less buggy ⛔ 🐛

Arnaud and Sam

### What's Changed

- Bump gitpython from 3.1.35 to 3.1.37 by [@dependabot](https://github.com/dependabot) in [#277](https://github.com/UNFmontreal/Dcm2Bids/pull/277)
- [BF] Auto extractors and merge regex expressions by [@arnaudbore](https://github.com/arnaudbore) in [#275](https://github.com/UNFmontreal/Dcm2Bids/pull/275)
- [ENH] fix binary by [@arnaudbore](https://github.com/arnaudbore) in [#278](https://github.com/UNFmontreal/Dcm2Bids/pull/278)

**Full Changelog**: [3.1.0...3.1.1](https://github.com/UNFmontreal/Dcm2Bids/compare/3.1.0...3.1.1)

## [3.1.0](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/3.1.0) - 2023-09-13

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.1.0)

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.1.0)

We are excited to announce the newest release of dcm2bids ! 🎉 🥳

This update introduces some new features, improvements, and bug fixes to enhance your DICOM to BIDS conversion experience.
Everything embedded into this version comes from the community ❤️. Here are few examples.

- During OHBM we've been asked to support archives as a dicom input, it's part of Dcm2bids 3.1.0. Check `dcm2bids --help` output. [link](https://unfmontreal.github.io/Dcm2Bids/3.1.0/tutorial/first-steps/#running-dcm2bids)
- While helping people on Neurostars, [@smeisler](https://github.com/smeisler) indicates that he needed to run pydeface after dcm2bids conversion since he needed both versions before and after defacing, it's now part of Dcm2bids 3.1.0. Check custom_entities in post-op section. [link](https://unfmontreal.github.io/Dcm2Bids/3.1.0/how-to/use-advanced-commands/#post_op)
- If you want to speed up dcm2bids conversion [@SamGuay](https://github.com/SamGuay) wrote a really nice [tutorial](https://unfmontreal.github.io/Dcm2Bids/3.1.0/tutorial/parallel/) to convert your data faster than ever.

Your questions and concerns remain our top priority and continue to shape the future of Dcm2bids!

Thank you
Arnaud and Sam

We would like to thank [@smeisler](https://github.com/smeisler), [@Remi-Gau](https://github.com/Remi-Gau), [@raniaezzo](https://github.com/raniaezzo), [@arokem](https://github.com/arokem) and the users from [neurostars](https://neurostars.org/tag/dcm2bids) for their feedbacks.

### What's Changed

- [MAINT] validate citation.cff by [@Remi-Gau](https://github.com/Remi-Gau) in [#257](https://github.com/UNFmontreal/Dcm2Bids/pull/257)
- Bump gitpython from 3.1.32 to 3.1.34 by [@dependabot](https://github.com/dependabot) in [#259](https://github.com/UNFmontreal/Dcm2Bids/pull/259)
- Bump gitpython from 3.1.34 to 3.1.35 by [@dependabot](https://github.com/dependabot) in [#261](https://github.com/UNFmontreal/Dcm2Bids/pull/261)
- Fix typos in scaffold files by [@SamGuay](https://github.com/SamGuay) in [#263](https://github.com/UNFmontreal/Dcm2Bids/pull/263)
- [ENH] Add possibility to input dicom tar or zip archives by [@arnaudbore](https://github.com/arnaudbore) in [#262](https://github.com/UNFmontreal/Dcm2Bids/pull/262)
- Fix post op - pydeface by [@arnaudbore](https://github.com/arnaudbore) in [#260](https://github.com/UNFmontreal/Dcm2Bids/pull/260)
- Fix release tags in GHA by [@SamGuay](https://github.com/SamGuay) in [#266](https://github.com/UNFmontreal/Dcm2Bids/pull/266)
- Release 3.0.3 by [@arnaudbore](https://github.com/arnaudbore) in [#265](https://github.com/UNFmontreal/Dcm2Bids/pull/265)
- [ENH] - Automate help message in doc by [@SamGuay](https://github.com/SamGuay) in [#267](https://github.com/UNFmontreal/Dcm2Bids/pull/267)
- [DOC] - Tutorial on parallel x dcm2bids by [@SamGuay](https://github.com/SamGuay) in [#268](https://github.com/UNFmontreal/Dcm2Bids/pull/268)

**Full Changelog**: [3.0.2...3.1.0](https://github.com/UNFmontreal/Dcm2Bids/compare/3.0.2...3.1.0)

## [3.0.2](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/3.0.2) - 2023-31-23

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.2)

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.2)

First of all thank you to everybody who came see our poster during OHBM 2023 in Montreal !

We listened to you and we added an option to reorganize your NIFTIs into a BIDS structure. Check this [link](https://unfmontreal.github.io/Dcm2Bids/3.0.1/how-to/use-advanced-commands/#-skip_dcm2niix).
We also extended the possibilities provided by the item sidecar_changes.

Congrats 🥳

### What's Changed

- codespell: add config and action to codespell the code to avoid known typos by [@yarikoptic](https://github.com/yarikoptic) in [#245](https://github.com/UNFmontreal/Dcm2Bids/pull/245)
- Bump certifi from 2023.5.7 to 2023.7.22 by [@dependabot](https://github.com/dependabot) in [#247](https://github.com/UNFmontreal/Dcm2Bids/pull/247)
- Bring all 3 Arnauds into 1 by [@yarikoptic](https://github.com/yarikoptic) in [#246](https://github.com/UNFmontreal/Dcm2Bids/pull/246)
- Add option to skip_dcm2niix and reorganize NIFTI and JSON files by [@arnaudbore](https://github.com/arnaudbore) in [#248](https://github.com/UNFmontreal/Dcm2Bids/pull/248)
- Allowing Numericals in JSON custom fields by [@smeisler](https://github.com/smeisler) in [#250](https://github.com/UNFmontreal/Dcm2Bids/pull/250)
- Bump gitpython from 3.1.31 to 3.1.32 by [@dependabot](https://github.com/dependabot) in [#251](https://github.com/UNFmontreal/Dcm2Bids/pull/251)

### New Contributors

- [@yarikoptic](https://github.com/yarikoptic) made their first contribution in [#245](https://github.com/UNFmontreal/Dcm2Bids/pull/245)
- [@dependabot](https://github.com/dependabot) made their first contribution in [#247](https://github.com/UNFmontreal/Dcm2Bids/pull/247)

**Full Changelog**: [3.0.1...3.0.2](https://github.com/UNFmontreal/Dcm2Bids/compare/3.0.1...3.0.2)

## [3.0.1](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/3.0.1) - 2023-07-23

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.1)

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.1)

We could not be more proud of the 3.0.1 dcm2bids release 😊 . We put everything we've learned from our past experiences and listen to all our users' ideas into this version.

Advanced searching criterias such as extractors combined with custom entities, the ability to compare floats or the auto_extract_entities option directly accessible from dcm2bids command will make the conversion to BIDS smoother than ever and significantly reduce the complexity and the length of your configuration file especially for multi-site acquisitions.

We highly encourage you to dive into the [documentation](https://unfmontreal.github.io/Dcm2Bids/3.0.1) since we added quite a lot of new features.

Please don't hesitate to give us your feedback using this [#240](https://github.com/UNFmontreal/Dcm2Bids/discussions/240).

Thank you again for all our users who contributed in some ways to this release. Thank you [@SamGuay](https://github.com/SamGuay) for the long discussions and late debug sessions. 🎉

Arnaud

### What's Changed

- [DOC] fix typo and add detail about entity reordering by [@Remi-Gau](https://github.com/Remi-Gau) in [#183](https://github.com/UNFmontreal/Dcm2Bids/pull/183)
- update version to match release by [@SamGuay](https://github.com/SamGuay) in [#185](https://github.com/UNFmontreal/Dcm2Bids/pull/185)
- [ENH] Refactorisation - Major API upgrade by [@arnaudbore](https://github.com/arnaudbore) in [#200](https://github.com/UNFmontreal/Dcm2Bids/pull/200)
- Get README from bids toolkit by [@arnaudbore](https://github.com/arnaudbore) in [#201](https://github.com/UNFmontreal/Dcm2Bids/pull/201)
- Add bids-validator option by [@arnaudbore](https://github.com/arnaudbore) in [#206](https://github.com/UNFmontreal/Dcm2Bids/pull/206)
- Upgrade feature Intended for by [@arnaudbore](https://github.com/arnaudbore) in [#207](https://github.com/UNFmontreal/Dcm2Bids/pull/207)
- [ENH] Upgrade custom entities by [@arnaudbore](https://github.com/arnaudbore) in [#208](https://github.com/UNFmontreal/Dcm2Bids/pull/208)
- [FIX] Broken scaffold no more by [@SamGuay](https://github.com/SamGuay) in [#209](https://github.com/UNFmontreal/Dcm2Bids/pull/209)
- [FIX,ENH] - Improve dcm2bids_helper mod by [@SamGuay](https://github.com/SamGuay) in [#210](https://github.com/UNFmontreal/Dcm2Bids/pull/210)
- Generalization of sidecarchanges using ids by [@arnaudbore](https://github.com/arnaudbore) in [#213](https://github.com/UNFmontreal/Dcm2Bids/pull/213)
- [ENH] dataType -> datatype and modalityLabel -> suffix by [@arnaudbore](https://github.com/arnaudbore) in [#214](https://github.com/UNFmontreal/Dcm2Bids/pull/214)
- Fix log n version by [@SamGuay](https://github.com/SamGuay) in [#219](https://github.com/UNFmontreal/Dcm2Bids/pull/219)
- [BF] valid participant by [@arnaudbore](https://github.com/arnaudbore) in [#215](https://github.com/UNFmontreal/Dcm2Bids/pull/215)
- Allow a criteria item to be a dict with a key - any (or) or all (and) by [@arnaudbore](https://github.com/arnaudbore) in [#217](https://github.com/UNFmontreal/Dcm2Bids/pull/217)
- Add an option to use duplicates instead of runs as suggested in heudiconv project. by [@arnaudbore](https://github.com/arnaudbore) in [#218](https://github.com/UNFmontreal/Dcm2Bids/pull/218)
- [BF] Valid session by [@arnaudbore](https://github.com/arnaudbore) in [#222](https://github.com/UNFmontreal/Dcm2Bids/pull/222)
- add test helper by [@arnaudbore](https://github.com/arnaudbore) in [#220](https://github.com/UNFmontreal/Dcm2Bids/pull/220)
- [BF] dcm2bids_scaffold by [@arnaudbore](https://github.com/arnaudbore) in [#224](https://github.com/UNFmontreal/Dcm2Bids/pull/224)
- prevent doc deployment by pushing to master by [@SamGuay](https://github.com/SamGuay) in [#226](https://github.com/UNFmontreal/Dcm2Bids/pull/226)
- [ENH] Add major OS executables on new release by [@SamGuay](https://github.com/SamGuay) in [#221](https://github.com/UNFmontreal/Dcm2Bids/pull/221)
- [ENH] Generalization of defaceTpl to post_op by [@arnaudbore](https://github.com/arnaudbore) in [#225](https://github.com/UNFmontreal/Dcm2Bids/pull/225)
- [ENH] Rename all cap var by [@arnaudbore](https://github.com/arnaudbore) in [#227](https://github.com/UNFmontreal/Dcm2Bids/pull/227)
- Revert doc to 2.1.9 by [@arnaudbore](https://github.com/arnaudbore) in [#228](https://github.com/UNFmontreal/Dcm2Bids/pull/228)
- Automated version-control documentation for 2.1.9 and up by [@SamGuay](https://github.com/SamGuay) in [#231](https://github.com/UNFmontreal/Dcm2Bids/pull/231)
- Fix GHA for docs + layouts by [@SamGuay](https://github.com/SamGuay) in [#234](https://github.com/UNFmontreal/Dcm2Bids/pull/234)
- [ENH] Add float comparison by [@arnaudbore](https://github.com/arnaudbore) in [#229](https://github.com/UNFmontreal/Dcm2Bids/pull/229)
- [Quick Fix] Add specific message when no acquisition was found by [@arnaudbore](https://github.com/arnaudbore) in [#235](https://github.com/UNFmontreal/Dcm2Bids/pull/235)
- Fix typo src_file dst_file by [@arnaudbore](https://github.com/arnaudbore) in [#236](https://github.com/UNFmontreal/Dcm2Bids/pull/236)
- Improve doc for v3.0.0 by [@arnaudbore](https://github.com/arnaudbore) in [#223](https://github.com/UNFmontreal/Dcm2Bids/pull/223)
- [FIX] - update the alias for dev and latest by [@SamGuay](https://github.com/SamGuay) in [#237](https://github.com/UNFmontreal/Dcm2Bids/pull/237)
- Quick fix version by [@arnaudbore](https://github.com/arnaudbore) in [#238](https://github.com/UNFmontreal/Dcm2Bids/pull/238)
- Update docs by [@smeisler](https://github.com/smeisler) in [#239](https://github.com/UNFmontreal/Dcm2Bids/pull/239)
- [BF] fix sidecars suggested by Sam by [@arnaudbore](https://github.com/arnaudbore) in [#243](https://github.com/UNFmontreal/Dcm2Bids/pull/243)

### New Contributors

- [@Remi-Gau](https://github.com/Remi-Gau) made their first contribution in [#183](https://github.com/UNFmontreal/Dcm2Bids/pull/183)
- [@smeisler](https://github.com/smeisler) made their first contribution in [#239](https://github.com/UNFmontreal/Dcm2Bids/pull/239)

**Full Changelog**: [2.1.9...3.0.1](https://github.com/UNFmontreal/Dcm2Bids/compare/2.1.9...3.0.1)

## [3.0.0rc1](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/3.0.0rc1) - 2023-07-17

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.0rc1)

[](https://github.com/UNFmontreal/Dcm2Bids/releases/edit/3.0.0rc1)

Ok let's be clear after working very hard on this we are definitively biased so we decided to ask ChatGPT to write for us a short fun description for our brand new version.

Introducing the latest version of dcm2bids: the superhero of medical imaging data conversion! With simplified configuration, enhanced DICOM handling, comprehensive data validation, advanced options, and amazing new features, dcm2bids will transform your data into BIDS format like magic. Join the fun and unleash your scientific superpowers today!

Please check the documentation 🎉

⚠️This is a release candidate.

### What's Changed

- [DOC] fix typo and add detail about entity reordering by [@Remi-Gau](https://github.com/Remi-Gau) in [#183](https://github.com/UNFmontreal/Dcm2Bids/pull/183)
- update version to match release by [@SamGuay](https://github.com/SamGuay) in [#185](https://github.com/UNFmontreal/Dcm2Bids/pull/185)
- [ENH] Refactorisation - Major API upgrade by [@arnaudbore](https://github.com/arnaudbore) in [#200](https://github.com/UNFmontreal/Dcm2Bids/pull/200)
- Get README from bids toolkit by [@arnaudbore](https://github.com/arnaudbore) in [#201](https://github.com/UNFmontreal/Dcm2Bids/pull/201)
- Add bids-validator option by [@arnaudbore](https://github.com/arnaudbore) in [#206](https://github.com/UNFmontreal/Dcm2Bids/pull/206)
- Upgrade feature Intended for by [@arnaudbore](https://github.com/arnaudbore) in [#207](https://github.com/UNFmontreal/Dcm2Bids/pull/207)
- [ENH] Upgrade custom entities by [@arnaudbore](https://github.com/arnaudbore) in [#208](https://github.com/UNFmontreal/Dcm2Bids/pull/208)
- [FIX] Broken scaffold no more by [@SamGuay](https://github.com/SamGuay) in [#209](https://github.com/UNFmontreal/Dcm2Bids/pull/209)
- [FIX,ENH] - Improve dcm2bids_helper mod by [@SamGuay](https://github.com/SamGuay) in [#210](https://github.com/UNFmontreal/Dcm2Bids/pull/210)
- Generalization of sidecarchanges using ids by [@arnaudbore](https://github.com/arnaudbore) in [#213](https://github.com/UNFmontreal/Dcm2Bids/pull/213)
- [ENH] dataType -> datatype and modalityLabel -> suffix by [@arnaudbore](https://github.com/arnaudbore) in [#214](https://github.com/UNFmontreal/Dcm2Bids/pull/214)
- Fix log n version by [@SamGuay](https://github.com/SamGuay) in [#219](https://github.com/UNFmontreal/Dcm2Bids/pull/219)
- [BF] valid participant by [@arnaudbore](https://github.com/arnaudbore) in [#215](https://github.com/UNFmontreal/Dcm2Bids/pull/215)
- Allow a criteria item to be a dict with a key - any (or) or all (and) by [@arnaudbore](https://github.com/arnaudbore) in [#217](https://github.com/UNFmontreal/Dcm2Bids/pull/217)
- Add an option to use duplicates instead of runs as suggested in heudiconv project. by [@arnaudbore](https://github.com/arnaudbore) in [#218](https://github.com/UNFmontreal/Dcm2Bids/pull/218)
- [BF] Valid session by [@arnaudbore](https://github.com/arnaudbore) in [#222](https://github.com/UNFmontreal/Dcm2Bids/pull/222)
- add test helper by [@arnaudbore](https://github.com/arnaudbore) in [#220](https://github.com/UNFmontreal/Dcm2Bids/pull/220)
- [BF] dcm2bids_scaffold by [@arnaudbore](https://github.com/arnaudbore) in [#224](https://github.com/UNFmontreal/Dcm2Bids/pull/224)
- prevent doc deployment by pushing to master by [@SamGuay](https://github.com/SamGuay) in [#226](https://github.com/UNFmontreal/Dcm2Bids/pull/226)
- [ENH] Add major OS executables on new release by [@SamGuay](https://github.com/SamGuay) in [#221](https://github.com/UNFmontreal/Dcm2Bids/pull/221)
- [ENH] Generalization of defaceTpl to post_op by [@arnaudbore](https://github.com/arnaudbore) in [#225](https://github.com/UNFmontreal/Dcm2Bids/pull/225)
- [ENH] Rename all cap var by [@arnaudbore](https://github.com/arnaudbore) in [#227](https://github.com/UNFmontreal/Dcm2Bids/pull/227)
- Revert doc to 2.1.9 by [@arnaudbore](https://github.com/arnaudbore) in [#228](https://github.com/UNFmontreal/Dcm2Bids/pull/228)
- Automated version-control documentation for 2.1.9 and up by [@SamGuay](https://github.com/SamGuay) in [#231](https://github.com/UNFmontreal/Dcm2Bids/pull/231)
- Fix GHA for docs + layouts by [@SamGuay](https://github.com/SamGuay) in [#234](https://github.com/UNFmontreal/Dcm2Bids/pull/234)
- [ENH] Add float comparison by [@arnaudbore](https://github.com/arnaudbore) in [#229](https://github.com/UNFmontreal/Dcm2Bids/pull/229)
- [Quick Fix] Add specific message when no acquisition was found by [@arnaudbore](https://github.com/arnaudbore) in [#235](https://github.com/UNFmontreal/Dcm2Bids/pull/235)
- Fix typo src_file dst_file by [@arnaudbore](https://github.com/arnaudbore) in [#236](https://github.com/UNFmontreal/Dcm2Bids/pull/236)
- Improve doc for v3.0.0 by [@arnaudbore](https://github.com/arnaudbore) in [#223](https://github.com/UNFmontreal/Dcm2Bids/pull/223)

### New Contributors

- [@Remi-Gau](https://github.com/Remi-Gau) made their first contribution in [#183](https://github.com/UNFmontreal/Dcm2Bids/pull/183)

**Full Changelog**: [2.1.8...3.0.0rc1](https://github.com/UNFmontreal/Dcm2Bids/compare/2.1.8...3.0.0rc1)

## **2.1.9 - 2022-06-17**

Some issues with pypi. Sorry for this.

### **What's Changed**

* Fix if dot in dcm files names by[ @arnaudbore](https://github.com/arnaudbore) in[ #169](https://github.com/UNFmontreal/Dcm2Bids/pull/169)
* Support output_dir override[ #170](https://github.com/UNFmontreal/Dcm2Bids/issues/170) by[ @GMerakis](https://github.com/GMerakis) in[ #171](https://github.com/UNFmontreal/Dcm2Bids/pull/171)
* BF - forgot bval bvec by[ @arnaudbore](https://github.com/arnaudbore) in[ #172](https://github.com/UNFmontreal/Dcm2Bids/pull/172)

### **New Contributors**

* [@GMerakis](https://github.com/GMerakis) made their first contribution in[ #171](https://github.com/UNFmontreal/Dcm2Bids/pull/171)

**Full Changelog**:[ 2.1.7...2.1.9](https://github.com/UNFmontreal/Dcm2Bids/compare/2.1.7...2.1.9)

## **2.1.8 - 2022-06-17**

This will be our last PR before moving to a new API.

### **What's Changed**

* Fix if dot in dcm files names by[ @arnaudbore](https://github.com/arnaudbore) in[ #169](https://github.com/UNFmontreal/Dcm2Bids/pull/169)
* Support output_dir override[ #170](https://github.com/UNFmontreal/Dcm2Bids/issues/170) by[ @GMerakis](https://github.com/GMerakis) in[ #171](https://github.com/UNFmontreal/Dcm2Bids/pull/171)
* BF - forgot bval bvec by[ @arnaudbore](https://github.com/arnaudbore) in[ #172](https://github.com/UNFmontreal/Dcm2Bids/pull/172)

### **New Contributors**

* [@GMerakis](https://github.com/GMerakis) made their first contribution in[ #171](https://github.com/UNFmontreal/Dcm2Bids/pull/171)

**Full Changelog**:[ 2.1.7...2.1.8](https://github.com/UNFmontreal/Dcm2Bids/compare/2.1.7...2.1.8)

## 2.1.7 - 2022-05-30

Last version before refactoring.

- Major and minor documentation fixes
- Fix Ìntended for
- Fix Entity table order
- Fix Windows paths
- Fix issue when no internet
- Remove support to Python 2.6

## 2.1.6 - 2021-02-16

- New Containers
- Fix pypi package

## 2.1.5 - 2021-01-04

- Add possibility to be not case sensitive
- Fix issue 34: dcm2bids not ordering runs chronologically

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

- The anonymizer option no longer exists from the script dcm2bids. It is still possible to deface the anatomical nifti images using the "defaceTpl" key in the configuration file.
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
