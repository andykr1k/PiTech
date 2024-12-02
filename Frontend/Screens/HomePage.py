from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HomePage(QWidget):
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Top Layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Fetch the current username from the database
        record = self.db.fetch_one("current_user", "1=1")  # Fetch username from the 'current_user' table
        current_username = record[1] if record else "Unknown"  # Use "Unknown" if no user is found
        
        # Username Label
        self.userLabel = QLabel(f"User: {current_username}")
        self.userLabel.setFont(QFont("Arial", 12, QFont.Bold))
        self.userLabel.setStyleSheet("background-color: #D3D3D3; padding: 5px; border-radius: 5px;")
        top_layout.addWidget(self.userLabel)
        
        # Spacer to push "Sign Out Button" to the right
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Sign In Button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.setFont(QFont("Arial", 12, QFont.Bold))
        sign_in_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 5px; border-radius: 10px;")
        sign_in_button.clicked.connect(self.goToSignInPage)
        top_layout.addWidget(sign_in_button)
        
        # Sign Out Button
        sign_out_button = QPushButton("Sign Out")
        sign_out_button.setFont(QFont("Arial", 12, QFont.Bold))
        sign_out_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 5px; border-radius: 10px;")
        sign_out_button.clicked.connect(self.goToSignInPage)
        top_layout.addWidget(sign_out_button)
        
        main_layout.addLayout(top_layout)
        
        # Center Layout
        center_layout = QHBoxLayout()
        center_layout.setSpacing(20)
        
        # Transfer Button
        transfer_button = QPushButton("Transfer")
        transfer_button.setFont(QFont("Arial", 24, QFont.Bold))
        transfer_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 50px; border-radius: 20px;")
        transfer_button.clicked.connect(self.goToOperationPage)
        center_layout.addWidget(transfer_button)
        
        # Balance Button
        balance_button = QPushButton("Balance")
        balance_button.setFont(QFont("Arial", 24, QFont.Bold))
        balance_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 50px; border-radius: 20px;")
        balance_button.clicked.connect(self.goToOperationPage)
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
        log_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 5px; border-radius: 10px;")
        log_button.clicked.connect(self.goToLogPage)
        bottom_layout.addWidget(log_button, alignment=Qt.AlignRight)
        
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
    

    def updateUserLabel(self):
        # Fetch the current username from the "current_user" table
        record = self.db.fetch_one("current_user", "1=1")
        if record:
            self.userLabel.setText(f"User: {record[1]}")  # Update label with the username
        else:
            self.userLabel.setText("User: Unknown")  # Fallback if no current user

    def goToSignInPage(self):
        self.stacked_widget.sign_in_page.clearUsernameInput() #Clear the username input
        self.stacked_widget.setCurrentIndex(0) # Switch to SignIn page
        
    def goToLogPage(self):
        self.stacked_widget.db.insert("page_history", "page", ("home",)) # Insert "home" in page_history
        self.stacked_widget.setCurrentIndex(3) # Switch to Log page

    def goToOperationPage(self):
        self.stacked_widget.db.insert("page_history", "page", ("operation",)) # Insert "operation" in page_history
        self.stacked_widget.operation_page.updateUserLabel()  # Refresh the user label
        self.stacked_widget.setCurrentIndex(2) # Switch to Operation page
