from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve

from util.Constants import UI


class AnimatedProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self._initialize_ui()

    def _initialize_ui(self):

        self.setValue(0)
        self.setTextVisible(False)
        self.loading_animation = QPropertyAnimation(self, b"value")

        self.setStyleSheet(UI.PROGRESS_BAR_STYLE)
        self.loading_animation.setStartValue(self.minimum())
        self.loading_animation.setEndValue(self.maximum())

        self.loading_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.loading_animation.setDuration(1500)

    def show_progress_bar(self, value):
        self.setValue(value)
        if self.loading_animation.currentValue() == self.loading_animation.endValue():
            self.loading_animation.setDirection(QAbstractAnimation.Direction.Backward)
            self.setInvertedAppearance(True)
            self.loading_animation.start()
        elif self.loading_animation.currentValue() == self.loading_animation.startValue():
            self.loading_animation.setDirection(QAbstractAnimation.Direction.Forward)
            self.setInvertedAppearance(False)
            self.loading_animation.start()

    def start_animation(self):
        self.loading_animation.valueChanged.connect(self.show_progress_bar)
        self.loading_animation.start()

    def stop_animation(self):
        self.loading_animation.valueChanged.disconnect(self.show_progress_bar)
        self.loading_animation.stop()
