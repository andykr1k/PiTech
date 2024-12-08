import os
import re
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont
from Frontend.Screens.LogPage import LogPage

class UserHeader(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.username = self.getUsername()
        self.manifest, self.manifest_name = self.getManifestData()
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

        sign_out_button = QPushButton("Sign out")
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

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateUsername()

    def signOut(self):
        self.parent.sign_in_page.clearUsernameInput()
        self.parent.db.update_by_id("profile", "id", 1, {"username": "Default", "currentTab": "SignIn"})
        self.parent.setCurrentIndex(0)

    def updateUsername(self):
        self.username = self.getUsername()
        self.userLabel.setText(f"User: {self.username}")

    def getUsername(self):
        return self.parent.fetch_username()

    def getManifestData(self):
        data, name = self.parent.fetch_manifest()
        return data, name

    def goToLog(self):
        log = LogPage(self)
        log.exec_()

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

                print(f"Manifest file selected: {file_name}")
                print(f"Manifest data saved to the database.")
            except Exception as e:
                print(f"Error reading or processing the file: {e}")
