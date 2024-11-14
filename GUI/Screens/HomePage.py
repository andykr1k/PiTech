from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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