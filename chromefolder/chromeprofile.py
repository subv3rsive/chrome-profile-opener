import subprocess
import os
import re
import time
import requests
import json
import random

class ProfileHandler(object):
    """Class to Manage Profiles."""

    def __init__(self, chrome_exe_path, chrome_user_data):
        """Initialize the object."""

        self.chrome_user_data = os.path.expandvars(chrome_user_data)
        self.chrome_exe_path = chrome_exe_path
        self.profiles = []

    def scan_profiles(self):
        """
        Scan the chrome user data folder for profiles.
        :param chrome_user_data: The chrome user data folder.
        :return: List.
        """

        pattern = r"Profile\s(\d*)"
        prog = re.compile(pattern)

        for f in os.listdir(self.chrome_user_data):
            result = prog.match(f)
            if result:
                # rint(result.string)
                self.profiles.append(Profile(self.chrome_exe_path, self.chrome_user_data, result.string))

        profiles = sorted(self.profiles, key=lambda x: x.profile_name)
        print([profile.profile_name for p in profiles])
        return profiles

    def scan_local_state(self):
        """Scan the local state for profiles."""

        local_state = os.path.join(self.chrome_user_data, "local state")

        with open(local_state, "r") as f:
            j = json.load(f)
            profiles = []
            for p in j["profile"]["info_cache"]:


                if os.path.exists(os.path.join(self.chrome_user_data, p)):
                    #print(new_profile.print_all())
                    print("Profile folder exists")
                else:
                    print("Profile folder does not exist")
                    continue
                    mkdir(os.path.join(self.chrome_user_data, p))
                new_profile = Profile(self.chrome_exe_path, self.chrome_user_data, p)
                profiles.append(new_profile)
        profiles = sorted(profiles, key=lambda x: x.profile_name)
        print([p.profile_name for p in profiles])
        return profiles




class Profile(object):
    """Class to handle profiles."""

    def __init__(self, chrome_exe_path, chrome_user_data, profile_root):
        """Initialize the object."""

        self.chrome_user_data = os.path.expandvars(chrome_user_data)
        self.chrome_exe_path = chrome_exe_path
        self.profile_root = profile_root
        #self.preferences = self.load_preferences()
        self.profile_name = self.get_name_from_local_state()

    def print_all(self):
        """Print all info."""

        print(f"chrome_user_data {self.chrome_user_data}")
        print(f"chrome_exe_path {self.chrome_exe_path}")
        print(f"profile_root {self.profile_root}")
        print(f"profile_name {self.profile_name}")


    def load_preferences(self):
        """Get the profile preferences as JSON object."""

        preferences_path = os.path.join(self.chrome_user_data, self.profile_root, 'Preferences')
        with open(preferences_path, 'r') as f:
            preferences = json.load(f)
        return preferences

    def get_name(self):
        """Get the profile name."""

        return self.preferences["profile"]["name"]

    def get_name_from_local_state(self):
        """Get the profile name from local state."""
        with open(os.path.join(self.chrome_user_data, "local state"), "r") as f:
            j = json.load(f)
            default = j["profile"]["info_cache"][self.profile_root]["name"]
            return default

    def open(self):
        """Open the profile."""
        arg0 = self.chrome_exe_path
        arg1 = f"--profile-directory={self.profile_root}"
        #arg2 = f"--new-tab {NEW_TAB}"
        args = [arg0, arg1]
        print(args)
        print(f"Opening profile {self.profile_root}")
        subprocess.Popen(args)
