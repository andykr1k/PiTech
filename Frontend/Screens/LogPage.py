from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LogPage(QDialog):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.titleLabel = QLabel("Log")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet(
            """
            color: black; 
            """
        )
        layout.addWidget(self.titleLabel)

        self.logDisplay = QTextEdit()
        self.logDisplay.setReadOnly(True)
        self.logDisplay.setStyleSheet(
            """
            background-color: #D3D3D3; 
            color: black; 
            font-weight: bold; 
            font-size: 20px;
            border-radius: 10px;
            """
        )
        self.logDisplay.setText("\n".join([
            "2024-10-30 08:00: Jerry Taylor signs out",
            "2024-10-30 08:01: Rodney Bernard signs in",
            "2024-10-30 08:08: Manifest GracefulCapRon.txt is opened, there are 8 containers",
            "2024-10-30 10:32: “Bike parts” is offloaded",
            "2024-10-30 10:33: Noticed the “Bike parts” container is 10% below its stated weight",
        ]))
        layout.addWidget(self.logDisplay)

        comment_layout = QHBoxLayout()

        self.commentInput = QTextEdit(self)
        self.commentInput.setPlaceholderText("Add your comment here...")
        self.commentInput.setStyleSheet(
            """
            background-color: #F1F1F1;
            color: black;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            """
        )
        comment_layout.addWidget(self.commentInput, 1)

        self.commentButton = QPushButton("Comment")
        self.commentButton.setFont(QFont("Arial", 14))
        self.commentButton.clicked.connect(self.addComment)
        self.commentButton.setStyleSheet(
            """
            background-color: #2F27CE;
            color: white;
            border-radius: 10px;
            padding: 10px;
            """
        )
        comment_layout.addWidget(self.commentButton)

        layout.addLayout(comment_layout)
        main_layout.addLayout(layout)
        self.setLayout(main_layout)

        self.setWindowFlag(Qt.FramelessWindowHint, False)

        self.setModal(True)
        self.resize(500, 400)
        self.center()

    def center(self):
        screen_geometry = self.screen().geometry()
        dialog_geometry = self.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.move(x, y)

    def addComment(self):
        text = self.commentInput.toPlainText()
        if text:
            timestamp = "2024-10-30 11:45"
            self.logDisplay.append(f"{timestamp}: {text}")
            self.commentInput.clear()
