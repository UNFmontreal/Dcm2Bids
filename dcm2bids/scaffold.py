# -*- coding: utf-8 -*-

"""
    def _updatestudyfiles(self):
        # participant table
        partfile = os.path.join(self.outputdir,"participants.tsv")
        participants = read_participants(partfile)
        if not participants or not any([part["participant_id"]==self.participant.name
                                        for part in participants]):
            participants.append(
                OrderedDict(zip(("participant_id","age","sex","group"),
                                (self.participant.name,"n/a","n/a","n/a"))))
        write_participants(partfile, participants)

        # dataset description
        descfile = os.path.join(self.outputdir,'dataset_description.json')
        if not os.path.exists(descfile):
            save_json({"Name": "", "BIDSVersion": "1.0.1",
                        "License": "", "Authors": [""],
                        "Acknowledgments": "",
                        "HowToAcknowledge": "",
                        "Funding": "",
                        "ReferencesAndLinks": [""],
                        "DatasetDOI": ""}, descfile)

        # readme/change files
        readmefile = os.path.join(self.outputdir,'README')
        if not os.path.exists(readmefile):
            write_txt(readmefile)
        changefile = os.path.join(self.outputdir,'CHANGES')
        if not os.path.exists(changefile):
            write_txt(changefile,
                      ["Revision history for BIDS dataset.",
                       "",
                       "0.01 " + datetime.date.today().strftime("%Y-%m-%d"),
                       "",
                       " - Initialised study directory"])

"""
