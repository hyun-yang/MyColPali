from PyQt6.QtCore import QObject, pyqtSignal

from util.Constants import AIProviderName, MODEL_MESSAGE
from vision.model.OpenAIVisionThread import OpenAIVisionThread


class AIThreadFactory:
    @staticmethod
    def create_thread(args, llm):
        if llm == AIProviderName.OPENAI.value:
            return OpenAIVisionThread(args)
        else:
            raise ValueError(f"{MODEL_MESSAGE.MODEL_UNSUPPORTED} {llm}")


class VisionModel(QObject):
    thread_started_signal = pyqtSignal()
    thread_finished_signal = pyqtSignal()
    response_signal = pyqtSignal(str, bool)
    response_finished_signal = pyqtSignal(str, str, float, bool)

    def __init__(self):
        super().__init__()
        self.ai_thread = None

    def send_user_input(self, args, llm):
        if self.ai_thread is not None and self.ai_thread.isRunning():
            print(f"{MODEL_MESSAGE.THREAD_RUNNING}")
            self.ai_thread.wait()

        self.ai_thread = AIThreadFactory.create_thread(args, llm)
        self.ai_thread.started.connect(self.thread_started_signal.emit)
        self.ai_thread.finished.connect(self.handle_thread_finished)
        self.ai_thread.response_signal.connect(self.response_signal.emit)
        self.ai_thread.response_finished_signal.connect(self.response_finished_signal.emit)
        self.ai_thread.start()

    def handle_thread_finished(self):
        print(f"{MODEL_MESSAGE.THREAD_FINISHED}")
        self.thread_finished_signal.emit()
        self.ai_thread = None

    def force_stop(self):
        if self.ai_thread is not None:
            self.ai_thread.set_force_stop(True)
