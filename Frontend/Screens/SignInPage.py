from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, pyqtSignal


class SignInPage(QWidget):
    username_updated = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.timeLabel = QLabel()
        self.timeLabel.setFont(QFont("Roboto", 12))
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet("color: #3F51B5;")
        layout.addWidget(self.timeLabel)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        self.updateTime()

        self.titleLabel = QLabel("Keogh's Ports")
        self.titleLabel.setFont(QFont("Roboto", 42, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #3F51B5;")
        layout.addWidget(self.titleLabel)

        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter your username")
        self.usernameInput.setFont(QFont("Roboto", 14))
        self.usernameInput.setFixedWidth(400)
        self.usernameInput.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #B0BEC5;
                border-radius: 4px;
                background-color: #FAFAFA;
            }
            QLineEdit:focus {
                border-color: #3F51B5;
                background-color: #FFFFFF;
            }
        """)
        self.usernameInput.returnPressed.connect(
            self.goToNextPage)
        layout.addWidget(self.usernameInput, alignment=Qt.AlignCenter)

        self.continueButton = QPushButton("Sign In")
        self.continueButton.setFont(QFont("Roboto", 14))
        self.continueButton.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                border-radius: 4px;
                padding: 12px;
                min-width: 200px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #303F9F;
            }
            QPushButton:pressed {
                background-color: #283593;
            }
        """)
        self.continueButton.clicked.connect(self.goToNextPage)
        layout.addWidget(self.continueButton, alignment=Qt.AlignCenter)

        self.copyrightLabel = QLabel("PiTech 2024")
        self.copyrightLabel.setFont(QFont("Roboto", 12))
        self.copyrightLabel.setAlignment(Qt.AlignCenter)
        self.copyrightLabel.setStyleSheet("color: #3F51B5;")
        layout.addWidget(self.copyrightLabel)

        self.setLayout(layout)

    # Update the timeLabel with the current time and date
    def updateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        current_date = QDate.currentDate().toString("MMMM dd, yyyy")
        self.timeLabel.setText(current_time + " - " + current_date)

    # Handle logic to sign in and navigate to the next page
    def goToNextPage(self):
        username = self.usernameInput.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Username field cannot be empty")
            return

        # Update the user profile in the database and switch to the next page
        self.parent.db.update_by_id("profile", "id", 1, {"username": username, "currentTab": "Home"})
        self.parent.setCurrentIndex(1)

        self.parent.add_log_entry(f"{username} signed in")

    # Clear the username input field
    def clearUsernameInput(self):
        self.usernameInput.clear()
