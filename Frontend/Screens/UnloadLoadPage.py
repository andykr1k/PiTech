import ast
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFormLayout, QFrame, QScrollArea, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Frontend.Components.Grid import Grid

class UnloadLoadPage(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.grid_state = self.parse_grid_state(self.get_grid_state())
        self.unload_load_list = []
        self.is_load_page = False
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title_label = QLabel("Tap to Unload Container and Type to Load Containers")
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
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
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

    def setup_unload_page(self, layout):
        middle_section = QHBoxLayout()
        grid_container = QFrame()
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setAlignment(Qt.AlignCenter)
        grid = Grid(self, static=False, gridState=self.grid_state)
        grid_layout.addWidget(grid.visualizeGrid())
        middle_section.addWidget(grid_container)
        layout.addLayout(middle_section)

    def setup_load_page(self, layout):
        form_layout = QFormLayout()

        self.container_name_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.quantity_input = QLineEdit()

        form_layout.addRow("Container Name:", self.container_name_input)
        form_layout.addRow("Weight:", self.weight_input)
        form_layout.addRow("Quantity:", self.quantity_input)

        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
            background-color: #3F51B5;
            color: white;
            padding: 8px 20px;
            border-radius: 4px;
            font-weight: 600;
        """)
        submit_button.clicked.connect(self.submit_load_info)


        layout.addLayout(form_layout)
        layout.addWidget(submit_button)

        self.container_list_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.container_list_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

    def submit_load_info(self):
        container_name = self.container_name_input.text().strip()
        weight = self.weight_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if container_name and weight and quantity:
            for _ in range(int(quantity)):
                self.unload_load_list.append("load," + container_name + "," + weight)
            self.container_name_input.clear()
            self.weight_input.clear()
            self.quantity_input.clear()

            self.update_container_list_display()

    def confirm_load_info(self):
        self.update_unload_and_load_lists()
        self.accept()

    def switch_to_load_page(self):
        self.is_load_page = True
        self.initUI()

    def get_grid_state(self):
        return self.parent.fetch_grid_state()

    def parse_grid_state(self, string_grid):
        return ast.literal_eval(string_grid)

    def update_unload_and_load_lists(self):
        self.parent.db.update_by_id("Lists", "id", 1, {"UnloadLoadList": str(self.unload_load_list)})

    def update_container_list_display(self):
        for i in reversed(range(self.container_list_layout.count())):
            widget = self.container_list_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for container in self.unload_load_list:
            container_widget = QHBoxLayout()
            container_label = QLabel(container)
            remove_button = QPushButton("X")
            remove_button.setStyleSheet("background-color: red; color: white;")
            remove_button.clicked.connect(lambda container=container: self.remove_container(container))
            container_widget.addWidget(container_label)
            container_widget.addWidget(remove_button)

            self.container_list_layout.addLayout(container_widget)

    def remove_container(self, container):
        self.unload_load_list.remove(container)
        self.update_container_list_display()

    def center(self):
        screen_geometry = self.screen().geometry()
        dialog_geometry = self.geometry()
        x = (screen_geometry.width() - dialog_geometry.width()) // 2
        y = (screen_geometry.height() - dialog_geometry.height()) // 2
        self.move(x, y)
