import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Screens.HomePage import HomePage
from Screens.TestPage import TestPage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    homePage = HomePage(stacked_widget)
    testpage = TestPage()
    stacked_widget.addWidget(homePage)
    stacked_widget.addWidget(testpage)
    stacked_widget.show()
    sys.exit(app.exec_())
