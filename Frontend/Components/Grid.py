from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor
import random
import re

class Grid:
    def __init__(self, parent, static=True, gridState=None, current_move=None) -> None:
        self.parent = parent
        self.rows = 8
        self.columns = 12
        self.container_colors = ["green"]
        self.buttons = {}
        self.current_move = current_move
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
            color = self.get_color(row, col, 2, False)
            button.setStyleSheet(f"background-color: {color}; border: 0.5px solid black;")
            button.setText("")
        else:
            color = "cyan"
            if tapped:
                color = "green"
            else:
                color = self.get_color(row, col, 1, True)
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

    def get_random_color(self):
        while True:
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            color_str = color.name()
            if color_str not in self.container_colors:
                self.container_colors.append(color_str)
                return color_str

    def get_color(self, row, col, curr, from_to):
        if (self.current_move is not None and self.current_move[4] == "STARTED"):
            x, y = self.parse_positions(self.current_move[curr])
            if (from_to):
                if (x, y) not in [(-1,-1), (8,0), (4,0)] and (y == row and x == col):
                    return "red"
                else:
                    return "cyan"
            else:
                if (x, y) not in [(-1,-1), (8,0), (4,0)] and (y == row and x == col):
                    return "green"
                else:
                    return "grey"
        else:
            if (from_to):
                return "cyan"
            else:
                return "grey"

    def parse_positions(self, string):
        if string not in ["(-1,-1)", "(8,0)", "(4,0)"]:
            parsedLine = re.findall(r'((\d+),(\d+))', string)
            y = parsedLine[0][1]
            x = parsedLine[0][2]
            return int(x), int(y)
        else:
            return -1, -1