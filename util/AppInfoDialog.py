from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy

from util.Constants import UI, Constants


class AppInfoDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(UI.ABOUT_TIP)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        layout = QVBoxLayout()

        about_text = Constants.ABOUT_TEXT

        about_label = QLabel(about_text)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_label.setOpenExternalLinks(True)
        layout.addWidget(about_label)

        ok_button = QPushButton(UI.OK)
        ok_button.clicked.connect(self.accept)
        ok_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        ok_button.setMaximumWidth(self.width() // 2)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
