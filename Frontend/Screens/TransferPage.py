from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from Frontend.Components.UserHeader import UserHeader


class TransferPage(QWidget):
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

        # 'Unload' button setup
        self.unload_button = QPushButton("Unload")
        self.unload_button.setFont(QFont("Roboto", 24, QFont.Bold))
        self.unload_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 90px 60px;
            border-radius: 8px;
            font-weight: 600;
        """)
        center_layout.addWidget(self.unload_button)

        # 'Load' button setup
        self.load_button = QPushButton("Load")
        self.load_button.setFont(QFont("Roboto", 24, QFont.Bold))
        self.load_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 90px 60px;
            border-radius: 8px;
            font-weight: 600;
        """)
        center_layout.addWidget(self.load_button)

        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)