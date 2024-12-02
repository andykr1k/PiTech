from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont

class UserHeader(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.username = ""
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.userLabel = QLabel(f"User: {self.username}")
        self.userLabel.setFont(QFont("Roboto", 14, QFont.Bold))
        self.userLabel.setStyleSheet("""
            background-color: #E8EAF6;
            padding: 8px 12px;
            border-radius: 5px;
            color: #3F51B5;
        """)
        layout.addWidget(self.userLabel)

        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

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

    def updateUsername(self, username):
        self.username = username
        self.userLabel.setText(f"User: {self.username}")

    def signOut(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.sign_in_page.clearUsernameInput()