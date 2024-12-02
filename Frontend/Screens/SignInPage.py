from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class SignInPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        self.titleLabel = QLabel("Keogh's Ports")
        self.titleLabel.setFont(QFont("Roboto", 42, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #3F51B5;")
        layout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel("PiTech")
        self.subtitleLabel.setFont(QFont("Roboto", 24, QFont.Bold))
        self.subtitleLabel.setAlignment(Qt.AlignCenter)
        self.subtitleLabel.setStyleSheet("color: #3F51B5;")
        layout.addWidget(self.subtitleLabel)

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

        self.setLayout(layout)

    def goToNextPage(self):
        username = self.usernameInput.text().strip()
        if not username:
            QMessageBox.warning(
                self, "Error", "Username field cannot be empty")
        else:
            self.stacked_widget.home_page.header.updateUsername(username)
            self.stacked_widget.setCurrentIndex(1)

    def clearUsernameInput(self):
        self.usernameInput.clear()
