from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor
import random


class Grid:
    def __init__(self, parent, static=True, gridState=None) -> None:
        self.parent = parent
        self.rows = 8
        self.columns = 12
        self.container_colors = ["green"]
        self.buttons = {}
        self.static = static

        if gridState:
            self.gridState = gridState
        else:
            self.gridState = self.initialize_grid_state()

    def initialize_grid_state(self):
        return [['UNUSED' for _ in range(self.columns)] for _ in range(self.rows)]

    def visualizeGrid(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        for row in range(self.rows - 1, -1, -1):
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_widget.setLayout(row_layout)

            for col in range(self.columns):
                cell = QPushButton()
                cell.setFixedSize(65, 65)

                self.buttons[(row, col)] = cell

                self.update_button_color(cell, row, col, False)

                cell.row = row
                cell.col = col
                if not self.static:
                    cell.clicked.connect(lambda checked, r=row, c=col: self.cell_clicked(r, c))

                row_layout.addWidget(cell)

            row_layout.setSpacing(0)
            row_layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(row_widget)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def update_button_color(self, button, row, col, tapped):
        state = self.gridState[row][col]
        if state == 'NAN':
            button.setStyleSheet("background-color: black; border: 0.5px solid black;")
            button.setText("")
        elif state == 'UNUSED':
            button.setStyleSheet("background-color: grey; border: 0.5px solid black;")
            button.setText("")
        else:
            if tapped:
                color = "green"
            else:
                color = self.get_random_color()
            button.setStyleSheet(f"background-color: {color}; border: 0.5px solid black;")
            button.setText(state)

    def cell_clicked(self, r, c):
        current_state = self.gridState[r][c]
        button = self.buttons[(r, c)]

        if current_state == 'UNUSED':
            container_name = f"Container {r},{c}"
            self.gridState[r][c] = container_name
            self.update_button_color(button, r, c, False)
        elif current_state == 'NAN':
            self.gridState[r][c] = 'NAN'
            self.update_button_color(button, r, c, False)
        else:
            self.parent.unload_load_list.append("unload," + current_state)
            self.update_button_color(button, r, c, True)
            print(self.parent.unload_load_list)

    def get_random_color(self):
        while True:
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            color_str = color.name()
            if color_str not in self.container_colors:
                self.container_colors.append(color_str)
                return color_str
