from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QLabel, QLineEdit


class CheckLineEdit(QWidget):
    textChanged = pyqtSignal(str)

    def __init__(self, line_edit_name=None, check_box_name=None, parent=None):
        super().__init__(parent)

        self.label = QLabel(line_edit_name, self)

        self.line_edit = QLineEdit(self)
        self.line_edit.setObjectName(line_edit_name)

        self.line_edit.textChanged.connect(self.on_text_changed)

        self.check_box = QCheckBox(check_box_name, self)
        self.check_box.setObjectName(check_box_name)
        self.check_box.setChecked(False)

        self.check_box.stateChanged.connect(self.on_check_box_changed)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.check_box)
        self.setLayout(layout)

    def on_text_changed(self, value):
        self.textChanged.emit(value)

    def on_check_box_changed(self, state):
        self.line_edit.setDisabled(state == Qt.CheckState.Checked.value)
