import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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

        self.setLayout(layout)

    def goToNextPage(self):
        self.stacked_widget.setCurrentIndex(1)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    homePage = HomePage(stacked_widget)
    testpage = TestPage()
    stacked_widget.addWidget(homePage)
    stacked_widget.addWidget(testpage)
    stacked_widget.show()
    sys.exit(app.exec_())
