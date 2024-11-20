import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Screens import HomePage, SignInPage

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.sign_in_page = SignInPage(self)
        self.home_page = HomePage(self)
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        
    @property
    def current_page(self):
        return self.home_page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec_())