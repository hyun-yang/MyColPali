from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton

from custom.PromptTextEdit import PromptTextEdit
from vision.view.VisionList import VisionList
from util.Constants import Constants, UI
from util.Utility import Utility


class VisionHistory(QWidget):
    new_vision_signal = pyqtSignal(str)
    delete_vision_signal = pyqtSignal()
    filter_signal = pyqtSignal(str)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.initialize_ui()

    def initialize_ui(self):
        self.add_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'database--plus.png')), "")
        self.add_button.clicked.connect(self.add_new_vision)
        self.add_button.setToolTip(UI.ADD)

        self.delete_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'database--minus.png')), "")
        self.delete_button.clicked.connect(self.delete_vision)
        self.delete_button.setToolTip(UI.DELETE)

        self.filter_text = PromptTextEdit()
        self.filter_text.submitted_signal.connect(self.filter_list)
        self.filter_text.setPlaceholderText(UI.SEARCH_PROMPT_PLACEHOLDER)
        self.filter_text.setFixedHeight(self.add_button.sizeHint().height())
        self.filter_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.filter_text)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.add_button)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        control_layout.setContentsMargins(0, 0, 0, 0)

        control_widget = QWidget()
        control_widget.setLayout(control_layout)

        top_layout = QVBoxLayout()
        top_layout.addWidget(control_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setFixedHeight(self.add_button.sizeHint().height())

        self._vision_list = VisionList(self.model)

        main_layout = QVBoxLayout()
        main_layout.addWidget(top_widget)
        main_layout.addWidget(self._vision_list)

        self.setLayout(main_layout)

    def add_new_vision(self):
        self.new_vision_signal.emit(Constants.NEW_VISION)

    def delete_vision(self):
        self.delete_vision_signal.emit()

    def filter_list(self, text: str):
        self.filter_signal.emit(text)

    @property
    def vision_list(self):
        return self._vision_list
