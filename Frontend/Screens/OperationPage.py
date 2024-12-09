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

        middle_section = QHBoxLayout()

        grid_container = QFrame()
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setAlignment(Qt.AlignCenter)
        grid = Grid(self, static=True, gridState=self.grid_state)
        grid_layout.addWidget(grid.visualizeGrid())
        middle_section.addWidget(grid_container)

        steps_widget = Steps(self.steps_list, self.steps_cost)
        middle_section.addWidget(steps_widget)

        main_layout.addLayout(middle_section)
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

    # def update_steps(self, moves):
    #     """Update the steps widget with new moves"""
    #     step_strings = []
    #     total_time = 0

    #     for i, move in enumerate(moves, 1):
    #         step_strings.append(f"Step {i}: {move}")
    #         total_time += move.cost

    #     self.steps_widget = Steps(step_strings, f"{total_time} min")

    #     for i in range(self.layout().count()):
    #         item = self.layout().itemAt(i)
    #         if isinstance(item.widget(), Steps):
    #             old_widget = item.widget()
    #             self.layout().replaceWidget(old_widget, self.steps_widget)
    #             old_widget.deleteLater()
    #             break
