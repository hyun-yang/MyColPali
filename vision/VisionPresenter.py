from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, QMessageBox

from util.ChatType import ChatType
from util.ConfirmationDialog import ConfirmationDialog
from util.Constants import Constants, UI
from util.DataManager import DataManager
from util.SettingsManager import SettingsManager
from util.Utility import Utility
from vision.model.ColPaliVLMModel import ColPaliVLMModel
from vision.model.VisionListModel import VisionListModel
from vision.model.VisionModel import VisionModel
from vision.view.VisionView import VisionView


class VisionPresenter(QWidget):

    def __init__(self):
        super().__init__()
        self._vision_main_id = None
        self._vision_main_index = None
        self.colpali_rag_ready = False
        self.initialize_manager()
        self.initialize_ui()

    def initialize_manager(self):
        self._settings = SettingsManager.get_settings()
        self._database = DataManager.get_database()
        self.llm = Utility.get_settings_value(section="AI_Provider", prop="llm", default="OpenAI", save=True)

    def initialize_ui(self):
        # View
        self.visionViewModel = VisionListModel(self._database)
        self.visionViewModel.new_vision_main_id_signal.connect(self.set_vision_main_id)
        self.visionViewModel.remove_vision_signal.connect(self.clear_vision)
        self.visionView = VisionView(self.visionViewModel)

        # Model
        self.visionModel = VisionModel()

        # View signal
        self.visionView.submitted_file_signal.connect(self.indexing_file)
        self.visionView.submitted_prompt_signal.connect(self.submit)
        self.visionView.stop_signal.connect(self.visionModel.force_stop)
        self.visionView.current_llm_signal.connect(self.set_current_llm_signal)

        self.visionView.vision_history.new_vision_signal.connect(self.create_new_vision)
        self.visionView.vision_history.delete_vision_signal.connect(self.confirm_delete_vision)
        self.visionView.vision_history.vision_list.delete_id_signal.connect(self.delete_vision_table)
        self.visionView.vision_history.filter_signal.connect(self.filter_list)
        self.visionView.set_default_tab(self.llm)

        # Model signal
        self.visionModel.thread_started_signal.connect(self.visionView.start_chat)
        self.visionModel.thread_finished_signal.connect(self.visionView.finish_chat)
        self.visionModel.response_signal.connect(self.handle_response_signal)
        self.visionModel.response_finished_signal.connect(self.handle_response_finished_signal)

        # ColPali
        self.colpaliVLMModel = ColPaliVLMModel()
        self.colpaliVLMModel.file_index_finished_signal.connect(self.handle_file_index_finished_signal)

        # View
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.visionView)

        self.initialize_vision_history()

        self.setLayout(main_layout)

    def initialize_vision_history(self):
        self.vision_list = self.visionView.vision_history.vision_list
        self.vision_list.vision_id_signal.connect(self.show_vision_detail)

    def set_vision_main_id(self, vision_main_id):
        self.vision_main_id = vision_main_id
        self.view.clear_all()

    @pyqtSlot(str, bool)
    def handle_response_signal(self, result, stream):
        self.vision_text = result
        self.visionView.update_ui(self.vision_text, stream)

    @pyqtSlot(str, str, float, bool)
    def handle_response_finished_signal(self, model, finish_reason, elapsed_time, stream):
        self.visionView.update_ui_finish(model, finish_reason, elapsed_time, stream)
        self._database.insert_vision_detail(self.vision_main_id, ChatType.AI.value, model,
                                            self.view.get_last_ai_widget().get_original_text(), elapsed_time,
                                            finish_reason)

    @property
    def colpali_model(self):
        return self.colpaliVLMModel

    @property
    def model(self):
        return self.visionModel

    @property
    def view(self):
        return self.visionView

    @property
    def vision_main_id(self):
        return self._vision_main_id

    @vision_main_id.setter
    def vision_main_id(self, value):
        self._vision_main_id = value

    @pyqtSlot(str)
    def set_current_llm_signal(self, llm_name):
        self.llm = llm_name

    @pyqtSlot(int)
    def clear_vision(self, delete_id):
        if self.vision_main_id == delete_id:
            self.vision_main_id = None
            self.view.clear_all()

    @pyqtSlot()
    def confirm_delete_vision(self):
        if self.vision_main_id:
            title = UI.CONFIRM_DELETION_TITLE
            message = UI.CONFIRM_DELETION_VISION_MESSAGE
            dialog = ConfirmationDialog(title, message)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.delete_vision(self.visionViewModel.get_index_by_vision_main_id(self.vision_main_id))
        else:
            QMessageBox.information(self, UI.DELETE, UI.CONFIRM_CHOOSE_VISION_MESSAGE)

    @pyqtSlot(int)
    def delete_vision_table(self, id):
        self._database.delete_vision_main(id)

    @pyqtSlot(str)
    def filter_list(self, text):
        self.visionViewModel.filter_by_title(text)

    def show_vision_detail(self, id):
        if id != self.vision_main_id:
            self.vision_main_id = id
            self.view.clear_all()
            self.view.reset_search_bar()
            vision_detail_list = self._database.get_all_vision_details_list(id)
            for vision_detail in vision_detail_list:
                if vision_detail['vision_type'] == ChatType.HUMAN.value:
                    vision_detail_id = f"{Constants.VISION_DETAIL_TABLE_ID_NAME}{id}_{vision_detail['id']}"
                    vision_detail_file_list = self._database.get_all_vision_details_file_list(vision_detail_id)
                    file_list = []
                    for vision_detail_file in vision_detail_file_list:
                        file_list.append(Utility.create_temp_file(vision_detail_file['vision_detail_file_data'],
                                                                  Constants.VISION_IMAGE_EXTENSION, True))

                    self.view.add_user_question(ChatType.HUMAN, vision_detail['vision_text'], file_list)
                else:
                    self.view.add_ai_answer(ChatType.AI, vision_detail['vision_text'],
                                            Constants.MODEL_PREFIX + vision_detail['vision_model'])
                    self.view.get_last_ai_widget().set_model_name(
                        Constants.MODEL_PREFIX + vision_detail['vision_model']
                        + Constants.RESPONSE_TIME + format(float(vision_detail['elapsed_time']), ".2f"))

    def delete_vision(self, index):
        self.visionViewModel.remove_vision(index)

    def create_new_vision(self, title=Constants.NEW_VISION):
        self.visionViewModel.add_new_vision(title)

    def add_human_vision(self, text, file_list):
        if self.vision_main_id:
            vision_detail_id = self._database.insert_vision_detail(self.vision_main_id, ChatType.HUMAN.value,
                                                                   self.visionView.vision_model, text, None, None)
            if vision_detail_id:
                for file in file_list:
                    self._database.insert_vision_file(vision_detail_id, Utility.base64_encode_file(file))
        else:
            self.create_new_vision()
            vision_detail_id = self._database.insert_vision_detail(self.vision_main_id, ChatType.HUMAN.value,
                                                                   self.visionView.vision_model, text, None, None)
            if vision_detail_id:
                for file in file_list:
                    self._database.insert_vision_file(vision_detail_id, Utility.base64_encode_file(file))

    @pyqtSlot(str, str, float)
    def handle_file_index_finished_signal(self, model, finish_reason, elapsed_time):
        self.colpali_rag_ready = True
        QMessageBox.information(self, "File Indexing Finished", "Enter your prompt")

    @pyqtSlot(object)
    def indexing_file(self, args):
        self.colpaliVLMModel.indexing_files(args)

    @pyqtSlot(str)
    def submit(self, text):
        if text and text.strip() and self.colpali_rag_ready:
            file_list = self.colpaliVLMModel.get_colpali_search_result(
                text, self.view.get_k_nearest(self.llm), self.view.get_image_size(self.llm))

            self.add_human_vision(text, file_list)
            self.visionView.update_ui_submit(ChatType.HUMAN, text, file_list)
            self.visionModel.send_user_input(self.visionView.create_args(text, self.llm, file_list), self.llm)
        else:
            QMessageBox.warning(self, "File Indexing", "Run 'File Indexing' first")
