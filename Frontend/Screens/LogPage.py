from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class LogPage(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
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
            background-color: #F1F1F1; 
            color: black; 
            font-weight: bold; 
            font-size: 12px;
            border-radius: 10px;
            """
        )
        layout.addWidget(self.logDisplay)

        comment_layout = QHBoxLayout()

        self.commentInput = QLineEdit(self)
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
        self.resize(1000, 1000)
        self.center()

        self.refresh_logs()  # Populate logs initially

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start(500)  # Refresh frequently

    def center(self):
        screen_geometry = self.screen().geometry()
        dialog_geometry = self.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.move(x, y)

    def addComment(self):
        text = self.commentInput.text().strip()
        self.parent.add_log_entry(f"{text}")
        self.clearCommentInput()

    def refresh_logs(self):
        logs = self.parent.fetch_logs()
        self.logDisplay.setText("\n".join(logs))

    def clearCommentInput(self):
        self.commentInput.clear()

