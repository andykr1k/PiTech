from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Steps(QWidget):
    def __init__(self, steps_list, current_step, total_time, parent):
        super().__init__()
        self.steps_list = steps_list
        self.current_step = current_step
        self.total_time = total_time
        self.parent = parent
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        steps_container = QFrame()
        steps_container.setStyleSheet(
            """
            QFrame {
                border: 1px solid #CCCCCC;
                border-radius: 16px;
                background-color: #FFFFFF;
                padding: 20px;
            }
            """
        )
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setAlignment(Qt.AlignTop)

        steps_title = QLabel("Steps")
        steps_title.setFont(QFont("Arial", 20, QFont.Bold))
        steps_title.setStyleSheet(
            """
            color: #333333;
            background-color: #FAFAFA;
            padding: 12px 20px;
            border-radius: 10px;                
        """)
        steps_title.setAlignment(Qt.AlignCenter)
        steps_layout.addWidget(steps_title)

        if self.current_step[0] == 1 and self.current_step[4] == "NOT STARTED":
            steps_widget = QWidget()
            steps_widget_layout = QVBoxLayout(steps_widget)
            steps_widget_layout.setAlignment(Qt.AlignTop)

            for step in self.steps_list:
                label = "Move container from " + step[1] + " to " + step[2] + " in " + str(step[3]) + " minutes."
                step_label = QLabel(label)
                step_label.setFont(QFont("Arial", 14))
                step_label.setStyleSheet(
                    """
                    color: #333333;
                    background-color: #FAFAFA;
                    padding: 12px 20px;
                    border-radius: 10px;
                    margin-bottom: 4px;
                    """
                )
                steps_widget_layout.addWidget(step_label)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(steps_widget)
            scroll_area.setStyleSheet("border: none;")
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            steps_layout.addWidget(scroll_area)

            steps_layout.addSpacerItem(QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            total_time_label = QLabel(f"Total Time: {self.total_time}")
            total_time_label.setFont(QFont("Arial", 16, QFont.Bold))
            total_time_label.setStyleSheet("""
                    color: #333333;
                    background-color: #FAFAFA;
                    padding: 12px 20px;
                    border-radius: 10px;
                    """)
            total_time_label.setAlignment(Qt.AlignCenter)
            steps_layout.addWidget(total_time_label)

            self.start_button = QPushButton("Start")
            self.start_button.setFont(QFont("Arial", 16, QFont.Bold))
            self.start_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #6200EE;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 10px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3700B3;
                }
                """
            )
            self.start_button.clicked.connect(self.start_button_clicked)
            steps_layout.addWidget(self.start_button)

            main_layout.addWidget(steps_container)
        else:
            self.parent.parent.update_current_step_in_db(self.steps_list, "STARTED")

            steps_widget = QWidget()
            steps_widget_layout = QVBoxLayout(steps_widget)
            steps_widget_layout.setAlignment(Qt.AlignTop)

            label = "Move container from " + self.current_step[1] + " to " + self.current_step[2] + " in " + str(self.current_step[3]) + " minutes."
            current_step_label = QLabel(label)
            current_step_label.setFont(QFont("Arial", 14))
            current_step_label.setStyleSheet(
                """
                color: #333333;
                background-color: #FAFAFA;
                padding: 12px 20px;
                border-radius: 10px;                    
                margin-bottom: 4px;
                """
            )
            steps_widget_layout.addWidget(current_step_label)


            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(steps_widget)
            scroll_area.setStyleSheet("border: none;")
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            steps_layout.addWidget(scroll_area)

            steps_layout.addSpacerItem(QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            total_time_label = QLabel(f"Total Time: {self.total_time}")
            total_time_label.setFont(QFont("Arial", 16, QFont.Bold))
            total_time_label.setStyleSheet("""
                    color: #333333;
                    background-color: #FAFAFA;
                    padding: 12px 20px;
                    border-radius: 10px;
                    """)
            total_time_label.setAlignment(Qt.AlignCenter)
            steps_layout.addWidget(total_time_label)

            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.setFont(QFont("Arial", 16, QFont.Bold))
            self.confirm_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 10px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
                """
            )
            self.confirm_button.clicked.connect(self.confirm_button_clicked)
            steps_layout.addWidget(self.confirm_button)

            main_layout.addWidget(steps_container)


    def start_button_clicked(self):
        self.parent.parent.update_current_step_in_db(self.steps_list, "STARTED")


    def confirm_button_clicked(self):
        self.parent.parent.update_current_step_in_db(self.steps_list, "COMPLETED")
