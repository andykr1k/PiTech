import ast
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid
from Frontend.Components.Steps import Steps
from Frontend.Components.UserHeader import UserHeader

class OperationPage(QWidget):
    def __init__(self, parent, operationTitle):
        super().__init__()
        self.parent = parent
        self.operation_title = operationTitle
        self.grid_state = self.parse_grid_state(self.get_grid_state())
        self.steps_list = self.get_moves_list()
        self.steps_cost = self.get_total_moves_cost()
        self.current_step = self.get_current_step()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.header = UserHeader(self.parent)
        main_layout.addWidget(self.header)

        title_label = QLabel(self.operation_title + " Operation")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2F27CE;")
        main_layout.addWidget(title_label)

        self.middle_section = QHBoxLayout()

        # Add grid container and grid visualization
        self.grid_container = QFrame()
        self.grid_layout = QVBoxLayout(self.grid_container)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.grid = Grid(self, static=True, gridState=self.grid_state, current_move=self.current_step)
        self.visual_grid = self.grid.visualizeGrid()
        self.grid_layout.addWidget(self.visual_grid)
        self.middle_section.addWidget(self.grid_container)

        # Add steps widget to the middle section
        self.steps_widget = Steps(self.steps_list, self.current_step, self.steps_cost, self)
        self.middle_section.addWidget(self.steps_widget)

        main_layout.addLayout(self.middle_section)
        self.setLayout(main_layout)

    # Fetch the current state of the grid from the parent
    def get_grid_state(self):
        return self.parent.fetch_grid_state()

    # Fetch the list of moves for the operation from the parent
    def get_moves_list(self):
        return self.parent.fetch_moves_list()

    # Parse the grid state from a string to a dictionary
    def parse_grid_state(self, string_grid):
        return ast.literal_eval(string_grid)

    # Calculate the total cost of all moves in the steps list
    def get_total_moves_cost(self):
        cost = 0
        for move in self.steps_list:
            cost += move[3]
        return cost

    # Fetch the current step of the operation from the parent
    def get_current_step(self):
        return self.parent.fetch_current_step()

    # Initialize and return a new Steps widget
    def initialize_steps_widget(self):
        return Steps(self.steps_list, self.current_step, self.steps_cost, self)

    # Initialize and return a visualized grid object
    def initialize_visual_grid(self):
        grid = Grid(self, static=True, gridState=self.grid_state, current_move=self.current_step)
        return grid.visualizeGrid()

    # Update the operations page with the latest grid state and steps list
    def update_operations_page(self):
        # Update state
        self.grid_state = self.parse_grid_state(self.get_grid_state())
        self.steps_list = self.get_moves_list()
        self.steps_cost = self.get_total_moves_cost()
        self.current_step = self.get_current_step()
        self.parent.update_current_step_in_db(self.current_step, "STARTED")
        self.current_step = self.get_current_step()

        # Remove and delete the current visual grid
        self.grid_layout.removeWidget(self.visual_grid)
        self.visual_grid.deleteLater()

        # Create and add the new visual grid
        self.grid = Grid(self, static=True, gridState=self.grid_state,
                        current_move=self.current_step)
        self.visual_grid = self.grid.visualizeGrid()
        self.grid_layout.addWidget(self.visual_grid)

        # Update layout
        self.grid_layout.update()
        self.visual_grid.show()

        # Remove and delete the current steps widget
        self.middle_section.removeWidget(self.steps_widget)
        self.steps_widget.deleteLater()

        # Create and add the new steps widget
        self.steps_widget = Steps(
            self.steps_list, self.current_step, self.steps_cost, self)
        self.middle_section.addWidget(self.steps_widget)

        # Ensure UI refresh
        self.update()
        self.repaint()
