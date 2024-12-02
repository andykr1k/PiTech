import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from Backend.Classes.Grid import Grid
from Backend.Classes.Pathfinder import Pathfinder
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Frontend import SignInPage, HomePage, LogPage, TransferPage, OperationPage
from Database import SQLiteDatabase

class PiTech(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.grid = None
        self.pathfinder = None
        self.db = self.setup_db()

        self.sign_in_page = SignInPage(self)
        self.home_page = HomePage(self)
        self.transfer_page = TransferPage(self)
        self.operation_page_balance = OperationPage(self, "Balance")
        self.operation_page_transfer = OperationPage(self, "Transfer")

        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.transfer_page)
        self.addWidget(self.operation_page_balance)
        self.addWidget(self.operation_page_transfer)

        self.setup_connections()
        self.show()

    def setup_db(self):
        db = SQLiteDatabase("Data/Database.db")

        db.create_table(
            "profile", "id INTEGER PRIMARY KEY, username TEXT")

        if not db.fetch_one("profile", "1=1"):
            db.insert("profile", "username", ("default",))
            print("Default added.")

        return db

    def fetch_username(self):
        user = self.db.fetch_all("profile")
        return user[0][1]
    
    def close_db(self):
        self.db.close()

    def setup_connections(self):
        self.home_page.balance_button.clicked.connect(self.handle_balance)
        self.home_page.transfer_button.clicked.connect(self.handle_transfer)


    def handle_balance(self):
        manifest_filename = "ShipCase1.txt"
        manifest_data = upload_manifest(manifest_filename)
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.pathfinder = Pathfinder(self.grid)
        balance_moves = self.pathfinder.balance()

        self.operation_page_balance.update_steps(balance_moves)
        self.setCurrentWidget(self.operation_page_balance)

    def handle_transfer(self):
        manifest_filename = "ShipCase1.txt"
        transfer_filename = "case1.txt"
        manifest_data = upload_manifest(manifest_filename)
        transfer_data = upload_transfer_list(transfer_filename)
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.grid.setup_transferlist(transfer_data)
        self.pathfinder = Pathfinder(self.grid)
        transfer_moves = self.pathfinder.transfer()

        self.operation_page_transfer.update_steps(transfer_moves)
        self.setCurrentWidget(self.operation_page_transfer)

def main():
    app = QApplication(sys.argv)
    system = PiTech()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
