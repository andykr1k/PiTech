import sys
from PyQt5.QtWidgets import QApplication
from frontend import MainWidget
from Backend.Classes.Grid import Grid
from Backend.Classes.Pathfinder import Pathfinder
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Frontend.Screens.OperationPage import OperationPage


class PiTech:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_widget = MainWidget()
        self.grid = None
        self.pathfinder = None
        
        # Initialize operation pages
        self.operation_page_balance = OperationPage(self.main_widget, "Balance")
        self.operation_page_transfer = OperationPage(self.main_widget, "Transfer")
        
        # Add operation pages to main widget
        self.main_widget.addWidget(self.operation_page_balance)
        self.main_widget.addWidget(self.operation_page_transfer)
        
        self.setup_connections()
        self.main_widget.show()

    def setup_connections(self):
        self.main_widget.home_page.balance_button.clicked.connect(
            self.handle_balance)
        self.main_widget.home_page.transfer_button.clicked.connect(
            self.handle_transfer)

    def handle_balance(self):
        manifest_filename = "ShipCase1.txt"
        manifest_data = upload_manifest(manifest_filename)
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.pathfinder = Pathfinder(self.grid)
        balance_moves = self.pathfinder.balance()

        # Update the balance operation page with the moves
        self.operation_page_balance.update_steps(balance_moves)
        
        # Switch to balance operation page
        self.main_widget.setCurrentWidget(self.operation_page_balance)

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

        # Update the transfer operation page with the moves
        self.operation_page_transfer.update_steps(transfer_moves)
        
        # Switch to transfer operation page
        self.main_widget.setCurrentWidget(self.operation_page_transfer)

    def run(self):
        return self.app.exec_()


def main():
    system = PiTech()
    sys.exit(system.run())


if __name__ == "__main__":
    main()
