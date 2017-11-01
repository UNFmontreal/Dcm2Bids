"""
            if self.selectseries and not self.sidecars[sidecar]["seriesnum"] in self.selectseries:
                continue
            self.sidecars[sidecar]["header"] = load_json(sidecar)
            self._sidecar = self.sidecars[sidecar]
            if self._respect(self.descriptions[index]["criteria"]):
                self.logger.debug("Description %d matches sidecar %s\n",sidecar)
                if "customHeader" in self.descriptions[index]:
                    self.sidecars[sidecar]["header"].update(
                        self.descriptions[index]["customHeader"])
                    save_json(self.sidecars[sidecar]["header"], sidecar)
                    # attempt to correct nifti header if a field has been
                    # changed that affects it
                    if "RepetitionTime" in self.descriptions[index]["customHeader"]:
                        self.logger.info(
                            "RepetitionTime field is changed to %.2f in " \
                            "description, updating nifti header to match...",
                            self.descriptions[index]["customHeader"]["RepetitionTime"])
                        try:
                            import nibabel
                            # load up the nifti and re-write the header
                            # see also:
                            # https://groups.google.com/d/msg/bids-discussion/jPVb-4Ah29A/fB52S8ExBgAJ
                            niftipath = splitext_(sidecar)[0] + '.nii'
                            if not os.path.exists(niftipath):
                                niftipath += '.gz'
                            ni = nibabel.load(niftipath)
                            ni.header['pixdim'][4] = self.descriptions[index]["customHeader"]["RepetitionTime"]
                            # ugly but necessary because the above fix may not
                            # always work (all method because numpy does not
                            # work reliably with python builtin function)
                            assert (ni.header['xyzt_units'] == 10).all(), \
                                "sequences with non-standard xyzt_units field "\
                                "are currently unsupported"

                            ni.to_filename(niftipath)
                            self.logger.info("updated header successfully.")
                        except ImportError:
                            self.logger.warning("nibabel is unavailable, unable to "\
                                           "fix nifti-sidecar mismatch")
                        except:
                            raise
"""
