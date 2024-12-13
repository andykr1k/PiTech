import ast
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFormLayout, QFrame, QScrollArea, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid
from functools import partial

class UnloadLoadPage(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.grid_state = self.parse_grid_state(self.get_grid_state())
        self.unload_load_list = []
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title_label = QLabel("Tap to Unload and Type to Load")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2F27CE;")
        main_layout.addWidget(title_label)

        unload_load_layout = QHBoxLayout()

        unload_layout = QVBoxLayout()
        self.setup_unload_page(unload_layout)

        load_layout = QVBoxLayout()
        self.setup_load_page(load_layout)

        unload_load_layout.addLayout(unload_layout, 2)
        unload_load_layout.addLayout(load_layout, 1)


        main_layout.addLayout(unload_load_layout)
        confirm_button = QPushButton("Confirm")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
            QPushButton:pressed {
                background-color: #3949AB;
            }
        """)
        confirm_button.clicked.connect(self.confirm_load_info)
        main_layout.addWidget(confirm_button)
        if self.layout() is not None:
            old_layout = self.layout()
            old_layout.setParent(None)

        self.setLayout(main_layout)
        self.setWindowFlag(Qt.FramelessWindowHint, False)
        self.setModal(True)
        self.resize(800, 400)
        self.center()

    # Set up the middle section with the grid container
    def setup_unload_page(self, layout):
        middle_section = QHBoxLayout()
        grid_container = QFrame()
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setAlignment(Qt.AlignCenter)
        grid = Grid(self, static=False, gridState=self.grid_state)
        grid_layout.addWidget(grid.visualizeGrid())
        middle_section.addWidget(grid_container)
        layout.addLayout(middle_section)

    # Set up the right section with the form to load containers
    def setup_load_page(self, layout):
        form_layout = QFormLayout()

        input_style = """
            QLineEdit {
                background-color: #FFFFFF;
                color: black;
                border: 1px solid #D1D1D1;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3F51B5;
            }
        """

        self.container_name_input = QLineEdit()
        self.container_name_input.setPlaceholderText("Enter container name")
        self.container_name_input.setStyleSheet(input_style)

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight")
        self.weight_input.setStyleSheet(input_style)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setStyleSheet(input_style)

        form_layout.addRow(self.create_label("Container Name"), self.container_name_input)
        form_layout.addRow(self.create_label("Weight"), self.weight_input)
        form_layout.addRow(self.create_label("Quantity"), self.quantity_input)

        submit_button = QPushButton("Add Container(s)")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
            QPushButton:pressed {
                background-color: #3949AB;
            }
        """)
        submit_button.clicked.connect(self.submit_load_info)

        layout.addLayout(form_layout)
        layout.addWidget(submit_button)

        self.container_list_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3F51B5;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.container_list_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #3F51B5;
            margin-bottom: 5px;
        """)
        return label

    # Submit the load information to the list
    def submit_load_info(self):
        container_name = self.container_name_input.text().strip()
        weight = self.weight_input.text().strip()
        quantity = self.quantity_input.text().strip()

        # Validation checks
        if not container_name:
            self.show_error_message("Container name cannot be empty.")
            return
        if not (1 <= len(container_name) <= 255):
            self.show_error_message("Container name must be between 1 and 255 characters.")
            return
        if not container_name.isalnum() and "_" not in container_name:
            self.show_error_message("Container name can only contain alphanumeric characters and underscores.")
            return
        if not container_name[0].isalpha():
            self.show_error_message("Container name must start with a letter.")
            return
        if not weight.isdigit() or float(weight) < 0:
            self.show_error_message("Weight must be a non-negative number.")
            return
        if not quantity.isdigit() or int(quantity) < 1:
            self.show_error_message("Quantity must be an integer of 1 or higher.")
            return

        # Add container(s) to the list
        for _ in range(int(quantity)):
            self.unload_load_list.append(f"load,{container_name},{weight}")
        self.container_name_input.clear()
        self.weight_input.clear()
        self.quantity_input.clear()

        self.update_container_list_display()

    # Confirm the load information and update the database
    def confirm_load_info(self):
        self.update_unload_and_load_lists()
        self.accept()

    # Switch to the load page
    def switch_to_load_page(self):
        self.is_load_page = True
        self.initUI()

    # Fetch the grid state from the parent
    def get_grid_state(self):
        return self.parent.fetch_grid_state()

    # Parse the grid state from a string to a dictionary
    def parse_grid_state(self, string_grid):
        return ast.literal_eval(string_grid)

    # Update the unload and load lists in the database
    def update_unload_and_load_lists(self):
        self.parent.db.update_by_id("Lists", "id", 1, {"UnloadLoadList": str(self.unload_load_list)})

    # Update the container list display
    def update_container_list_display(self):
        print("Updated Container List:", self.unload_load_list)

        while self.container_list_layout.count():
            item = self.container_list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for container in self.unload_load_list:
            container_widget = QHBoxLayout()
            container_widget.setContentsMargins(10, 5, 10, 5)
            container_widget.setSpacing(15)

            container_label = QLabel(container)
            container_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                border: none;
                color: #333;
            """)
            container_widget.addWidget(container_label)

            remove_button = QPushButton("Remove")
            remove_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF5252;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #FF1744;
                }
                QPushButton:pressed {
                    background-color: #D50000;
                }
            """)
            remove_button.clicked.connect(partial(self.remove_container, container))
            container_widget.addWidget(remove_button)

            container_frame = QFrame()
            container_frame.setLayout(container_widget)
            container_frame.setStyleSheet("""
                QFrame {
                    background-color: #F7F7F7;
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 5px;
                    max-height: 40px
                }
            """)
            self.container_list_layout.addWidget(container_frame)


    # Remove the specified container and refresh the display
    def remove_container(self, container):
        if container in self.unload_load_list:
            self.unload_load_list.remove(container)
            self.update_container_list_display()

    # Center the dialog on the screen
    def center(self):
        screen_geometry = self.screen().geometry()
        dialog_geometry = self.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.move(x, y)

    def show_error_message(self, message):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setWindowTitle("Error")
        error_message.setText(message)
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.exec_()