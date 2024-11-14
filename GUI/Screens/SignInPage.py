from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SignInPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)

        #Title
        self.titleLabel = QLabel("PiTech")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #2F27CE;")
        layout.addWidget(self.titleLabel)

        #Username Input
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter your username")
        self.usernameInput.setFont(QFont("Arial", 14))
        self.usernameInput.setFixedWidth(400)
        layout.addWidget(self.usernameInput, alignment=Qt.AlignCenter)

        #Sign In Button
        self.continueButton = QPushButton("Sign In")
        self.continueButton.setFont(QFont("Arial", 14))
        self.continueButton.setStyleSheet(
            """
            QPushButton {
                background-color: #2F27CE;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2F27CE;
            }
            """
        )
        self.continueButton.clicked.connect(self.goToNextPage)
        layout.addWidget(self.continueButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)
            
    def goToNextPage(self):
        username = self.usernameInput.text().strip()  # Trim any leading or trailing spaces
        if not username:
            # Show error message if username field is empty
            QMessageBox.warning(self, "Error", "Username field cannot be empty")
        else:
            # Proceed to the next page if username is entered
            self.stacked_widget.home_page.username = username  # Pass username to HomePage
            self.stacked_widget.home_page.updateUserLabel()     # Update the label with username
            self.stacked_widget.setCurrentIndex(1)

    def clearUsernameInput(self):
        self.usernameInput.clear()  # Clear the text in the input field