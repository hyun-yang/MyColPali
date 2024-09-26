from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QTextEdit


class PromptTextEdit(QTextEdit):
    submitted_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                return super().keyPressEvent(event)
            else:
                self.submitted_signal.emit(self.toPlainText())
        else:
            return super().keyPressEvent(event)
