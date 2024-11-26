from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Steps(QWidget):
    def __init__(self, steps_list, total_time):
        super().__init__()
        self.steps_list = steps_list
        self.total_time = total_time
        self.initUI()

    def initUI(self):
        # Main container layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Steps container with styling
        steps_container = QFrame()
        steps_container.setStyleSheet(
            """
            QFrame {
                border: 2px solid rgba(47, 39, 206, 0.5);
                border-radius: 15px;
                background-color: #F5F5F5;
                padding: 15px;
            }
            """
        )
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setAlignment(Qt.AlignTop)

        # Steps title
        steps_title = QLabel("_______ Steps")
        steps_title.setFont(QFont("Arial", 18, QFont.Bold))
        steps_title.setStyleSheet("color: black;")
        steps_title.setAlignment(Qt.AlignCenter)
        steps_layout.addWidget(steps_title)

        # Steps widget with scrollable area
        steps_widget = QWidget()
        steps_widget_layout = QVBoxLayout(steps_widget)
        steps_widget_layout.setAlignment(Qt.AlignTop)

        for step in self.steps_list:
            step_label = QLabel(step)
            step_label.setFont(QFont("Arial", 14))
            step_label.setStyleSheet("color: black; border: 2px solid rgba(47, 39, 206, 0.5);")
            steps_widget_layout.addWidget(step_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(steps_widget)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        steps_layout.addWidget(scroll_area)

        # Spacer for alignment
        steps_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Total time label
        total_time_label = QLabel(f"Total Time: {self.total_time}")
        total_time_label.setFont(QFont("Arial", 16, QFont.Bold))
        total_time_label.setStyleSheet("color: black; border: none;")
        total_time_label.setAlignment(Qt.AlignCenter)
        steps_layout.addWidget(total_time_label)

        main_layout.addWidget(steps_container)

        # Start button
        start_button = QPushButton("Start")
        start_button.setFont(QFont("Arial", 14, QFont.Bold))
        start_button.setStyleSheet("background-color: #008000; padding: 10px; border-radius: 10px;")
        start_button_layout = QHBoxLayout()
        start_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        start_button_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        start_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        main_layout.addLayout(start_button_layout)
