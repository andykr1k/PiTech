import sys
from Frontend import SignInPage, HomePage, TestPage, LogPage
from PyQt5.QtWidgets import QStackedWidget

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.sign_in_page = SignInPage(self)  
        self.home_page = HomePage(self)           
        
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)