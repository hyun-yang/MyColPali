from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton

from util.Constants import UI


class RenameDialog(QDialog):
    def __init__(self, title, name):
        super().__init__()
        self.setWindowTitle(title)

        self.layout = QVBoxLayout()

        self.title_label = QLabel(UI.LABEL_ENTER_NEW_NAME, self)
        self.layout.addWidget(self.title_label)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(name)
        self.layout.addWidget(self.name_edit)

        self.name_edit.textChanged.connect(self.on_text_changed)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton(UI.OK, self)
        self.cancel_button = QPushButton(UI.CANCEL, self)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button.clicked.connect(self.close)

        self.setLayout(self.layout)

    @pyqtSlot()
    def on_text_changed(self):
        self.ok_button.setEnabled(bool(self.name_edit.text().strip()))

    @property
    def text(self):
        return self.name_edit.text()
