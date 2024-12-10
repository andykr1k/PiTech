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

        self.grid_container = QFrame()
        self.grid_layout = QVBoxLayout(self.grid_container)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.grid = Grid(self, static=True, gridState=self.grid_state, current_move=self.current_step)
        self.visual_grid = self.grid.visualizeGrid()
        self.grid_layout.addWidget(self.visual_grid)
        self.middle_section.addWidget(self.grid_container)

        self.steps_widget = Steps(self.steps_list, self.current_step, self.steps_cost, self)
        self.middle_section.addWidget(self.steps_widget)

        main_layout.addLayout(self.middle_section)
        self.setLayout(main_layout)

    def get_grid_state(self):
        return self.parent.fetch_grid_state()

    def get_moves_list(self):
        return self.parent.fetch_moves_list()

    def parse_grid_state(self, string_grid):
        return ast.literal_eval(string_grid)

    def get_total_moves_cost(self):
        cost = 0
        for move in self.steps_list:
            cost += move[3]
        return cost

    def get_current_step(self):
        return self.parent.fetch_current_step()

    def update_operations_page(self):
        self.grid_state = self.parse_grid_state(self.get_grid_state())
        self.steps_list = self.get_moves_list()
        self.steps_cost = self.get_total_moves_cost()
        self.current_step = self.get_current_step()

        new_steps_widget = Steps(self.steps_list, self.current_step, self.steps_cost, self)
        new_grid = Grid(self, static=True, gridState=self.grid_state, current_move=self.current_step)
        new_visual_grid = new_grid.visualizeGrid()

        self.middle_section.removeWidget(self.steps_widget)
        self.steps_widget.deleteLater()

        self.grid_layout.removeWidget(self.visual_grid)
        self.visual_grid.deleteLater()

        self.middle_section.addWidget(new_steps_widget)
        self.grid_layout.addWidget(new_visual_grid)

        self.steps_widget = new_steps_widget
        self.visual_grid = new_visual_grid
