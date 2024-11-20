import sys
from Frontend import SignInPage, HomePage, OperationPage, TestPage
from PyQt5.QtWidgets import QApplication, QStackedWidget

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.sign_in_page = SignInPage(self)  
        self.home_page = HomePage(self)  
        self.operation_page = OperationPage() 
        self.test_page = TestPage(self)  
         
        
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.operation_page)
        self.addWidget(self.test_page) 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = MainWidget()  
    main_widget.show()  
    sys.exit(app.exec_())  