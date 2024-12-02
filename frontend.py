import sys
from Frontend import SignInPage, HomePage, LogPage, TransferPage
from PyQt5.QtWidgets import QStackedWidget

class MainWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.sign_in_page = SignInPage(self)  
        self.home_page = HomePage(self)           
        self.transfer_page = TransferPage(self)
        
        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.transfer_page)