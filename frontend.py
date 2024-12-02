import sys
from Frontend import SignInPage, HomePage, TestPage, LogPage
from PyQt5.QtWidgets import QApplication, QStackedWidget

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.sign_in_page = SignInPage(self)  
        self.home_page = HomePage(self)  
        self.test_page = TestPage(self)
        self.log_page = LogPage(self)
         
        
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.test_page) 
        self.addWidget(self.log_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()  
    main_widget.show()  
    sys.exit(app.exec_())  