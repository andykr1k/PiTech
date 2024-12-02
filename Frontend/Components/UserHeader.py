from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from Frontend.Screens.LogPage import LogPage

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

    def updateUsername(self, username):
        self.username = username
        self.userLabel.setText(f"User: {self.username}")

    def signOut(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.sign_in_page.clearUsernameInput()

    def goToLog(self):
        log = LogPage(self)
        log.exec_()
