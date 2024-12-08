import os
import sys
import ast
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import QTime, QDate
from Backend.Classes.Grid import Grid
from Backend.Classes.Pathfinder import Pathfinder
from Backend.Utilities.Utils import upload_manifest, upload_transfer_list
from Frontend import SignInPage, HomePage, LogPage, TransferPage, OperationPage, UnloadLoadPage
from Database import SQLiteDatabase


class PiTech(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.grid = None
        self.pathfinder = None
        self.db_path = os.path.join(os.getcwd(), "Data", "Database.db")
        self.db = self.setup_db()

        self.sign_in_page = SignInPage(self)
        self.home_page = HomePage(self)
        self.transfer_page = TransferPage(self)
        self.operation_page_balance = None
        self.operation_page_transfer = None

        self.addWidget(self.sign_in_page)
        self.addWidget(self.home_page)
        self.addWidget(self.transfer_page)

        self.setup_connections()
        self.fetch_state()
        self.show()

    def setup_db(self):
        db = SQLiteDatabase(self.db_path)

        # For setting db up before final db structure
        # db.drop_table("profile")
        # db.drop_table("Grids")
        # db.drop_table("Lists")
        db.drop_table("Log")

        db.create_table(
            "profile", "id INTEGER PRIMARY KEY, username TEXT, currentTab TEXT")

        if not db.fetch_one("profile", "1=1"):
            db.insert("profile", "username, currentTab", ("default", "SignIn"))

        db.create_table(
            "Grids", "id INTEGER PRIMARY KEY, Name TEXT, State TEXT")
        
        db.create_table(
            "Log", "id INTEGER PRIMARY KEY, Time TEXT, Event TEXT"
        )

        db.create_table(
            "Lists", "id INTEGER PRIMARY KEY, UnloadLoadList TEXT, Manifest TEXT, ManifestName TEXT, OutboundManifest TEXT, OutboundManifestName TEXT")

        if not db.fetch_one("Lists", "1=1"):
            db.insert("Lists", "UnloadLoadList", ("NAN",))

        return db

    def fetch_state(self):
        user = self.db.fetch_all("profile")
        if user[0][1] != "default":
            if user[0][2] == "Home":
                self.setCurrentWidget(self.home_page)
            elif user[0][2] == "Balance":
                self.operation_page_balance = OperationPage(self, "Balance")
                self.addWidget(self.operation_page_balance)
                self.setCurrentWidget(self.operation_page_balance)
            elif user[0][2] == "Transfer":
                self.operation_page_transfer = OperationPage(self, "Transfer")
                self.addWidget(self.operation_page_transfer)
                self.setCurrentWidget(self.operation_page_transfer)
        return

    def fetch_username(self):
        user = self.db.fetch_all("profile")
        return user[0][1]

    def fetch_grid_state(self):
        grid_state = self.db.fetch_one("Grids", "id = ?", params=(1,))[2]
        return grid_state

    def fetch_unload_and_load_list(self):
        list = self.db.fetch_one("Lists", "id = ?", params=(1,))[1]
        if list:
            list = ast.literal_eval(list)
        return list

    def fetch_manifest(self):
        data = self.db.fetch_one("Lists", "id = ?", params=(1,))[2]
        name = self.db.fetch_one("Lists", "id = ?", params=(1,))[3]
        if data and name:
            data = ast.literal_eval(data)
        return data, name

    def fetch_moves_list(self):
        moves = self.db.fetch_all("Moves")
        return moves

    def close_db(self):
        self.db.close()
        return

    def setup_connections(self):
        self.home_page.balance_button.clicked.connect(self.handle_balance)
        self.home_page.transfer_button.clicked.connect(self.handle_transfer)
        return

    def handle_balance(self):
        manifest_data, manifest_name = self.fetch_manifest()
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.pathfinder = Pathfinder(self.grid)
        self.update_grid_state_in_db(self.grid.get_grid())
        balance_moves = self.pathfinder.balance()
        self.update_moves_in_db(balance_moves)
        self.db.update_by_id("profile", "id", 1, {"currentTab": "Balance"})
        self.operation_page_balance = OperationPage(self, "Balance")
        self.addWidget(self.operation_page_balance)
        self.setCurrentWidget(self.operation_page_balance)
        return

    def update_moves_in_db(self, moves):
        self.db.drop_table("Moves")
        self.db.create_table(
            "Moves", "id INTEGER PRIMARY KEY, From_Slot TEXT, To_Slot TEXT, Cost INT(4), Status TEXT, Completed_Grid_State TEXT")
        for move in moves:
            self.db.insert("Moves", "From_Slot, To_Slot, Cost, Status, Completed_Grid_State", (str(
                move.get_from_slot()), str(move.get_to_slot()), move.get_cost(), "NOT STARTED", "TEMP_GRID_STATE_HOLDER"))
        return

    def update_grid_state_in_db(self, grid_state):
        state = []
        row = []
        for grid_row in range(len(grid_state)):
            for grid_col in range(len(grid_state[grid_row])):
                row.append(grid_state[grid_row][grid_col].container.name)
            state.append(row)
            row = []
        self.db.insert("Grids", "Name, State", ("Name", str(state)))
        return

    def handle_transfer(self):
        manifest_data, manifest_name = self.fetch_manifest()
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.update_grid_state_in_db(self.grid.get_grid())
        transfer_list_page = UnloadLoadPage(self)
        transfer_list_page.exec_()
        transfer_data = self.fetch_unload_and_load_list()

        self.grid.setup_transferlist(transfer_data)
        self.pathfinder = Pathfinder(self.grid)
        transfer_moves = self.pathfinder.transfer()
        self.update_moves_in_db(transfer_moves)
        self.db.update_by_id("profile", "id", 1, {"currentTab": "Transfer"})
        self.operation_page_transfer = OperationPage(self, "Transfer")
        self.addWidget(self.operation_page_transfer)
        self.setCurrentWidget(self.operation_page_transfer)
        return
    
    def add_log_entry(self, event_description):
        # Retrieve current time
        current_time = QTime.currentTime().toString("hh:mm")
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        timestamp = f"{current_date} {current_time}"
        # Insert event with timestamp into log database
        self.db.insert("Log", "Time, Event", (timestamp, event_description))

    def fetch_logs(self):
        logs = self.db.fetch_all("Log")
        return [f"{log[1]}: {log[2]}" for log in logs]

def main():
    app = QApplication(sys.argv)
    system = PiTech()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
