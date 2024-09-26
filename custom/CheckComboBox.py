from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QCheckBox, QHBoxLayout


class CheckComboBox(QWidget):
    currentTextChanged = pyqtSignal(str)

    def __init__(self, combo_box_name=None, check_box_name=None, parent=None):
        super().__init__(parent)

        self.label = QLabel(combo_box_name, self)

        self.combo_box = QComboBox(self)
        self.combo_box.setObjectName(combo_box_name)
        self.combo_box.currentTextChanged.connect(self.on_current_text_changed)

        self.check_box = QCheckBox(check_box_name, self)
        self.check_box.setObjectName(check_box_name)
        self.check_box.setChecked(False)
        self.check_box.stateChanged.connect(self.on_check_box_changed)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.check_box)
        self.setLayout(layout)

    def on_current_text_changed(self, current_text):
        self.currentTextChanged.emit(current_text)

    def on_check_box_changed(self, state):
        self.combo_box.setDisabled(state == Qt.CheckState.Checked.value)
