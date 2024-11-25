from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid
from Frontend.Components.Steps import Steps

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
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Top Section: Log and Sign In Buttons
        top_section = QHBoxLayout()
        top_section.setContentsMargins(0, 0, 0, 0)

        # Log Button
        self.log_button = QPushButton("Log")
        self.log_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.log_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 10px; border-radius: 10px;")
        self.log_button.clicked.connect(self.goToLogPage)
        top_section.addWidget(self.log_button)

        # Spacer to push Sign In button to the right
        top_section.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Sign In Button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.setFont(QFont("Arial", 12, QFont.Bold))
        sign_in_button.setStyleSheet("background-color: #2F27CE; color: white; padding: 10px; border-radius: 10px;")
        top_section.addWidget(sign_in_button)

        # Add top section to main layout
        main_layout.addLayout(top_section)

        # Page Title
        title_label = QLabel("_______ Operation")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2F27CE;")
        main_layout.addWidget(title_label)

        # Middle Section: Grid and Steps
        middle_section = QHBoxLayout()

        # Grid Container
        grid_container = QFrame()
        grid_container.setStyleSheet(
            """
            QFrame {
                border: 2px solid rgba(47, 39, 206, 0.5);
                border-radius: 15px;
                background-color: #F5F5F5;
                padding: 15px;
            }
            """
        )
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setAlignment(Qt.AlignCenter)
        grid = Grid(test_grid_state)
        grid_layout.addWidget(grid.visualizeGrid())
        middle_section.addWidget(grid_container)

        # Steps
        steps_list = ["Step 1: 1 min", "Step 2: 2 min", "Step 3: 3 min", "Step 5: 5 min"]
        steps_widget = Steps(steps_list, "14 min")
        middle_section.addWidget(steps_widget)

        main_layout.addLayout(middle_section)
        self.setLayout(main_layout)

        # Bottom Section: Log Input and Arrow Button
        bottom_section = QHBoxLayout()

        # Log Input
        input_field = QLineEdit()
        input_field.setFont(QFont("Arial", 12))
        input_field.setPlaceholderText("Comment in log")
        input_field.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid gray;")
        bottom_section.addWidget(input_field)

        # Arrow Button
        arrow_button = QPushButton("➔")
        arrow_button.setFont(QFont("Arial", 14, QFont.Bold))
        arrow_button.setStyleSheet(
            "background-color: #2F27CE; color: white; padding: 10px; border-radius: 10px;"
        )
        bottom_section.addWidget(arrow_button)

        main_layout.addLayout(bottom_section)

        # Adjust widths
        bottom_section.setStretch(0, 7)  # Text input stretches more
        bottom_section.setStretch(1, 1)  # Arrow button takes less space

        # Set the main layout
        self.setLayout(main_layout)

    def goToLogPage(self):
        self.stacked_widget.setCurrentIndex(4)