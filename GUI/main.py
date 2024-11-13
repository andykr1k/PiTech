import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class HomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.titleLabel = QLabel("PiTech")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #2F27CE;")
        layout.addWidget(self.titleLabel)

        self.continueButton = QPushButton("Continue")
        self.continueButton.setFont(QFont("Arial", 14))
        self.continueButton.setStyleSheet(
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
        self.continueButton.clicked.connect(self.goToNextPage)
        layout.addWidget(self.continueButton, alignment=Qt.AlignCenter)

        self.continueButton = QPushButton("Go to Log Page")
        self.continueButton.setFont(QFont("Arial", 14))
        self.continueButton.setStyleSheet(
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
        self.continueButton.clicked.connect(self.goToLogPage)
        layout.addWidget(self.continueButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def goToNextPage(self):
        self.stacked_widget.setCurrentIndex(1)

    def goToLogPage(self):
        self.stacked_widget.setCurrentIndex(2)


class TestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.titleLabel = QLabel("PiTech Test Page")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #2F27CE;")
        layout.addWidget(self.titleLabel)

        main_layout.addLayout(layout)

        self.setLayout(main_layout)

class LogPage(QWidget): 
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

    def goToPreviousPage(self):
        self.stacked_widget.setCurrentIndex(0)

    def addComment(self):
        text, ok = QInputDialog().getText(self, "Add Comment", "Enter comment:")
        if ok and text:
            timestamp = "2024-10-30 11:45"
            self.logDisplay.append(f"{timestamp} {text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    homePage = HomePage(stacked_widget)
    testpage = TestPage()
    logPage = LogPage(stacked_widget)
    stacked_widget.addWidget(homePage)
    stacked_widget.addWidget(testpage)
    stacked_widget.addWidget(logPage)
    stacked_widget.show()
    sys.exit(app.exec_())
