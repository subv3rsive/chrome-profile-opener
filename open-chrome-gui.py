import PySimpleGUI as sg
import subprocess
import os
import re
import time
import requests
from gettoken.gettoken import gettokens
import json
import random

from chromeprofile import ProfileHandler, Profile

# USER OPTIONS
# ----------------------------------------------------------------------------------------------------------------------
# Path to the Chrome executable.
CHROME_EXE_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Path to the profile directory.
CHROME_USER_DATA = r"%localappdata%\Google\Chrome\User Data"

# END USER OPTIONS
# ----------------------------------------------------------------------------------------------------------------------



def table_window(table):
    """
    Create a new window with profile table.
    :param table: List of rows containing profile info.
    """
    headings = ["Profile", "Name"]
    layout = [[sg.Table(values=table,
                      headings=headings,
                      max_col_width=25,
                      auto_size_columns=True,
                      select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                      justification='left',
                      key='-TABLE-',
                      tooltip='This is a table')],
              [sg.Button("Open"), sg.Button("Sort")]]
    window = sg.Window('Profile Table', layout, relative_location=(-500, -150), finalize=True)
    return window


def create_table(CHROME_USER_DATA, profiles):
    table = []
    for p in profiles:
        table.append([p.profile_root, p.profile_name])
    return table

layout = [
    [sg.Text("Chrome Path"), sg.Input(CHROME_EXE_PATH,size=(40,1), key='-CHROME_EXE_PATH-')],
    [sg.Text("Profile Path"), sg.Input(CHROME_USER_DATA, size=(40, 1), key='-CHROME_USER_DATA-')],
    [sg.Button('Scan'), sg.Button('Exit')]
]

window = sg.Window('Chrome Profile Manager', layout)
t_window = ""

table = None
while True:  # Event Loop
    print("start")
    if t_window:
        event, values = t_window.read()
        if event == "Open":
            #print(event, values)
            print(values['-TABLE-'])
            print(profiles)
            selected = [profiles[v] for v in values['-TABLE-']]
            print([s.profile_root+" "+s.profile_name for s in selected])
            for s in selected:
                s.print_all()
                time.sleep(.1)
                s.open()

    else:
        event, values = window.read()
        print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Scan":
        profile_handler = ProfileHandler(values['-CHROME_EXE_PATH-'], values['-CHROME_USER_DATA-'])
        profiles = profile_handler.scan_local_state()
        table = create_table(values['-CHROME_USER_DATA-'], profiles)
        t_window = table_window(table)



    print("test")


window.close()
