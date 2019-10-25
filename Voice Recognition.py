import time  # Used for Sleep Function
import os  # For System Commands
import re  # For Splitting
import keyboard  # Simulate Keyboard Input
import win10toast # For notifications
import subprocess # Also for system commands
import spotipy # Spotify Python API

import speech_recognition as sr  # Main SR API

from datetime import datetime # Check date
from keyboardVirtual import Keyboard  # Faked Key Presses (Different from normal module)
from googleapiclient.discovery import build # For Youtube API

r = sr.Recognizer()
notification = win10toast.ToastNotifier()
youtube = build('youtube', 'v3', developerKey="AIzaSyDu5qoUXtLVam1LytJi26Z_Is48jq0zVyM")

# Things to add
# spotify play
# spotify transfer playback

MainKeys = [["open"],
            ["close", "exit", "quit"],
            ["date", "time"],
            ["search"],
            [["shut", "down"], ["turn", "off"], ["close", "down"], ["shutdown", "turnoff", "closedown"]],
            ["restart", "reinstate", "retard"],
            ["pause", "play", "lay", "mouse"],
            ["set", "volume"],
            ["calculate", "evaluate"],
            ["next", "skip"],
            ["previous"]]

explorer_list = ["explore", "explorer", "folder"]
taskview_list = ["task", "view", "taskview"]
mword_list = ["word", "words"]
mexcel_list = ["excel", "spreadsheet"]
mpowerpoint_list = ["powerpoint"]
spotify_list = ["spotify", "music"]
browser_list = ["browser", "google", "chrome"]
search_internet_list = ["google", "youtube"]


def get_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        print("Speak Anything: ")
        audio = r.listen(source)
        # audio = r.record(source, duration=4)
        try:
            text = r.recognize_google(audio, language="EN-US")
            print("You Said: {}".format(text))
        except:
            print("Sorry could not recognize your voice")
            return
    return text.lower()


def split_command(text):
    input = text.split()
    # If multiple command
    if ("then" in input) or ("and" in input):
        input2 = re.split('then|and', text)
        for i in input2:
            parse_text(i.split())
            time.sleep(1)
    else:
        parse_text(input)


def parse_text(input):
    # Open Stuff
    if any(x in input for x in MainKeys[0]):
        open_stuff(input)
        return True
    # Close Stuff
    if any(x in input for x in MainKeys[1]):
        close_stuff(input)
        return True
    # Search on Internet
    if any(x in input for x in MainKeys[3]):
        internet_stuff(input)
        return True
    # Check Date
    if any(x in input for x in MainKeys[2]):
        check_date()
        return True
    # Shutdown Computer
    if all(x in input for x in MainKeys[4][0]) or all(x in input for x in MainKeys[4][1]) or \
    all(x in input for x in MainKeys[4][2]) or any(x in input for x in MainKeys[4][3]):
        print("Are you sure?")
        if get_audio() == "yes":
            shutdown()
        return True
    # Restart Computer
    if any(x in input for x in MainKeys[5]):
        print("Are you sure?")
        if get_audio() == "yes":
            restart()
        return True
    # Play music on Youtube
    if any(x in input for x in MainKeys[6]) and ("youtube" in input):
        play_youtube(input)
        return True
    # Pause/Play Media
    if any(x in input for x in MainKeys[6]):
        media_pause_play()
        return True
    # Set Volume
    if all(x in input for x in MainKeys[7]):
        for i in input:
            if '%' in i:
                set_volume(int(i.split('%')[0]))
        return True
    # Next Media
    if any(x in input for x in MainKeys[9]):
        next_media()
        return True
    # Prev Media
    if any(x in input for x in MainKeys[10]):
        prev_media()
        return True
    # Evaluate/Calculate
    if any(x in input for x in MainKeys[8]):
        evaluator(input)
        return True


def open_stuff(text):
    # Open Explorer
    if any(word in text for word in explorer_list):
        open_explorer()
        return True
    # Open Task View
    if all(word in text for word in taskview_list[:2]) or (taskview_list[2] in text):
        open_taskview()
        return True
    # Open Microsoft Applications (word, excel, powerpoint)
    if "microsoft" in text:
        if any(word in text for word in mword_list):
            microsoft_word()
            return True
        if any(word in text for word in mexcel_list):
            microsoft_excel()
            return True
        if any(word in text for word in mpowerpoint_list):
            microsoft_powerpoint()
            return True
    # Open Spotify
    if any(word in text for word in spotify_list):
        open_spotify()
        return True
    # Open Browser or Chrome
    if any(word in text for word in browser_list):
        open_chrome()
        return True


def close_stuff(text):
    # Close Microsoft Applications (word, excel, powerpoint)
    if "microsoft" in text:
        if any(word in text for word in mword_list):
            close_word()
            return True
        if any(word in text for word in mexcel_list):
            close_excel()
            return True
        if any(word in text for word in mpowerpoint_list):
            close_powerpoint()
            return True
    # Close Spotify
    if any(word in text for word in spotify_list):
        close_spotify()
        return True
    # Close Browser or Chrome
    if any(word in text for word in browser_list):
        close_chrome()
        return True


# Search on the internet
def internet_stuff(text):
    if "google" in text:
        search_options(text, 1)
        return True
    if "youtube" in text:
        search_options(text, 2)
        return True

# Searching (Google and Youtube)
def search_options(input, setting):
    # Getting search array
    search_array = get_SearchArray(input, setting, 1)
    seperator = "+"
    searchquery = seperator.join(search_array)
    if setting == 1:
        os.system("start www.google.com/search?q=" + searchquery)
    elif setting == 2:
        os.system("start www.youtube.com/results?search_query=" + searchquery)

# Getting Search Query
def get_SearchArray(input, setting, setting2):
    settingtype = ""
    settingtype2 = ""
    # Determines whether google/youtube search
    if setting == 1:
        settingtype = "google"
    elif setting == 2:
        settingtype = "youtube"
    elif setting == 3:
        settingtype = "spotify"
    # Determines whether search or directly click on line
    if setting2 == 1:
        settingtype2 = "search"
    elif setting2 == 2:
        settingtype2 = "play"
    # Assign settings
    startg = input.index(settingtype)
    starts = input.index(settingtype2)
    search_array = []
    if startg == (len(input) - 1):
        search_array = input[starts + 1:-2]
    elif startg > starts:
        search_array = input[startg + 1:]
    elif starts > startg:
        search_array = input[starts + 1:]
    return search_array

# Play query on Youtube
def play_youtube(text):
    # Getting search_query
    search_array = get_SearchArray(text, 2, 2)
    print(search_array)
    separator = " "
    searchquery = separator.join(search_array)
    # Getting VideoID and Playing it
    req = youtube.search().list(q=searchquery, part='snippet', type='video')
    res = req.execute()
    id = res['items'][0]['id']['videoId']
    command = "start https://youtube.com/watch?v=" + id
    os.system(command)


# Open Stuff Functions
def open_explorer():
    os.system('start explorer')
    notification.show_toast('Windows Explorer', 'Successfully opened', icon_path='icon/explorer.ico', duration=3)

def open_taskview():
    print("open taskview")
    Keyboard.keyDown(Keyboard.VK_LWIN)
    Keyboard.keyDown(Keyboard.VK_TAB)
    Keyboard.keyUp(Keyboard.VK_LWIN)
    Keyboard.keyUp(Keyboard.VK_TAB)
    notification.show_toast('Taskview', 'Successfully opened', duration=3)

def microsoft_word():
    os.system('start winword')
    time.sleep(1)
    notification.show_toast('Microsoft Word', 'Successfully opened', icon_path='icon/ms-word.ico', duration=3)

def microsoft_excel():
    os.system('start excel')
    time.sleep(1)
    notification.show_toast('Microsoft Excel', 'Successfully opened', icon_path='icon/ms-excel.ico', duration=3)

def microsoft_powerpoint():
    os.system('start powerpnt')
    time.sleep(1)
    notification.show_toast('Microsoft PowerPoint', 'Successfully opened', icon_path='icon/ms-powerpoint.ico',duration=3)

def open_spotify():
    os.system('start spotify')
    time.sleep(1)
    notification.show_toast('Spotify', 'Successfully opened', icon_path='icon/spotify.ico', duration=3)
    time.sleep(1)

def open_chrome():
    os.system('start chrome')
    time.sleep(1)
    notification.show_toast('Chrome', 'Successfully opened', icon_path='icon/chrome.ico', duration=3)
    time.sleep(1)


# Close Stuff Functions
def close_word():
    os.system('taskkill /im winword.exe /f')
    notification.show_toast('Microsoft Word', 'Successfully closed', icon_path='icon/ms-word.ico', duration=3)

def close_excel():
    os.system('taskkill /im excel.exe /f')
    notification.show_toast('Microsoft Excel', 'Successfully closed', icon_path='icon/ms-excel.ico', duration=3)

def close_powerpoint():
    os.system('taskkill /im powerpnt.exe /f')
    notification.show_toast('Microsoft PowerPoint', 'Successfully closed', icon_path='icon/ms-powerpoint.ico',
                            duration=3)

def close_spotify():
    os.system('taskkill /im spotify.exe /f')
    notification.show_toast('Spotify', 'Successfully closed', icon_path='icon/spotify.ico', duration=3)

def close_chrome():
    os.system('taskkill /im chrome.exe /f')
    notification.show_toast('Chrome', 'Chrome closed', icon_path='icon/chrome.ico', duration=3)


# System Functions
def check_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%y %H:%M")
    notification.show_toast(dt_string, "Date & Time", duration=3)

def shutdown():
    # os.system('shutdown /s')
    print("computer shutdown")

def restart():
    # os.system('shutdown /r')
    print("computer restart")

def media_pause_play():
    Keyboard.key(Keyboard.VK_MEDIA_PLAY_PAUSE)
    time.sleep(1)

def set_volume(num):
    for i in range(50):
        Keyboard.key(Keyboard.VK_VOLUME_DOWN)
    for i in range(int(num / 2)):
        Keyboard.key(Keyboard.VK_VOLUME_UP)

def next_media():
    Keyboard.key(Keyboard.VK_MEDIA_NEXT_TRACK)
    time.sleep(1)

def prev_media():
    Keyboard.key(Keyboard.VK_MEDIA_PREV_TRACK)
    Keyboard.key(Keyboard.VK_MEDIA_PREV_TRACK)
    time.sleep(1)

# Evaluate/Calculate Functions
def evaluator(exp, eval_regex=r'^(\d+|\+|-|\*|\/)$'):
    checked = []
    for i in range(len(exp)):
        if re.match(eval_regex, exp[i], re.M):
            checked.append(exp[i])
    result = str(eval("".join(checked)))
    print(result)
    notification.show_toast(result, "Result",icon_path='icon/Dtafalonso-Android-Lollipop-Calculator.ico', duration=3)


# computer play imagine dragons radioactive on youtube
# Main While Loop
# while True:
#     keyboard.wait(hotkey="k + l")
#     split_command(get_audio())

while True:
    text = input("Write Command: ")
    print("What you wrote: ", text)
    split_command(text)