from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid
from Frontend.Components.Steps import Steps
from Frontend.Components.UserHeader import UserHeader

test_grid_state = [
    ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
        'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
     'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
     'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
     'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    ['UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
     'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED'],
    ['NAN', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED',
     'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'UNUSED', 'NAN'],
    ['NAN', 'NAN', 'CONTAINER', 'CONTAINER', 'UNUSED', 'UNUSED',
            'UNUSED', 'UNUSED', 'CONTAINER', 'CONTAINER', 'NAN', 'NAN'],
    ['NAN', 'NAN', 'NAN', 'CONTAINER', 'CONTAINER', 'UNUSED',
     'UNUSED', 'UNUSED', 'CONTAINER', 'NAN', 'NAN', 'NAN']
]


class OperationPage(QWidget):
    def __init__(self, parent, operationTitle):
        super().__init__()
        self.parent = parent
        self.operation_title = operationTitle
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
        grid = Grid(test_grid_state)
        grid_layout.addWidget(grid.visualizeGrid())
        middle_section.addWidget(grid_container)

        steps_list = ["Step 1: 1 min", "Step 2: 2 min",
                      "Step 3: 3 min", "Step 5: 5 min"]
        steps_widget = Steps(steps_list, "14 min")
        middle_section.addWidget(steps_widget)

        main_layout.addLayout(middle_section)
        self.setLayout(main_layout)

    def update_steps(self, moves):
        """Update the steps widget with new moves"""
        step_strings = []
        total_time = 0

        for i, move in enumerate(moves, 1):
            step_strings.append(f"Step {i}: {move}")
            total_time += move.cost

        self.steps_widget = Steps(step_strings, f"{total_time} min")

        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item.widget(), Steps):
                old_widget = item.widget()
                self.layout().replaceWidget(old_widget, self.steps_widget)
                old_widget.deleteLater()
                break
