from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QSpacerItem, QSizePolicy, QFrame, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import re

class Steps(QWidget):
    def __init__(self, steps_list, current_step, total_time, parent):
        super().__init__()
        self.steps_list = steps_list
        self.current_step = current_step
        self.total_time = total_time
        self.parent = parent
        self.done_button = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        steps_container = self.create_steps_container()
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setAlignment(Qt.AlignTop)

        if self.current_step == "COMPLETED":
            steps_title = self.create_label("Operation Completed", 20, bold=True)
            steps_layout.addWidget(steps_title)
            steps_layout.addItem(self.create_spacer())
            download_button = self.create_button(
                "Download Outbound Manifest",
                self.download_outbound_clicked,
                "#6200EE",
                "#3700B3"
            )
            steps_layout.addWidget(download_button)
            self.done_button = self.create_button(
                "Done",
                self.done_button_clicked,
                "#6200EE",
                "#3700B3"
            )
            self.done_button.setEnabled(False)
            steps_layout.addWidget(self.done_button)
            main_layout.addWidget(steps_container)
            return

        if self.current_step[0] == 1 and self.current_step[4] == "NOT STARTED":
            steps_title = self.create_label("Steps", 20, bold=True)
            steps_layout.addWidget(steps_title)
            steps_widget = self.create_steps_widget(self.steps_list)
            steps_layout.addWidget(self.create_scroll_area(steps_widget))
            steps_layout.addItem(self.create_spacer())
            steps_layout.addWidget(self.create_label(f"Total Time: {self.total_time}", 16, bold=True))
            steps_layout.addWidget(self.create_button("Start", self.start_button_clicked, "#6200EE", "#3700B3"))
        else:
            steps_title = self.create_label("Steps", 20, bold=True)
            steps_layout.addWidget(steps_title)
            self.parent.parent.update_current_step_in_db(self.current_step, "STARTED")
            steps_widget = self.create_steps_widget([self.current_step])
            steps_layout.addWidget(self.create_scroll_area(steps_widget))
            steps_layout.addItem(self.create_spacer())
            steps_layout.addWidget(self.create_label(f"Total Time: {self.total_time}", 16, bold=True))
            steps_layout.addWidget(self.create_button("Confirm", self.confirm_button_clicked, "#28a745", "#218838"))

        main_layout.addWidget(steps_container)

    def create_steps_container(self):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                border: 1px solid #CCCCCC;
                border-radius: 16px;
                background-color: #FFFFFF;
                padding: 20px;
            }
        """)
        return container

    def create_label(self, text, font_size, bold=False):
        label = QLabel(text)
        label.setFont(QFont("Arial", font_size, QFont.Bold if bold else QFont.Normal))
        label.setStyleSheet("""
            color: #333333;
            background-color: #FAFAFA;
            padding: 12px 20px;
            border-radius: 10px;
        """)
        label.setAlignment(Qt.AlignCenter)
        return label

    def create_button(self, text, callback, bg_color, hover_color):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 16, QFont.Bold))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 12px 20px;
                border-radius: 10px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        button.clicked.connect(callback)
        return button

    def create_spacer(self):
        return QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def create_steps_widget(self, steps):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)

        for step in steps:
            pos1 = self.correct_moves(step[1])
            pos2 = self.correct_moves(step[2])
            time = step[3]
            if (pos1 == "truck" and pos2 == "crane"):
                label = f"Move crane from {pos1} to original crane position (8,0) in {time} minutes."
            else:
                label = f"Move container from {pos1} to {pos2} in {time} minutes."
            layout.addWidget(self.create_label(label, 14))
        return widget

    def create_scroll_area(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll_area

    def start_button_clicked(self):
        self.parent.parent.update_current_step_in_db(self.current_step, "STARTED")
        self.parent.update_operations_page()

    def confirm_button_clicked(self):
        self.parent.parent.update_current_step_in_db(self.current_step, "COMPLETED")
        self.parent.update_operations_page()

    def download_outbound_clicked(self):
        list_object = self.parent.parent.db.fetch_one("Lists", "id = ?", params=(1,))
        # manifest = list_object[5]
        # manifest_name = list_object[6]
        manifest = "Manifest Content"
        manifest_name = "OutboundManifestName.txt"

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Manifest", manifest_name, "All Files (*)", options=options
        )

        if save_path:
            try:
                with open(save_path, 'w') as file:
                    file.write(manifest)
                if self.done_button:
                    self.done_button.setEnabled(True)
            except Exception as e:
                print(f"Error saving file: {e}")


    def done_button_clicked(self):
        self.parent.parent.db.update_by_id("profile", "id", 1, {"currentTab": "Home"})
        self.parent.parent.add_log_entry(f"Operation Completed")
        self.parent.parent.db.drop_table("Lists")
        self.parent.parent.db.create_table(
            "Lists", "id INTEGER PRIMARY KEY, UnloadLoadList TEXT, Manifest TEXT, ManifestName TEXT, OutboundManifest TEXT, OutboundManifestName TEXT")
        self.parent.parent.home_page.header.resetManifest()
        self.parent.parent.setCurrentIndex(1)

    def correct_moves(self, string):
        if string not in ["(-1,-1)", "(8,0)", "(4,0)"]:
            # parsedLine = re.findall(r'((\d+),(\d+))', string)
            # y = parsedLine[0][1]
            # x = parsedLine[0][2]
            # return f"({x},{y})"
            return string
        else:
            if string == "(-1,-1)":
                return "truck"
            else:
                return "crane"
