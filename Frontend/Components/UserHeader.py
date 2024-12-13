import os
import re
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont
from Frontend.Screens.LogPage import LogPage

class UserHeader(QWidget):
    def __init__(self, parent, homepage=None):
        super().__init__()
        self.parent = parent
        self.username = self.getUsername()
        self.manifest, self.manifest_name = self.getManifestData()
        self.home_page = homepage
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.userLabel = QLabel(f"User: {self.username}")
        self.userLabel.setFont(QFont("Roboto", 16))
        self.userLabel.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        layout.addWidget(self.userLabel)

        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        if self.manifest and self.manifest_name:
            self.upload_button = QPushButton(f"Manifest: {self.manifest_name}")
        else:
            self.upload_button = QPushButton("Upload Manifest")

        self.upload_button.setFont(QFont("Roboto", 14))
        self.upload_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        self.upload_button.clicked.connect(self.openFileDialog)
        layout.addWidget(self.upload_button)

        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        log_button = QPushButton("Log")
        log_button.setFont(QFont("Roboto", 14))
        log_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        log_button.clicked.connect(self.goToLog)
        layout.addWidget(log_button)

        sign_out_button = QPushButton("Sign In")
        sign_out_button.setFont(QFont("Roboto", 14))
        sign_out_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        sign_out_button.clicked.connect(self.signOut)
        layout.addWidget(sign_out_button)

        close_year_button = QPushButton("Close Down")
        close_year_button.setFont(QFont("Roboto", 14))
        close_year_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        close_year_button.clicked.connect(self.signOut)
        layout.addWidget(close_year_button)

        self.setLayout(layout)

    # Updates the username label when the page is shown
    def showEvent(self, event):
        super().showEvent(event)
        self.updateUsername()

    # Signs out the user and clears the username input
    def signOut(self):
        username = self.getUsername()
        self.parent.add_log_entry(f"{username} signed out")
        self.parent.sign_in_page.clearUsernameInput()
        self.parent.db.update_by_id("profile", "id", 1, {"username": "Default", "currentTab": "SignIn"})
        self.parent.setCurrentIndex(0)
    
    # Updates the username label with the current username
    def updateUsername(self):
        self.username = self.getUsername()
        self.userLabel.setText(f"User: {self.username}")

    # Fetches the username from the database
    def getUsername(self):
        return self.parent.fetch_username()

    # Fetches the manifest data from the database
    def getManifestData(self):
        data, name = self.parent.fetch_manifest()
        return data, name

    # Resets the manifest data
    def resetManifest(self):
        self.manifest = None
        self.manifest_name = None
        self.upload_button.setText("Upload Manifest")
        self.home_page.updateButtons(0)

    # Opens the log page
    def goToLog(self):
        log = LogPage(self.parent)
        log.exec_()

    # Opens a file dialog to select a manifest file
    def openFileDialog(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Manifest File", "", "All Files (*);;Text Files (*.txt)", options=options)

        if file:
            try:
                file_name = os.path.basename(file)

                with open(file, 'r') as f:
                    manifestData = []
                    for line in f:
                        parsedLine = re.findall(r'\[[^\]]+\]|\{[^\}]+\}|\w+(?: \w+)*', line)
                        for item in parsedLine:
                            manifestData.append(item)

                self.parent.db.update_by_id("Lists", "id", 1, {"Manifest": str(manifestData), "ManifestName": file_name})

                self.upload_button.setText(f"Manifest: {file_name}")
                username = self.getUsername()
                print(f"Manifest file selected: {file_name}")
                self.parent.add_log_entry(f"{username} uploaded {file_name}")
                print(f"Manifest data saved to the database.")
                if self.home_page is not None:
                    self.home_page.updateButtons(1)
            except Exception as e:
                print(f"Error reading or processing the file: {e}")

