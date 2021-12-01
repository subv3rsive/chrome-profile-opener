import subprocess
import os
import re

# USER OPTIONS
#-----------------------------------------
# Path to the Chrome executable.
CHROME_EXE_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Path to the profile directory.
CHROME_FOLDER_PATH = r"%localappdata%\Google\Chrome\User Data"

# Number of profiles to open
NUM_PROFILES = 3

# END USER OPTIONS
#-----------------------------------------

# Expand %localappdata% into a full system path.
expanded = os.path.expandvars(CHROME_FOLDER_PATH)

# Regular expression to search for profile names in the profile directory.
pattern = r"Profile\s(\d*)"
prog = re.compile(pattern)

# Iterate through profile directory.
profiles = []
for f in os.listdir(expanded):
    result = prog.match(f)
    if result:
        print(result.string)
        profiles.append(result.string)

# Sort profiles by number.
profiles = sorted(profiles, key=lambda x: int(x.split(" ")[1]))

# Launch chrome with the profile.
count = 1
for p in profiles:
    arg = f"--profile-directory={p}"
    subprocess.check_call([CHROME_EXE_PATH, arg])

    if count >= NUM_PROFILES:
        break
        
    count += 1
