from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox


class ConfirmationDialog(QDialog):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.message = message
        self.initialize_ui()

    def initialize_ui(self):
        layout = QVBoxLayout()

        prompt_label = QLabel(self.message)
        layout.addWidget(prompt_label)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)

        # Set 'No' button as the default
        no_button = button_box.button(QDialogButtonBox.StandardButton.No)
        if no_button:
            no_button.setDefault(True)
            no_button.setFocus()

        yes_button = button_box.button(QDialogButtonBox.StandardButton.Yes)
        if yes_button:
            yes_button.setAutoDefault(False)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)
