import sys
from Frontend.Screens.HomePage import HomePage
from Frontend.Screens.TestPage import TestPage
from PyQt5.QtWidgets import QApplication, QStackedWidget

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
