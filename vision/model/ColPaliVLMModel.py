from PyQt6.QtCore import QObject, pyqtSignal
from byaldi import RAGMultiModalModel

from util.Utility import Utility
from vision.model.ColPaliThread import ColPaliThread
from util.Constants import FILE_INDEX_MESSAGE


class ColPaliVLMModel(QObject):
    thread_started_signal = pyqtSignal()
    thread_finished_signal = pyqtSignal()
    file_index_error_signal = pyqtSignal(str)
    file_index_finished_signal = pyqtSignal(str, str, float)
    colpali_rag_signal = pyqtSignal(RAGMultiModalModel)

    def __init__(self):
        super().__init__()
        self.colpali_thread = None
        self.colpali_rag = None

    def indexing_files(self, args):
        if self.colpali_thread is not None and self.colpali_thread.isRunning():
            print(f"{FILE_INDEX_MESSAGE.THREAD_RUNNING}")
            self.colpali_thread.wait()

        self.colpali_thread = ColPaliThread(args)
        self.colpali_thread.started.connect(self.thread_started_signal.emit)
        self.colpali_thread.finished.connect(self.handle_thread_finished)
        self.colpali_thread.file_index_error_signal.connect(self.file_index_error_signal.emit)
        self.colpali_thread.file_index_finished_signal.connect(self.file_index_finished_signal.emit)
        self.colpali_thread.colpali_rag_signal.connect(self.handle_colpali_rag)
        self.colpali_thread.start()

    def handle_thread_finished(self):
        print(f"{FILE_INDEX_MESSAGE.THREAD_FINISHED}")
        self.thread_finished_signal.emit()
        self.colpali_thread = None

    def handle_colpali_rag(self, rag):
        self.colpali_rag = rag

    def get_colpali_search_result(self, text, k_nearest, image_size):
        file_list = []
        colpali_search_results = self.colpali_rag.search(text, k=k_nearest)
        for result in colpali_search_results:
            if image_size:
                image_file = Utility.resize_image(
                    Utility.create_temp_file(result.base64, "png", True),
                    image_size
                )
                file_list.append(image_file)
            else:
                file_list.append(Utility.create_temp_file(result.base64, "png", True))
        return file_list

    def force_stop(self):
        if self.colpali_thread is not None:
            self.colpali_thread.set_force_stop(True)
