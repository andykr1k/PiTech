import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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


class HomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.username = ""
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Top Layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)
        
        # Username Label
        self.userLabel = QLabel(f"User: {self.username}")
        self.userLabel.setFont(QFont("Arial", 12, QFont.Bold))
        self.userLabel.setStyleSheet("background-color: #D3D3D3; padding: 5px; border-radius: 5px;")
        top_layout.addWidget(self.userLabel)
        
        # Spacer to push "Sign Out Button" to the right
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Sign Out Button
        sign_out_button = QPushButton("Sign out")
        sign_out_button.setFont(QFont("Arial", 12))
        sign_out_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 5px; border-radius: 10px;")
        sign_out_button.clicked.connect(self.signOut)
        top_layout.addWidget(sign_out_button)
        
        main_layout.addLayout(top_layout)
        
        # Center Layout
        center_layout = QHBoxLayout()
        center_layout.setSpacing(20)
        
        # Transfer Button
        transfer_button = QPushButton("Transfer")
        transfer_button.setFont(QFont("Arial", 24, QFont.Bold))
        transfer_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 50px; border-radius: 20px;")
        center_layout.addWidget(transfer_button)
        
        # Balance Button
        balance_button = QPushButton("Balance")
        balance_button.setFont(QFont("Arial", 24, QFont.Bold))
        balance_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 50px; border-radius: 20px;")
        center_layout.addWidget(balance_button)
        
        main_layout.addStretch()  # Add stretch to push Center Layout to the middle
        main_layout.addLayout(center_layout)
        main_layout.addStretch()  # Add stretch to push Center Layout to the middle
        
        # Bottom Layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Log Button
        log_button = QPushButton("Log")
        log_button.setFont(QFont("Arial", 12, QFont.Bold))
        log_button.setStyleSheet("background-color: #D3D3D3; padding: 5px; border-radius: 10px;")
        bottom_layout.addWidget(log_button, alignment=Qt.AlignRight)
        
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        
    def updateUserLabel(self):
        self.userLabel.setText(f"User: {self.username}")
        
    def signOut(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.sign_in_page.clearUsernameInput() #Clear the username input


class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.sign_in_page = SignInPage(self)
        self.home_page = HomePage(self)
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        
    @property
    def current_page(self):
        return self.home_page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())