import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Screens.HomePage import HomePage
from Screens.TestPage import TestPage
from Screens.OperationPage import OperationPage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    homePage = HomePage(stacked_widget)
    testpage = TestPage(stacked_widget)
    operationpage = OperationPage()
    stacked_widget.addWidget(homePage)
    stacked_widget.addWidget(testpage)
    stacked_widget.addWidget(operationpage)
    stacked_widget.show()
    sys.exit(app.exec_())
