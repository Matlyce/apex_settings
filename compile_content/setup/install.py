import os
import zipfile
import getpass
import os
import ctypes
import os, winshell
from win32com.client import Dispatch
from sys import exit
import sys

###################
# FUNCTIONS UTILS #
###################

def resource_path(relative_path):
    """ Get absolute path to resource, works for both development and one-file mode """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def create_shortcut(target_path, shortcut_path, working_directory, icon_path=None):
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = working_directory
        shortcut.IconLocation = icon_path
        shortcut.save()
    except Exception as e:
        print("Error while creating shortcut: " + str(e))

def run_as_admin():
    # Get the script file path
    script_path = os.path.abspath(__file__)

    # request admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)    

if ctypes.windll.shell32.IsUserAnAdmin():
    print("Running with admin rights.")
else:
    print("Requesting admin rights...")
    run_as_admin()
    exit(0)

try:
    ###################
    # MENDATORY PATHS #
    ###################
    START_MENU_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    PROGRAM_FILES_PATH = os.environ['PROGRAMFILES']
    PROGRAM_FILES_X86_PATH = os.environ['PROGRAMFILES(X86)']
    DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    BINARY_APP_NAME = resource_path("app.bytes")

    TEMP_DIR = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Temp\\apex_settings"
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    ##############################
    # START INSTALLATION PROCESS #
    ##############################

    # read BINARY_APP_NAME (bytes file)
    data = None
    with open(BINARY_APP_NAME, 'rb') as f:
        data = f.read()

    # convert the bytes to a zip file
    with open(os.path.join(TEMP_DIR, "apex_total.zip"), "wb") as f:
        f.write(data)

    print("Application uncrypted.")

    # create future install folder
    # check if PROGRAM_FILES_PATH exists
    selected_installation_path = None

    if os.path.exists(PROGRAM_FILES_PATH):
        if not os.path.exists(os.path.join(PROGRAM_FILES_PATH, "ApexSettings")):
            os.makedirs(os.path.join(PROGRAM_FILES_PATH, "ApexSettings"))
        selected_installation_path = os.path.join(PROGRAM_FILES_PATH, "ApexSettings")
    elif os.path.exists(PROGRAM_FILES_X86_PATH):
        if not os.path.exists(os.path.join(PROGRAM_FILES_X86_PATH, "ApexSettings")):
            os.makedirs(os.path.join(PROGRAM_FILES_X86_PATH, "ApexSettings"))
        selected_installation_path = os.path.join(PROGRAM_FILES_X86_PATH, "ApexSettings")
    elif os.path.exists(START_MENU_PATH):
        if not os.path.exists(os.path.join(START_MENU_PATH, "ApexSettings")):
            os.makedirs(os.path.join(START_MENU_PATH, "ApexSettings"))
        selected_installation_path = os.path.join(START_MENU_PATH, "ApexSettings")

    if selected_installation_path is None:
        print("Could not find a suitable installation path.")
        print("Please contact the developer.")
        exit(1)

    print("Selected installation path: " + str(selected_installation_path))

    # unzip the zip file
    with zipfile.ZipFile(os.path.join(TEMP_DIR, "apex_total.zip"), 'r') as zipf:
        zipf.extractall(selected_installation_path)

    print("Application successfully extracted to " + str(selected_installation_path))

    # delete the zip file
    os.remove(os.path.join(TEMP_DIR, "apex_total.zip"))
    print("Zip file successfully deleted.")

    # create desktop shortcut
    create_shortcut(os.path.join(selected_installation_path, "app.exe"), os.path.join(DESKTOP_PATH, "ApexSettings.lnk"), selected_installation_path, os.path.join(selected_installation_path, "logo.ico"))
    print("Desktop shortcut successfully created.")

    # create start menu shortcut
    create_shortcut(os.path.join(selected_installation_path, "app.exe"), os.path.join(START_MENU_PATH, "ApexSettings", "ApexSettings.lnk"), selected_installation_path, os.path.join(selected_installation_path, "logo.ico"))
    print("Start menu shortcut successfully created.")

except Exception as e:
    print("Error while installing: " + str(e))