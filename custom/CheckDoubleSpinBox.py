from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QLabel, QDoubleSpinBox


class CheckDoubleSpinBox(QWidget):
    valueChanged = pyqtSignal(float)

    def __init__(self, spin_box_name=None, check_box_name=None, parent=None):
        super().__init__(parent)

        self.label = QLabel(spin_box_name, self)

        self.spin_box = QDoubleSpinBox(self)
        self.spin_box.setObjectName(spin_box_name)

        self.spin_box.valueChanged.connect(self.on_value_changed)

        self.check_box = QCheckBox(check_box_name, self)
        self.check_box.setObjectName(check_box_name)
        self.check_box.setChecked(False)

        self.check_box.stateChanged.connect(self.on_check_box_changed)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.spin_box)
        layout.addWidget(self.check_box)
        self.setLayout(layout)

    def on_value_changed(self, value):
        self.valueChanged.emit(value)

    def on_check_box_changed(self, state):
        self.spin_box.setDisabled(state == Qt.CheckState.Checked.value)
