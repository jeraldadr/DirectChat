"""
Profile.py
"""
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9
import json
from pathlib import Path
import ds_messenger


class DsuFileError(Exception):
    """raised for dsu file error"""


class DsuProfileError(Exception):
    """raised for dsu profile error"""


class Profile:

    """
    The Profile class exposes the properties required to join
    an ICS 32 DSU server. You will need to use this class to
    manage the information provided by each new user created
    within your program for a2. Pay close attention to the properties and
    functions in this class as you will need to make use of
    each of them in your program. When creating your program
    you will need to collect user input for the properties exposed
    by this class. A Profile class should ensure that
    a username and password are set, but contains no conventions
    to do so. You should make sure that your code
    verifies that required properties are set.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
        self.messages = []
        self.friends = []

    def save_profile(self, path: str) -> None:
        """saves_profile into the file"""
        path_file = Path(path)

        if path_file.exists() and path_file.suffix == '.dsu':
            try:
                with open(path_file, 'w', encoding='utf-8') as file_f:
                    json.dump(self.__dict__, file_f)
            except Exception as ex:
                raise DsuFileError("Error while attempting to " +
                                   "process the DSU file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """loads the profile"""
        file_path = Path(path)

        if file_path.exists() and file_path.suffix == '.dsu':
            try:
                with open(file_path, 'r', encoding='utf-8') as file_f:
                    obj = json.load(file_f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.token = obj['token']
                    self.messages = obj['messages']
                    self.friends = obj['friends']
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()

    def save_messages(self):
        """saves messages to profile"""
        user_msg = ds_messenger.DirectMessenger(dsuserver=self.dsuserver,
                                                username=self.username,
                                                password=self.password)
        self.messages = []
        self.messages = user_msg.retrieve_all()
