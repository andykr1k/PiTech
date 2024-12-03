from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor
import random


class Grid:
    def __init__(self, gridState=None) -> None:
        self.rows = 8
        self.columns = 12
        self.container_colors = []
        self.buttons = {}

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

        for row in range(self.rows):
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_widget.setLayout(row_layout)

            for col in range(self.columns):
                cell = QPushButton()
                cell.setFixedSize(65, 65)

                self.buttons[(row, col)] = cell

                self.update_button_color(cell, row, col)

                cell.row = row
                cell.col = col

                cell.clicked.connect(lambda checked, r=row,
                                     c=col: self.cell_clicked(r, c))

                row_layout.addWidget(cell)

            row_layout.setSpacing(0)
            row_layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(row_widget)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def update_button_color(self, button, row, col):
        state = self.gridState[row][col]
        if state == 'NAN':
            button.setStyleSheet(
                "background-color: black; border: 0.5px solid black;")
        elif state == 'UNUSED':
            button.setStyleSheet(
                "background-color: grey; border: 0.5px solid black;")
        elif state == 'CONTAINER':
            color = self.get_random_color()
            button.setStyleSheet(
                f"background-color: {color}; border: 0.5px solid black;")

    def cell_clicked(self, r, c):
        current_state = self.gridState[r][c]

        if current_state == 'UNUSED':
            self.gridState[r][c] = 'CONTAINER'
        elif current_state == 'CONTAINER':
            self.gridState[r][c] = 'NAN'
        elif current_state == 'NAN':
            self.gridState[r][c] = 'UNUSED'

        button = self.buttons[(r, c)]
        self.update_button_color(button, r, c)

    def get_random_color(self):
        while True:
            color = QColor(random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            color_str = color.name()
            if color_str not in self.container_colors:
                self.container_colors.append(color_str)
                return color_str
