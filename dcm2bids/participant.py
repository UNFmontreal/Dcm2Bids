# -*- coding: utf-8 -*-

"""Participant class"""

from os.path import join as opj

from dcm2bids.utils.utils import DEFAULT


class Participant(object):
    """ Class representing a participant

    Args:
        name (str): Label of your participant
        session (str): Optional label of a session
    """

    def __init__(self, name, session=DEFAULT.session):
        self._name = ""
        self._session = ""

        self.name = name
        self.session = session

    @property
    def name(self):
        """
        Returns:
            A string 'sub-<subject_label>'
        """
        return self._name

    @name.setter
    def name(self, name):
        """ Prepend 'sub-' if necessary"""
        if name.startswith("sub-"):
            self._name = name
        else:
            self._name = "sub-" + name

        if not self._name.replace('sub-', '').isalnum():
            raise NameError(f"Participant '{self._name.replace('sub-', '')}' "
                            "should contains only alphanumeric characters.")

    @property
    def session(self):
        """
        Returns:
            A string 'ses-<session_label>'
        """
        return self._session

    @session.setter
    def session(self, session):
        """ Prepend 'ses-' if necessary"""
        if session.strip() == "":
            self._session = ""

        elif session.startswith("ses-"):
            self._session = session

        else:
            self._session = "ses-" + session

        if not self._session.replace('ses-', '').isalnum() and self._session:
            raise NameError(f"Session '{self._session.replace('ses-', '')}' "
                            "should contains only alphanumeric characters.")

    @property
    def directory(self):
        """ The directory of the participant

        Returns:
            A path 'sub-<subject_label>' or
            'sub-<subject_label>/ses-<session_label>'
        """
        if self.hasSession():
            return opj(self.name, self.session)
        else:
            return self.name

    @property
    def prefix(self):
        """ The prefix to build filenames

        Returns:
            A string 'sub-<subject_label>' or
            'sub-<subject_label>_ses-<session_label>'
        """
        if self.hasSession():
            return self.name + "_" + self.session
        else:
            return self.name

    def hasSession(self):
        """ Check if a session is set

        Returns:
            Boolean
        """
        return self.session.strip() != DEFAULT.session
