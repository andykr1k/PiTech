from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class LogPage(QWidget): 
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
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
            background-color: #D3D3D3; 
            color: black; 
            border-radius: 10px;
            """
        )
        layout.addWidget(self.titleLabel)

        # Adding QTextEdit to display the list
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
        self.logDisplay.setText("\n".join
            ([
            "2024-10-30 08:00 Jerry Taylor signs out", 
            "2024-10-30 08:01  Rodney Bernard signs in", 
            "2024-10-30 08:08  Manifest GracefulCapRon.txt is opened, there are 8 containers", 
            "2024-10-30 10:32  “Bike parts” is offloaded",
            "2024-10-30 10:33  Noticed the “Bike parts” container is 10% below its stated weight",
            ]))
        layout.addWidget(self.logDisplay)

        button_layout = QHBoxLayout()

        self.commentButton = QPushButton("Add Comment")
        self.commentButton.setFont(QFont("Arial", 14))
        self.commentButton.clicked.connect(self.addComment)
        button_layout.addWidget(self.commentButton, alignment=Qt.AlignLeft)
        self.commentButton.setStyleSheet(
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

        self.backButton = QPushButton("Back")
        self.backButton.setFont(QFont("Arial", 14))
        self.backButton.clicked.connect(self.goToPreviousPage)
        button_layout.addWidget(self.backButton, alignment=Qt.AlignRight)
        self.backButton.setStyleSheet(
            """
            background-color: #D3D3D3; 
            color: black; 
            border-radius: 10px;
            padding: 10px;
            """
        )

        layout.addLayout(button_layout)
        main_layout.addLayout(layout)
        self.setLayout(main_layout)


    def addComment(self):
        text, ok = QInputDialog().getText(self, "Add Comment", "Enter comment:")
        if ok and text:
            timestamp = "2024-10-30 11:45"
            self.logDisplay.append(f"{timestamp} {text}")

    def goToPreviousPage(self):
        # Fetch the last page from page_history
        last_page = self.stacked_widget.db.fetch_one(
            "page_history", "1=1 ORDER BY id DESC LIMIT 1"
        )

        if last_page:
            previous_page = last_page[1]  # Extract the page name
            # Navigate to the previous page
            if previous_page == "home":
                self.stacked_widget.setCurrentIndex(1) # Switch to Home page
            elif previous_page == "operation":
                self.stacked_widget.setCurrentIndex(2) # Switch to Operation page

            # Delete the last page entry from the history
            self.stacked_widget.db.delete("page_history", "id = ?", (last_page[0],))
        else:
            QMessageBox.warning(self, "Error", "No previous page found!")
    
