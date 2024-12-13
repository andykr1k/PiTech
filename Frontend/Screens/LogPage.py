from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QFileDialog
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
            font-size: 20px;
            border: 2px solid #3F51B5;
            border-radius: 10px;
            padding: 15px;
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
            font-size: 20px;
            border: 2px solid #3F51B5;
            border-radius: 10px;
            padding: 15px;
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

        self.downloadButton = QPushButton("Download")
        self.downloadButton.setFont(QFont("Arial", 14))
        self.downloadButton.clicked.connect(self.download_logs)
        self.downloadButton.setStyleSheet(
            """
            background-color: #2F27CE;
            color: white;
            border-radius: 10px;
            padding: 10px;
            """
        )
        comment_layout.addWidget(self.downloadButton)

        layout.addLayout(comment_layout)
        main_layout.addLayout(layout)
        self.setLayout(main_layout)

        self.setWindowFlag(Qt.FramelessWindowHint, False)

        self.setModal(True)
        self.resize(1000, 1000)
        self.center()

        self.refresh_logs()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start(500)

    # Center log page on users screen
    def center(self):
        screen_geometry = self.screen().geometry()
        dialog_geometry = self.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.move(x, y)

    # Enables user to add comment
    def addComment(self):
        # Get current username
        username = self.getUsername()
        # Define text for comment
        text = self.commentInput.text().strip()
        # Push comment with username to log database
        self.parent.add_log_entry(f"{username} comments: {text}")
        # Clear comment box after comment is pushed to log database
        self.clearCommentInput()

    # Update log page with data in log database
    def refresh_logs(self):
        # Fetch updated log database
        logs = self.parent.fetch_logs()
        # Display updated log database
        self.logDisplay.setText("\n".join(logs))

    # Download log database as .txt file
    def download_logs(self):
        # Get username of current logged in user
        username = self.getUsername()
        # Define log for export
        log = self.parent.fetch_logs_for_download()
        # Define log file name
        log_name = "KeoghsPort2024.txt"
        # Add event to log database when user downloads log file
        self.parent.add_log_entry(f"{username} downloaded {log_name}")

        # Define options for download path
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Log File", log_name, "All Files (*)", options=options
        )

        if save_path:
            try:
                # Export log file to user-selected path
                with open(save_path, 'w') as file:
                    for l in log:
                        file.write(l)

            # Print error if file is not exported correctly
            except Exception as e:
                print(f"Error saving file: {e}")

    # Clear comment box
    def clearCommentInput(self):
        self.commentInput.clear()
 
    # Get username of current user
    def getUsername(self):
        return self.parent.fetch_username()

