import os
import sys
import ast
import signal
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

        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def set_up(self):
        db_dir = os.path.join(os.getcwd(), "Data")
        db_path = os.path.join(db_dir, "Database.db")

        os.makedirs(db_dir, exist_ok=True)

        if not os.path.isfile(db_path):
            with open(db_path, "w") as db_file:
                pass
            print(f"Database file created at {db_path}")
        else:
            print(f"Database file already exists at {db_path}")
        return

    def setup_db(self):
        self.set_up()

        db = SQLiteDatabase(self.db_path)

        # For setting db up before final db structure
        db.drop_table("profile")
        db.drop_table("Grids")
        db.drop_table("Lists")
        db.drop_table("Log")

        db.create_table(
            "profile", "id INTEGER PRIMARY KEY, username TEXT, currentTab TEXT")

        if not db.fetch_one("profile", "1=1"):
            db.insert("profile", "username, currentTab", ("default", "SignIn"))

        db.create_table(
            "Grids", "id INTEGER PRIMARY KEY, Name TEXT, State TEXT")

        if not db.fetch_one("Grids", "1=1"):
            db.insert("Grids", "Name, State", ("", ""))

        db.create_table(
            "Log", "id INTEGER PRIMARY KEY, Time TEXT, Event TEXT"
        )

        db.create_table(
            "Lists", "id INTEGER PRIMARY KEY, UnloadLoadList TEXT, Manifest TEXT, ManifestName TEXT, OutboundManifest TEXT, OutboundManifestName TEXT")

        if not db.fetch_one("Lists", "1=1"):
            db.insert("Lists", "UnloadLoadList", ("NAN",))

        return db

    def fetch_state(self):
        user = self.db.fetch_all("profile", "DESC")
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
        user = self.db.fetch_all("profile", "DESC")
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
        moves = self.db.fetch_all("Moves", "ASC")
        return moves

    def fetch_current_step(self):
        current_step = self.db.fetch_all("Moves", "ASC")
        for move in current_step:
            if not move[4] == "COMPLETED":
                return move
        return "COMPLETED"

    def close_db(self):
        self.db.close()
        return

    def setup_connections(self):
        self.home_page.balance_button.clicked.connect(self.handle_balance)
        self.home_page.transfer_button.clicked.connect(self.handle_transfer)
        return

    def handle_balance(self):
        self.add_log_entry(f"Balance Operation Selected")
        manifest_data, manifest_name = self.fetch_manifest()
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.pathfinder = Pathfinder(self.grid)
        self.update_grid_state_in_db(self.grid.get_grid(), True)
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
                move[0].get_from_slot().position).replace(" ", ""), str(move[0].get_to_slot().position).replace(" ", ""), move[0].get_cost(), "NOT STARTED", str(self.parse_grid_state(move[1].get_grid()))))
        return

    def update_current_step_in_db(self, current_step, status):
        if status =="STARTED":
            self.db.update_by_id("Moves", "id", str(current_step[0]), {"Status": "STARTED"})
        elif status == "COMPLETED":
            self.db.update_by_id("Moves", "id", str(current_step[0]), {"Status": "COMPLETED"})
            self.update_grid_state_in_db(str(current_step[5]), False)

    def parse_grid_state(self, grid_state):
        state = []
        row = []
        for grid_row in range(len(grid_state)):
            for grid_col in range(len(grid_state[grid_row])):
                row.append(grid_state[grid_row][grid_col].container.name)
            state.append(row)
            row = []
        return state

    def update_grid_state_in_db(self, grid_state, parse):
        if parse:
            grid_state = self.parse_grid_state(grid_state)
        self.db.update_by_id("Grids", "id", 1, {"State": str(grid_state)})
        return

    def handle_transfer(self):
        self.add_log_entry(f"Transfer Operation Selected")
        manifest_data, manifest_name = self.fetch_manifest()
        self.grid = Grid()
        self.grid.setup_grid(manifest_data)
        self.update_grid_state_in_db(self.grid.get_grid(), True)
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

    # Function that adds atomic events to log
    def add_log_entry(self, event_description):
        # Get current time
        current_time = QTime.currentTime().toString("hh:mm")
        # Get current date
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        # Create timestamp with time and date in ISO format (excluding seconds and miliseconds)
        timestamp = f"{current_date} {current_time}"
        # Insert atomic event into the log database
        self.db.insert("Log", "Time, Event", (timestamp, event_description))

    # Function that fetches the log
    def fetch_logs(self):
        # Define log database
        logs = self.db.fetch_all("Log", "ASC")
        # Return all rows in log database
        return [f"{log[1]}: {log[2]}" for log in logs]

    def fetch_logs_for_download(self):
        # Define log database
        logs = self.db.fetch_all("Log", "ASC")
        # Return all rows in log database with new line char
        return [f"{log[1]}: {log[2]}\n" for log in logs]

    def handle_shutdown(self, signum, frame):
        print(f"Signal {signum} received. Performing cleanup...")
        self.add_log_entry("App shutting down due to signal.")
        self.add_log_entry("Application Shutdown - Possible Power Outage")
        self.close_db()
        sys.exit(0)

    def closeEvent(self, event):
        print("Application closing...")
        username = self.fetch_username()
        self.add_log_entry(f"Application Closed by {username}")
        self.close_db()
        event.accept()

def main():
    app = QApplication(sys.argv)
    system = PiTech()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
