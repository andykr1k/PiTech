import sys
from Frontend import SignInPage, HomePage, OperationPage, TestPage, LogPage
from Database.main import initialize_database
from PyQt5.QtWidgets import QApplication, QStackedWidget

class MainWidget(QStackedWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.sign_in_page = SignInPage(self, db)  
        self.home_page = HomePage(self, db)  
        self.operation_page = OperationPage(self, db) 
        self.log_page = LogPage(self, db)
        self.test_page = TestPage(self, db)
        
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.operation_page)
        self.addWidget(self.log_page)
        self.addWidget(self.test_page) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = initialize_database()
    main_widget = MainWidget(db)  
    main_widget.show() 
    sys.exit(app.exec_())
    