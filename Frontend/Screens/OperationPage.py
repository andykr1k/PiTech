from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid

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
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.titleLabel = QLabel("PiTech Operations Page")
        self.titleLabel.setFont(QFont("Arial", 28, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: #2F27CE;")
        layout.addWidget(self.titleLabel)

        grid = Grid(test_grid_state)
        layout.addWidget(grid.visualizeGrid())


        main_layout.addLayout(layout)

        self.setLayout(main_layout)