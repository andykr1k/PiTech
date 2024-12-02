from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SignInPage(QWidget):
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)

        # Title
        self.titleLabel = QLabel("PiTech")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #2F27CE;")
        layout.addWidget(self.titleLabel)

        # Username Input
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter your username")
        self.usernameInput.setFont(QFont("Arial", 14))
        self.usernameInput.setFixedWidth(400)
        layout.addWidget(self.usernameInput, alignment=Qt.AlignCenter)

        # Sign In Button
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
        self.continueButton.clicked.connect(self.goToPreviousPage)
        layout.addWidget(self.continueButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)


    def clearUsernameInput(self):
        self.usernameInput.clear() # Clear the text in the input field

    def goToPreviousPage(self):
        username = self.usernameInput.text().strip() # Trim any leading or trailing spaces
        if not username:
            # Show error message if username field is empty
            QMessageBox.warning(self, "Error", "Username field cannot be empty")
            return
        else:
            self.stacked_widget.db.delete("current_user", "1=1", ()) # Clear any previous current user
            self.stacked_widget.db.insert("current_user", "username", (username,))
            # Add the username to the database if not already present
            record = self.stacked_widget.db.fetch_one("current_user", "username = ?", (username,))
            if not record:
                self.stacked_widget.db.insert("current_user", "username", (username,))
        # Fetch the last page from page_history
        last_page = self.stacked_widget.db.fetch_one(
            "page_history", "1=1 ORDER BY id DESC LIMIT 1"
        )

        if last_page:
            previous_page = last_page[1] # Extract the page name
            # Navigate to the previous page
            if previous_page == "home":
                self.stacked_widget.setCurrentIndex(1) # Switch to Home page
            elif previous_page == "operation":
                self.stacked_widget.operation_page.updateUserLabel() # Update the user label
                self.stacked_widget.setCurrentIndex(2) # Switch to Operation page

            # Delete the last page entry from the history
            self.stacked_widget.db.delete("page_history", "id = ?", (last_page[0],))
        else:
            self.stacked_widget.setCurrentIndex(1) # Switch to Home page

        self.stacked_widget.home_page.updateUserLabel() # Update the user label
        