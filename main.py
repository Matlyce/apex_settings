import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, pyqtSlot
import zipfile
import os
import threading
import shutil

import utils

DEBUG_MODE = False

def show_warning_popup(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle("Warning")
    msg_box.setText(message)
    msg_box.exec_()

def export_config(self, file_path, parent=None):
    if (parent is None):
        print("Parent is None!")
        return
    print("File to save:", file_path)
    # C:\Users\<user>\Saved Games\Respawn\Apex

    # Get the current user
    current_user = utils.get_current_user()
    self.update_progress.emit(utils.get_random_value_with_interval(5, 10))

    ###################
    # LOCAL APEX PART #
    ###################
    local_apex_path = f"C:\\Users\\{current_user}\\Saved Games\\Respawn\\Apex"
    # zip that folder
    utils.zip_folder_contents(local_apex_path, os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"))
    self.update_progress.emit(utils.get_random_value_with_interval(10, 20))
    # read the zip file as bytes and write it to a temp file
    with open(os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"), "rb") as f:
        data = f.read()
    local_config_temp_path = os.path.join(parent.temp_directory_path, "local-apex_folderbytes_tmp")
    # write the temp file to the file_path
    with open(local_config_temp_path, "wb") as f:
        f.write(data)

    self.update_progress.emit(utils.get_random_value_with_interval(20, 30))

    ##############################
    # APEX INSTALL LOCATION PART #
    ##############################
    install_location_apex_path = os.path.join(parent.apex_installation_path, "cfg")
    # zip that folder
    utils.zip_folder_contents(install_location_apex_path, os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"))
    self.update_progress.emit(utils.get_random_value_with_interval(30, 40))
    # read the zip file as bytes and write it to a temp file
    with open(os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"), "rb") as f:
        data = f.read()
    cfg_config_temp_path = os.path.join(parent.temp_directory_path, "cfg-apex_folderbytes_tmp")
    # write the temp file to the file_path
    with open(cfg_config_temp_path, "wb") as f:
        f.write(data)

    self.update_progress.emit(utils.get_random_value_with_interval(40, 50))

    ################################
    # MERGE THE TWO FILES TOGETHER #
    ################################
    # create a zip file
    final_zip_path = os.path.join(parent.temp_directory_path, "apex_total.zip")
    with zipfile.ZipFile(final_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # add the two files to the zip file
        zipf.write(local_config_temp_path, arcname=os.path.relpath(local_config_temp_path, parent.temp_directory_path))
        zipf.write(cfg_config_temp_path, arcname=os.path.relpath(cfg_config_temp_path, parent.temp_directory_path))
    
    self.update_progress.emit(utils.get_random_value_with_interval(50, 60))

    # read the zip file as bytes and write it to a temp file
    with open(final_zip_path, "rb") as f:
        data = f.read()

    self.update_progress.emit(utils.get_random_value_with_interval(60, 70))

    # write the temp file to the file_path
    with open(file_path, "wb") as f:
        f.write(data)

    self.update_progress.emit(utils.get_random_value_with_interval(70, 80))

    # delete the temp files
    os.remove(local_config_temp_path)
    os.remove(cfg_config_temp_path)
    self.update_progress.emit(utils.get_random_value_with_interval(80, 90))
    os.remove(os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"))
    os.remove(os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"))
    os.remove(final_zip_path)
    self.update_progress.emit(100)
    print("Done!")
    
def load_config(self, file_path, parent=None):
    if (parent is None):
        print("Parent is None!")
        return
    print("File to load:", file_path)
    # C:\Users\<user>\Saved Games\Respawn\Apex\local

    # Get the current user
    current_user = utils.get_current_user()
    current_path = os.getcwd()

    self.update_progress.emit(utils.get_random_value_with_interval(5, 10))

    ##############################
    # UNMERGE THE TWO FILES PART #
    ##############################
    # read the file_path as bytes and write it to a temp file
    with open(file_path, "rb") as f:
        data = f.read()
    self.update_progress.emit(utils.get_random_value_with_interval(10, 15))

    # convert the bytes to a zip file
    with open(os.path.join(parent.temp_directory_path, "apex_total.zip"), "wb") as f:
        f.write(data)
    self.update_progress.emit(utils.get_random_value_with_interval(15, 20))
    # extract the zip file to the path as a temp folder in the temp directory path
    if DEBUG_MODE:
        print("Extracting zip file...")
    # create the temp folder
    if not os.path.exists(os.path.join(parent.temp_directory_path, "apex_total")):
        os.makedirs(os.path.join(parent.temp_directory_path, "apex_total"))
    utils.unzip_folder_contents(os.path.join(parent.temp_directory_path, "apex_total.zip"), os.path.join(parent.temp_directory_path, "apex_total"))

    self.update_progress.emit(utils.get_random_value_with_interval(20, 30))

    ###################
    # LOCAL APEX PART #
    ###################
    if DEBUG_MODE:
        local_apex_path = os.path.join(current_path, "output", "Apex")
        # create the temp folder
        if not os.path.exists(local_apex_path):
            os.makedirs(local_apex_path)
    else:
        local_apex_path = f"C:\\Users\\{current_user}\\Saved Games\\Respawn\\Apex"
    # read the "local-apex_folderbytes_tmp" in the temp directory as bytes and write it to a temp file
    with open(os.path.join(parent.temp_directory_path, "apex_total", "local-apex_folderbytes_tmp"), "rb") as f:
        data = f.read()
    self.update_progress.emit(utils.get_random_value_with_interval(30, 40))
    # create a zip file with the bytes in the temp file
    with open(os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"), "wb") as f:
        f.write(data)
    # extract the zip file to the local apex path
    if DEBUG_MODE:
        print("Extracting zip file...")

    # create a temp folder named localapex in the temp directory
    if not os.path.exists(os.path.join(parent.temp_directory_path, "localapex")):
        os.makedirs(os.path.join(parent.temp_directory_path, "localapex"))
    # extract the zip file to the localapex folder
    utils.unzip_folder_contents(os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"), os.path.join(parent.temp_directory_path, "localapex"))
    self.update_progress.emit(utils.get_random_value_with_interval(40, 50))
    # check if videos settings isn't checked, so we can delete the "Apex/local/videoconfig.txt" file
    if not parent.centralWidget().layout().itemAt(1).widget().isChecked():
        os.remove(os.path.join(parent.temp_directory_path, "localapex", "local", "videoconfig.txt"))
    self.update_progress.emit(utils.get_random_value_with_interval(51, 53))
    # check if control settings isn't checked, so we can delete the "Apex/local/settings.cfg" file
    if not parent.centralWidget().layout().itemAt(2).widget().isChecked():
        os.remove(os.path.join(parent.temp_directory_path, "localapex", "local", "settings.cfg"))
    self.update_progress.emit(utils.get_random_value_with_interval(54, 56))

    # now we can move the localapex folder content to the local apex path
    utils.move_folder_contents(parent.temp_directory_path, os.path.join(parent.temp_directory_path, "localapex"), local_apex_path)

    # remove recursively the localapex folder
    shutil.rmtree(os.path.join(parent.temp_directory_path, "localapex"))

    self.update_progress.emit(utils.get_random_value_with_interval(56, 64))

    ##############################
    # APEX INSTALL LOCATION PART #
    ##############################
    if DEBUG_MODE:
        install_location_apex_path = os.path.join(current_path, "output", "cfg")
        # create the temp folder
        if not os.path.exists(install_location_apex_path):
            os.makedirs(install_location_apex_path)
    else:
        install_location_apex_path = os.path.join(parent.apex_installation_path, "cfg")
    # read the "cfg-apex_folderbytes_tmp" in the temp directory as bytes and write it to a temp file
    with open(os.path.join(parent.temp_directory_path, "apex_total", "cfg-apex_folderbytes_tmp"), "rb") as f:
        data = f.read()
    self.update_progress.emit(utils.get_random_value_with_interval(64, 70))
    # create a zip file with the bytes in the temp file
    with open(os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"), "wb") as f:
        f.write(data)
    self.update_progress.emit(utils.get_random_value_with_interval(70, 80))
    # extract the zip file to the local apex path
    if DEBUG_MODE:
        print("Extracting zip file...")
    utils.unzip_folder_contents(os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"), install_location_apex_path)
    self.update_progress.emit(utils.get_random_value_with_interval(80, 90))

    # delete the temp files
    os.remove(os.path.join(parent.temp_directory_path, "local-apex_folder_tmp.zip"))
    os.remove(os.path.join(parent.temp_directory_path, "cfg-apex_folder_tmp.zip"))
    os.remove(os.path.join(parent.temp_directory_path, "apex_total.zip"))
    os.remove(os.path.join(parent.temp_directory_path, "apex_total", "local-apex_folderbytes_tmp"))
    os.remove(os.path.join(parent.temp_directory_path, "apex_total", "cfg-apex_folderbytes_tmp"))
    os.rmdir(os.path.join(parent.temp_directory_path, "apex_total"))
    self.update_progress.emit(100)

"""
    self.update_progress.emit(utils.get_random_value_with_interval(5, 15))
    # read the file_path as bytes and write it to a temp file
    with open(file_path, "rb") as f:
        data = f.read()
    # convert the bytes to a zip file
    with open(os.path.join(parent.temp_directory_path, "apex.zip"), "wb") as f:
        f.write(data)
    # extract the zip file to the path to the current execution path + "output" folder
    if DEBUG_MODE:
        print("Extracting zip file...")
    utils.unzip_folder_contents(os.path.join(parent.temp_directory_path, "apex.zip"), os.path.join(parent.temp_directory_path, "output"))
    # delete the temp file
    os.remove(os.path.join(parent.temp_directory_path, "apex.zip"))
    self.update_progress.emit(100)
    print("load_config() Done!")
"""

class MainWindow(QMainWindow):
    update_progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apex Settings")
        self.setGeometry(100, 100, 400, 400)  # Set window position and size
        self.setFixedSize(400, 400)  # Make the window non-resizable
        
        self.apex_installation_path = None
        self.temp_directory_path = f"C:\\Users\\{utils.get_current_user()}\\AppData\\Local\\Temp\\apex_settings"
        if not os.path.exists(self.temp_directory_path):
            os.makedirs(self.temp_directory_path)
        
        self.setWindowIcon(QIcon("logo.ico"))

        self.setStyleSheet("background-color: white;")
        font = QFont("Helvetica", 16)
        font_id = QFontDatabase.addApplicationFont("./Apex-Black.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        title_font = QFont(font_family, 24)  # Replace "20" with the desired font size
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title_label = QLabel("CONFIG LOADER", self)
        title_label.setFont(title_font)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Create checkboxes "VIDEOS SETTINGS" and "CONTROL SETTINGS"
        videos_checkbox = QCheckBox("VIDEOS SETTINGS", self)
        control_checkbox = QCheckBox("CONTROL SETTINGS", self)
        videos_checkbox.setChecked(True)
        control_checkbox.setChecked(True)
        videos_checkbox.setFont(font)
        control_checkbox.setFont(font)
        layout.addWidget(videos_checkbox, alignment=Qt.AlignCenter)
        layout.addWidget(control_checkbox, alignment=Qt.AlignCenter)

        # PATH SELECTOR
        self.path_label = QLabel("C:\SteamLibrary\steamapps\common\Apex Legends", self)
        # center the text
        path_text_style = """
            QLabel {
                color: #808080;
                font-size: 12px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """
        self.path_label.setStyleSheet(path_text_style)
        path_font = QFont("Helvetica", 8)
        self.path_label.setFont(path_font)
        path_button = QPushButton("Browse to Apex Installation folder", self)
        path_button_style = """
            QPushButton {
                background-color: #BCBCBC; /* Green */
                border: 2px solid #9E9E9E;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #868686; /* Darker Green */
            }
            QPushButton:pressed {
                background-color: #4F4F4F; /* Even Darker Green */
            }
            QPushButton:disabled {
                background-color: #D3D3D3; /* Light Gray */
                border: 2px solid #D3D3D3; /* Light Gray */
                color: #808080; /* Dark Gray */
            }
        """
        path_button.setStyleSheet(path_button_style)
        layout.addWidget(self.path_label)
        layout.addWidget(path_button)

        # Create the title label "USER ACTIONS"
        user_actions_label = QLabel("USER ACTIONS", self)
        user_actions_label.setFont(title_font)
        layout.addWidget(user_actions_label, alignment=Qt.AlignCenter)

        # Create the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Set the range from 0 to 100 (percentage)
        self.progress_bar.setValue(0)  # Set the initial progress to 0
        # Apply custom style sheet animation to the progress bar (pulse effect)
        self.pulse_animation_style = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            @keyframes pulse {
                0% {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                      stop:0.0 #0DFF00, stop:0.5 #1DFF7E,
                                                      stop:1.0 #0DFF00);
                }
                50% {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                      stop:0.0 #1DFF7E, stop:0.5 #0DFF00,
                                                      stop:1.0 #1DFF7E);
                }
                100% {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                      stop:0.0 #0DFF00, stop:0.5 #1DFF7E,
                                                      stop:1.0 #0DFF00);
                }
            }
        """
        self.progress_bar.setStyleSheet(self.pulse_animation_style)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        self.update_progress_signal.connect(self.update_progress_bar)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()

        # Create "load" and "export" buttons
        load_button = QPushButton("Load", self)
        export_button = QPushButton("Export", self)
        load_button.setFont(font)
        export_button.setFont(font)
        button_style = """
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: 2px solid #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker Green */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Even Darker Green */
            }
            QPushButton:disabled {
                background-color: #D3D3D3; /* Light Gray */
                border: 2px solid #D3D3D3; /* Light Gray */
                color: #808080; /* Dark Gray */
            }
        """
        load_button.setStyleSheet(button_style)
        export_button.setStyleSheet(button_style)
        self.button_layout.addWidget(load_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(export_button, alignment=Qt.AlignCenter)
        layout.addLayout(self.button_layout)

        # Create the quit button at the bottom, centered
        quit_button = QPushButton("Quit", self)
        exit_button_style = """
            QPushButton {
                background-color: #FF1700;
                border: 2px solid #C91200;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C91200;
            }
            QPushButton:pressed {
                background-color: #5D1000; /* Even Darker Green */
            }
            QPushButton:disabled {
                background-color: #D3D3D3; /* Light Gray */
                border: 2px solid #D3D3D3; /* Light Gray */
                color: #808080; /* Dark Gray */
            }
        """
        quit_button.setStyleSheet(exit_button_style)
        layout.addWidget(quit_button, alignment=Qt.AlignCenter)

        # Connect the buttons to their respective functions
        load_button.clicked.connect(self.on_load)
        export_button.clicked.connect(self.on_export)
        quit_button.clicked.connect(self.on_quit)
        path_button.clicked.connect(self.on_select_path)

        # check if the path file exists
        if os.path.exists(os.path.join(self.temp_directory_path, "apex_path.txt")):
            with open(os.path.join(self.temp_directory_path, "apex_path.txt"), "r") as f:
                self.apex_installation_path = f.read()
                self.path_label.setText(self.apex_installation_path)

    def on_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Apex Config File (*.apexconfig)")
        if file_path:
            if (self.apex_installation_path is None):
                show_warning_popup("Please select your Apex Legends installation folder!")
                return
            # create a thread to run the load_config function
            self.disable_buttons()
            self.thread = WorkerLoader(self, file_path)
            self.thread.update_progress.connect(self.update_progress_signal)  # Connect the thread's signal
            self.thread.start()

    def on_export(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Apex Config File (*.apexconfig)")
        if file_path:
            if (self.apex_installation_path is None):
                show_warning_popup("Please select your Apex Legends installation folder!")
                return
            # create a thread to run the export_config function
            self.disable_buttons()
            self.thread = WorkerExporter(self, file_path)
            self.thread.update_progress.connect(self.update_progress_signal)  # Connect the thread's signal
            self.thread.start()

    @pyqtSlot(int)
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)
        self.progress_bar.setStyleSheet(self.pulse_animation_style)

    def re_enable_buttons(self):
        # enable all the buttons and checkboxes and disable the progress bar
        self.centralWidget().layout().itemAt(0).widget().setEnabled(True)
        self.centralWidget().layout().itemAt(1).widget().setEnabled(True)
        self.centralWidget().layout().itemAt(2).widget().setEnabled(True)

        self.centralWidget().layout().itemAt(4).widget().setEnabled(True)

        self.centralWidget().layout().itemAt(5).widget().setEnabled(True)
        self.centralWidget().layout().itemAt(6).widget().setEnabled(True)

        self.centralWidget().layout().itemAt(8).widget().setEnabled(True)

        if DEBUG_MODE:
            # list all the items in centralWidget's layout
            for i in range(self.centralWidget().layout().count()):
                print(f"{i} ITEM : " + str(self.centralWidget().layout().itemAt(i).widget()))

        for i in range(self.button_layout.count()):
            item = self.button_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setEnabled(True)

        print("All buttons and checkboxes re-enabled")

    def disable_buttons(self):
        # disable all the buttons and checkboxes and enable the progress bar
        self.progress_bar.setValue(0)
        self.centralWidget().layout().itemAt(0).widget().setEnabled(False)
        self.centralWidget().layout().itemAt(1).widget().setEnabled(False)
        self.centralWidget().layout().itemAt(2).widget().setEnabled(False)

        self.centralWidget().layout().itemAt(4).widget().setEnabled(False)

        self.centralWidget().layout().itemAt(5).widget().setEnabled(True)
        self.centralWidget().layout().itemAt(6).widget().setEnabled(True)

        self.centralWidget().layout().itemAt(8).widget().setEnabled(False)

        for i in range(self.button_layout.count()):
            item = self.button_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setEnabled(False)

        print("All buttons and checkboxes disabled")

    def on_select_path(self):
        selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if selected_directory:
            self.path_label.setText(str(selected_directory))
            print("Selected Directory:", selected_directory)
            self.apex_installation_path = selected_directory
            # write it into a file into the temp directory
            with open(os.path.join(self.temp_directory_path, "apex_path.txt"), "w") as f:
                f.write(selected_directory)

    def on_quit(self):
        print("Quitting...")
        app.quit()
    
class WorkerLoader(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, parent=None, file_path=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        load_config(self, self.file_path, self.parent())
        self.parent().re_enable_buttons()

class WorkerExporter(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, parent=None, file_path=None):
        super().__init__(parent)
        self.file_path = file_path

    def run(self):
        export_config(self, self.file_path, self.parent())
        self.parent().re_enable_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
