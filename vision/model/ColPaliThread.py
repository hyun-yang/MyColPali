import time

from PyQt6.QtCore import QThread, pyqtSignal
from byaldi import RAGMultiModalModel

from util.Constants import Constants
from util.Utility import Utility


class ColPaliThread(QThread):
    file_index_error_signal = pyqtSignal(str)
    file_index_finished_signal = pyqtSignal(str, str, float)
    colpali_rag_signal = pyqtSignal(RAGMultiModalModel)

    def __init__(self, args):
        super().__init__()
        self.rag = None
        self.model_name = args['model_name']
        self.verbose = args['verbose']
        self.index_name = args['index_name']
        self.store_collection_with_index = args['store_collection_with_index']
        self.overwrite = args['overwrite']
        self.input_file_path = args['input_file_path']
        self.force_stop = False

    def run(self):
        self.start_time = time.time()
        try:
            self.rag = RAGMultiModalModel.from_pretrained(self.model_name, verbose=self.verbose,
                                                          device=Utility.get_torch_device())
            self.rag.index(
                input_path=self.input_file_path,
                index_name=self.index_name,
                store_collection_with_index=self.store_collection_with_index,
                overwrite=self.overwrite,
            )
            self.colpali_rag_signal.emit(self.rag)
            self.finish_run(self.model_name, Constants.NORMAL_STOP)
        except Exception as e:
            self.file_index_error_signal.emit(str(e))

    def set_force_stop(self, force_stop):

        self.force_stop = force_stop

    def finish_run(self, model, finish_reason):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.file_index_finished_signal.emit(model, finish_reason, elapsed_time)
