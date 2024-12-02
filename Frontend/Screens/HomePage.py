from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from Frontend.Components.UserHeader import UserHeader


class HomePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)
        self.header = UserHeader(self.parent)
        main_layout.addWidget(self.header)

        main_layout.addLayout(top_layout)

        center_layout = QHBoxLayout()
        center_layout.setSpacing(20)

        self.transfer_button = QPushButton("Transfer")
        self.transfer_button.setFont(QFont("Roboto", 24, QFont.Bold))
        self.transfer_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 90px 60px;
            border-radius: 8px;
            font-weight: 600;
        """)
        center_layout.addWidget(self.transfer_button)

        self.balance_button = QPushButton("Balance")
        self.balance_button.setFont(QFont("Roboto", 24, QFont.Bold))
        self.balance_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 90px 60px;
            border-radius: 8px;
            font-weight: 600;
        """)
        center_layout.addWidget(self.balance_button)

        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
