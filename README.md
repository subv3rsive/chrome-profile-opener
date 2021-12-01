# chrome-profile-opener
Open up every chrome profile automatically.

1. Install Python >3.x

2. Edit the file and modify the following paths to reflect your system (Windows only):
```
#Path to the Chrome executable.
CHROME_EXE_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

#Path to the profile directory.
CHROME_FOLDER_PATH = r"%localappdata%\Google\Chrome\User Data"

#Number of profiles to open
NUM_PROFILES = 3
```


3. Run open-chrome-profile.py
