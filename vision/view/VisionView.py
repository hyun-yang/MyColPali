from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QScrollArea, QSplitter, \
    QTabWidget, QGroupBox, QFormLayout, QLabel, QComboBox, QCheckBox, QFileDialog, QListWidget, QMessageBox, \
    QLineEdit, QSpinBox

from custom.CheckComboBox import CheckComboBox
from custom.CheckDoubleSpinBox import CheckDoubleSpinBox
from custom.CheckSpinBox import CheckSpinBox
from custom.PromptTextEdit import PromptTextEdit
from util.ChatType import ChatType
from util.Constants import AIProviderName, Constants, UI
from util.SettingsManager import SettingsManager
from util.Utility import Utility
from vision.view.ChatWidget import ChatWidget
from vision.view.ImageListWidget import ImageListWidget
from vision.view.VisionHistory import VisionHistory


class VisionView(QWidget):
    submitted_file_signal = pyqtSignal(object)
    submitted_prompt_signal = pyqtSignal(str)
    stop_signal = pyqtSignal()
    current_llm_signal = pyqtSignal(str)
    reload_chat_detail_signal = pyqtSignal(int)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self._settings = SettingsManager.get_settings()
        self._current_llm = Utility.get_settings_value(section="AI_Provider", prop="llm",
                                                       default="OpenAI", save=True)

        self.found_text_positions = []

        self.initialize_ui()

    def initialize_ui(self):
        # Top layout
        self.top_layout = QVBoxLayout()
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.clear_all_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'bin.png')), UI.CLEAR_ALL)
        self.clear_all_button.clicked.connect(lambda: self.clear_all())

        self.reload_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'arrow-circle.png')), UI.RELOAD_ALL)
        self.reload_button.clicked.connect(lambda: self.reload_chat_detail_signal.emit(-1))

        self.search_text = PromptTextEdit()
        self.search_text.submitted_signal.connect(self.search)
        self.search_text.setPlaceholderText(UI.SEARCH_PROMPT_PLACEHOLDER)

        self.search_text.setFixedHeight(self.clear_all_button.sizeHint().height())
        self.search_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.search_result = QLabel()

        # Create navigation buttons
        self.prev_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'arrow-180.png')), '')
        self.prev_button.clicked.connect(self.scroll_to_previous_match_widget)
        self.next_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'arrow.png')), '')
        self.next_button.clicked.connect(self.scroll_to_next_match_widget)

        # Create a horizontal layout and add the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_text)
        button_layout.addWidget(self.search_result)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.clear_all_button)
        button_layout.addWidget(self.reload_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add the button layout to the result layout
        self.top_layout.addLayout(button_layout)

        self.top_widget = QWidget()
        self.top_widget.setLayout(self.top_layout)
        self.top_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Result View
        self.result_layout = QVBoxLayout()
        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.result_layout.setSpacing(0)
        self.result_layout.setContentsMargins(0, 0, 0, 0)

        self.result_widget = QWidget()
        self.result_widget.setLayout(self.result_layout)

        # Scroll Area
        self.ai_answer_scroll_area = QScrollArea()
        self.ai_answer_scroll_area.setWidgetResizable(True)
        self.ai_answer_scroll_area.setWidget(self.result_widget)

        # Stop Button
        self.stop_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'minus-circle.png')), UI.STOP)
        self.stop_button.clicked.connect(self.force_stop)

        stop_layout = QHBoxLayout()
        stop_layout.setContentsMargins(0, 0, 0, 0)
        stop_layout.setSpacing(0)
        stop_layout.addWidget(self.stop_button)
        stop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stop_widget = QWidget()
        self.stop_widget.setLayout(stop_layout)
        self.stop_widget.setVisible(False)

        # Prompt View
        self.prompt_text = PromptTextEdit()
        self.prompt_text.setPlaceholderText(UI.CHAT_PROMPT_PLACEHOLDER)
        self.prompt_text.submitted_signal.connect(self.handle_submitted_prompt_signal)

        prompt_layout = QVBoxLayout()
        prompt_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        prompt_layout.addWidget(self.prompt_text)
        prompt_layout.setSpacing(0)
        prompt_layout.setContentsMargins(0, 0, 0, 0)

        self.prompt_widget = QWidget()
        self.prompt_widget.setLayout(prompt_layout)
        self.prompt_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        chat_layout = QVBoxLayout()

        chat_layout.addWidget(self.top_widget)
        chat_layout.addWidget(self.ai_answer_scroll_area)
        chat_layout.addWidget(self.stop_widget)
        chat_layout.addWidget(self.prompt_widget)

        chatWidget = QWidget()
        chatWidget.setLayout(chat_layout)

        config_layout = QVBoxLayout()

        self.config_tabs = QTabWidget()
        vision_icon = QIcon(Utility.get_icon_path('ico', 'picture--pencil.png'))
        self.config_tabs.addTab(self.create_parameters_tab(), vision_icon, UI.COLPALI)
        self.config_tabs.addTab(self.create_visiondb_tab(), vision_icon, UI.COLPALI_LIST)

        config_layout.addWidget(self.config_tabs)

        configWidget = QWidget()
        configWidget.setLayout(config_layout)

        mainWidget = QSplitter(Qt.Orientation.Horizontal)
        mainWidget.addWidget(configWidget)
        mainWidget.addWidget(chatWidget)
        mainWidget.setSizes([UI.QSPLITTER_LEFT_WIDTH, UI.QSPLITTER_RIGHT_WIDTH])
        mainWidget.setHandleWidth(UI.QSPLITTER_HANDLEWIDTH)

        main_layout = QVBoxLayout()
        main_layout.addWidget(mainWidget)

        self.setLayout(main_layout)

    def reset_search_bar(self):
        self.found_text_positions = []
        self.search_result.clear()
        self.current_position_index = -1
        self.update_navigation_buttons()

    def search(self, text: str):
        if text and text.strip() and len(text) >= 2:
            self.found_text_positions = []
            self.current_position_index = -1

            search_text_lower = text.lower()

            for i in range(self.result_layout.count()):
                current_widget = self.result_layout.itemAt(i).widget()
                current_text = current_widget.get_original_text()
                current_text_lower = current_text.lower()

                if search_text_lower in current_text_lower:
                    self.found_text_positions.append(i)
                    highlight_text = current_widget.highlight_search_text(current_text, text)
                    current_widget.apply_highlight(highlight_text)
                else:
                    current_widget.show_original_text()

            if self.found_text_positions:
                self.current_position_index = 0
                self.scroll_to_match_widget(self.found_text_positions[self.current_position_index])
        if len(self.found_text_positions) > 0:
            self.search_result.setText(f'{len(self.found_text_positions)} {UI.FOUNDS}')
        else:
            self.search_result.clear()
        self.update_navigation_buttons()
        self.search_text.clear()

    def scroll_to_match_widget(self, position):
        self.ai_answer_scroll_area.ensureWidgetVisible(self.result_layout.itemAt(position).widget())

    def scroll_to_previous_match_widget(self):
        if len(self.found_text_positions) > 0 and self.current_position_index > 0:
            self.current_position_index -= 1
            self.scroll_to_match_widget(self.found_text_positions[self.current_position_index])
            self.update_navigation_buttons()

    def scroll_to_next_match_widget(self):
        if len(self.found_text_positions) > 0 and self.current_position_index < len(self.found_text_positions) - 1:
            self.current_position_index += 1
            self.scroll_to_match_widget(self.found_text_positions[self.current_position_index])
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.prev_button.setEnabled(self.current_position_index > 0)
        self.next_button.setEnabled(self.current_position_index < len(self.found_text_positions) - 1)

    def adjust_scroll_bar(self, min_val, max_val):
        self.ai_answer_scroll_area.verticalScrollBar().setSliderPosition(max_val)

    def create_visiondb_tab(self):
        layoutWidget = QWidget()
        layout = QVBoxLayout()

        self._vision_history = VisionHistory(self.model)

        layout.addWidget(self._vision_history)

        layoutWidget.setLayout(layout)
        return layoutWidget

    def create_parameters_tab(self):
        layoutWidget = QWidget()
        layout = QVBoxLayout()

        # Tabs for LLM
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_openai_tabcontent(AIProviderName.OPENAI.value), UI.COLPALI)
        self.tabs.currentChanged.connect(self.on_tab_change)
        layout.addWidget(self.tabs)

        layoutWidget.setLayout(layout)
        return layoutWidget

    def on_tab_change(self, index):
        self._current_llm = self.tabs.tabText(index)
        self._settings.setValue('AI_Provider/llm', self._current_llm)
        self.current_llm_signal.emit(self._current_llm)

    def create_openai_tabcontent(self, name):
        tabWidget = QWidget()
        tabWidget.setObjectName(name)
        layoutMain = QVBoxLayout()

        groupColPaliName = QGroupBox(f"{UI.COLPALI} Setting")
        colpaliLayout = QFormLayout()
        colpaliChatLabel = QLabel("ColPali Index Name")
        self.colpaliChatName = QLineEdit()
        self.colpaliChatName.setObjectName("ColPaliChatName")
        self.colpaliChatName.setPlaceholderText("ColPali Index Name")
        colpaliLayout.addRow(colpaliChatLabel)
        colpaliLayout.addRow(self.colpaliChatName)

        Utility.get_settings_value(section=f"{name}_ColPali_Parameter", prop="model_name",
                                   default="vidore/colpali-v1.2", save=True)

        overwriteCheckbox = QCheckBox()
        overwriteCheckbox.setObjectName(f"{name}_overwriteCheckbox")
        overwriteCheckbox.setChecked(
            (Utility.get_settings_value(section=f"{name}_ColPali_Parameter", prop="overwrite", default="True",
                                        save=True)) == "True")
        overwriteCheckbox.toggled.connect(lambda value: self.overwrite_changed(value, name))
        overwriteCheckbox.setChecked(True)
        overwriteCheckbox.setEnabled(False)
        colpaliLayout.addRow('Overwrite', overwriteCheckbox)

        storeCollectionWithIndexCheckbox = QCheckBox()
        storeCollectionWithIndexCheckbox.setObjectName(f"{name}_storeCollectionWithIndexCheckbox")
        storeCollectionWithIndexCheckbox.setChecked(
            (Utility.get_settings_value(section=f"{name}_ColPali_Parameter", prop="store_collection", default="True",
                                        save=True)) == "True")
        storeCollectionWithIndexCheckbox.toggled.connect(lambda value: self.store_collection_with_index_changed(value, name))
        storeCollectionWithIndexCheckbox.setChecked(True)
        storeCollectionWithIndexCheckbox.setEnabled(False)
        colpaliLayout.addRow('Store Collection With Index', storeCollectionWithIndexCheckbox)

        kNearestSpinBox = QSpinBox()
        kNearestSpinBox.setObjectName(f"{name}_kNearestSpinBox")
        kNearestSpinBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        kNearestSpinBox.setRange(1, 100)
        kNearestSpinBox.setAccelerated(True)
        kNearestSpinBox.setSingleStep(1)
        kNearestSpinBox.setValue(
            int(Utility.get_settings_value(section=f"{name}_ColPali_Parameter", prop="k_nearest", default="3",
                                           save=True)))
        kNearestSpinBox.valueChanged.connect(lambda value: self.k_nearest_changed(value, name))
        colpaliLayout.addRow('Image Result', kNearestSpinBox)

        sizeComboBox = CheckComboBox()
        sizeComboBox.setObjectName(f"{name}_sizeComboBox")
        sizeComboBox.combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizeComboBox.combo_box.addItems(Constants.VISION_SIZE_LIST)
        sizeComboBox.combo_box.setCurrentText(
            Utility.get_settings_value(section=f"{name}_ColPali_Parameter", prop="size",
                                       default="1024", save=True)
        )
        sizeComboBox.currentTextChanged.connect(lambda value: self.size_changed(value, name))
        colpaliLayout.addRow('Image Size', sizeComboBox)

        groupColPaliName.setLayout(colpaliLayout)
        layoutMain.addWidget(groupColPaliName)

        # file list
        # Document List Group
        documentListGroup = QGroupBox(f"{UI.COLPALI} Data Source - PDF File")
        documentListLayout = QVBoxLayout()
        documentListGroup.setLayout(documentListLayout)

        # Add QListWidget to show selected file list
        fileListWidget = QListWidget()
        fileListWidget.setObjectName(f"{name}_FileList")
        documentListLayout.addWidget(fileListWidget)

        # Add buttons
        buttonLayout = QHBoxLayout()
        selectButton = QPushButton(QIcon(Utility.get_icon_path('ico', 'document-pdf.png')), "File")
        selectButton.setObjectName(f"{name}_SelectButton")

        deleteButton = QPushButton(QIcon(Utility.get_icon_path('ico', 'folder--minus.png')), "Remove")
        deleteButton.setObjectName(f"{name}_DeleteButton")
        deleteButton.setEnabled(False)

        buttonLayout.addWidget(selectButton)
        buttonLayout.addWidget(deleteButton)

        documentListLayout.addLayout(buttonLayout)

        submitLayout = QHBoxLayout()
        submitButton = QPushButton(QIcon(Utility.get_icon_path('ico', 'inbox-document-text.png')), "File Indexing")
        submitButton.setObjectName(f"{name}_SubmitButton")
        submitButton.setEnabled(False)
        submitLayout.addWidget(submitButton)

        documentListLayout.addLayout(submitLayout)

        selectButton.clicked.connect(partial(self.select_files, name))
        deleteButton.clicked.connect(partial(self.delete_file, name))
        submitButton.clicked.connect(partial(self.submit_file, name))

        fileListWidget.itemSelectionChanged.connect(partial(self.on_item_selection_changed, name))

        layoutMain.addWidget(documentListGroup)

        groupModel = QGroupBox(f"{name} Model")
        modelLayout = QFormLayout()
        modelLabel = QLabel(f"{name} Model List")
        modelList = QComboBox()
        modelList.setObjectName(f"{name}_ModelList")
        modelList.clear()

        self.set_model_list(modelList, name)

        modelLayout.addRow(modelLabel)
        modelLayout.addRow(modelList)
        groupModel.setLayout(modelLayout)
        layoutMain.addWidget(groupModel)

        # Parameters Group
        groupParam = QGroupBox(f"{name} Parameters")
        paramLayout = QFormLayout()

        max_tokensSpinBox = CheckSpinBox()
        max_tokensSpinBox.setObjectName(f"{name}_max_tokensSpinBox")
        max_tokensSpinBox.spin_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        max_tokensSpinBox.spin_box.setRange(0, 128000)
        max_tokensSpinBox.spin_box.setAccelerated(True)
        max_tokensSpinBox.spin_box.setSingleStep(1)
        max_tokensSpinBox.spin_box.setValue(
            int(
                Utility.get_settings_value(section=f"{name}_Vision_Parameter", prop="max_tokens",
                                           default="2048", save=True)))
        max_tokensSpinBox.check_box.setEnabled(True)
        max_tokensSpinBox.valueChanged.connect(lambda value: self.maxtokens_changed(value, name))
        paramLayout.addRow('Max Tokens', max_tokensSpinBox)

        temperatureSpinBox = CheckDoubleSpinBox()
        temperatureSpinBox.setObjectName(f"{name}_temperatureSpinBox")
        temperatureSpinBox.spin_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        temperatureSpinBox.spin_box.setRange(0, 2)
        temperatureSpinBox.spin_box.setAccelerated(True)
        temperatureSpinBox.spin_box.setSingleStep(0.1)
        temperatureSpinBox.spin_box.setValue(
            float(Utility.get_settings_value(section=f"{name}_Vision_Parameter", prop="temperature", default="0.2",
                                             save=True)))
        temperatureSpinBox.valueChanged.connect(lambda value: self.temperature_changed(value, name))
        paramLayout.addRow('Temperature', temperatureSpinBox)

        groupParam.setLayout(paramLayout)
        layoutMain.addWidget(groupParam)

        optionGroup = QGroupBox(f"{name} Options")
        optionLayout = QVBoxLayout()

        streamCheckbox = QCheckBox("Stream")
        streamCheckbox.setObjectName(f"{name}_streamCheckbox")
        streamCheckbox.setChecked(
            (Utility.get_settings_value(section=f"{name}_Vision_Parameter", prop="stream", default="True",
                                        save=True)) == "True")
        streamCheckbox.toggled.connect(lambda value: self.stream_changed(value, name))
        optionLayout.addWidget(streamCheckbox)
        optionGroup.setLayout(optionLayout)
        layoutMain.addWidget(optionGroup)

        tabWidget.setLayout(layoutMain)

        return tabWidget

    def select_files(self, llm):
        fileListWidget = self.findChild(QListWidget, f"{llm}_FileList")
        selected_files = self.show_file_dialog(llm)
        for file in selected_files:
            fileListWidget.addItem(file)
        self.update_submit_status(llm)

    def delete_file(self, llm):
        fileListWidget = self.findChild(QListWidget, f"{llm}_FileList")
        for item in fileListWidget.selectedItems():
            fileListWidget.takeItem(fileListWidget.row(item))
        self.update_submit_status(llm)

    def update_submit_status(self, llm):
        fileListWidget = self.findChild(QListWidget,
                                        f"{llm}_FileList")
        submitButton = self.findChild(QPushButton,
                                      f"{llm}_SubmitButton")
        submitButton.setEnabled(bool(fileListWidget.count()))

    def on_item_selection_changed(self, llm):
        fileListWidget = self.findChild(QListWidget,
                                        f"{llm}_FileList")
        deleteButton = self.findChild(QPushButton,
                                      f"{llm}_DeleteButton")
        deleteButton.setEnabled(bool(fileListWidget.selectedItems()))

        submitButton = self.findChild(QPushButton,
                                      f"{llm}_SubmitButton")
        submitButton.setEnabled(bool(fileListWidget.count()))

    def show_file_dialog(self, llm=None):
        file_filter = UI.PDF_FILTER

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(file_filter)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            return selected_files
        else:
            return [] if llm != AIProviderName.GEMINI.value else None

    def get_selected_file(self, llm):
        fileListWidget = self.findChild(QListWidget, f"{llm}_FileList")
        return fileListWidget.item(0).text()

    def create_args(self, text, llm, file_list):
        method_name = f'create_args_{llm.lower()}'
        method = getattr(self, method_name, None)
        if callable(method):
            return method(text, llm, file_list)
        else:
            raise ValueError(f'{UI.METHOD} {method_name} {UI.NOT_FOUND}')

    def create_colpali_args(self, llm):

        model_name = Utility.get_settings_value(section=f"{llm}_ColPali_Parameter", prop="model_name",
                                                default="vidore/colpali-v1.2", save=True)

        store_collection_with_index = self.findChild(QCheckBox,
                                                     f'{llm}_storeCollectionWithIndexCheckbox').isChecked()

        overwrite = self.findChild(QCheckBox,
                                   f'{llm}_overwriteCheckbox').isChecked()
        verbose = 1

        args = {
            'model_name': model_name,
            'verbose': verbose,
            'store_collection_with_index': store_collection_with_index,
            'overwrite': overwrite,
        }
        return args

    def create_args_openai(self, text, llm, file_list):
        api_key = self._settings.value(f'AI_Provider/{llm}')
        model = self.findChild(QComboBox, f'{llm}_ModelList').currentText()

        max_tokens_spin_box = self.findChild(CheckSpinBox,
                                             f'{llm}_max_tokensSpinBox').spin_box
        max_tokens = max_tokens_spin_box.value() if max_tokens_spin_box.isEnabled() else None

        temperature_spin_box = self.findChild(CheckDoubleSpinBox,
                                              f'{llm}_temperatureSpinBox').spin_box
        temperature = temperature_spin_box.value() if temperature_spin_box.isEnabled() else None

        stream = self.findChild(QCheckBox,
                                f'{llm}_streamCheckbox').isChecked()
        detail = 'auto'

        content = []
        if file_list:
            for file in file_list:
                content.append(
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{Utility.base64_encode_file(file)}',
                            'detail': detail
                        }
                    }
                )
        content.append({
            'type': 'text',
            'text': text
        })

        messages = [
            {"role": "user", "content": content}
        ]

        ai_arg = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'stream': stream,
        }

        args = {
            'api_key': api_key,
            'ai_arg': ai_arg,
        }

        return args

    def set_model_list(self, modelList, name):
        modelList.addItems(Constants.VISION_MODEL_LIST)
        current_model = Utility.get_settings_value(section=f"{name}_Vision_Parameter", prop="vision_model",
                                                   default="gpt-4o", save=True)
        modelList.setCurrentText(current_model)
        modelList.currentTextChanged.connect(lambda current_text: self.model_list_changed(current_text, name))

    def model_list_changed(self, model, llm):
        self._settings.setValue(f"{llm}_Vision_Parameter/vision_model", model)

    def submit_file(self, llm):
        args = self.create_colpali_args(llm)
        input_file_path = self.get_selected_file(llm)
        args['input_file_path'] = input_file_path

        colpali_index_name = self.colpaliChatName.text()
        if not colpali_index_name:
            self.show_warning(UI.WARNING_COLPALI_INDEX_NAME)
            return

        args['index_name'] = colpali_index_name

        if not self.validate_input(input_file_path):
            return
        if input_file_path:
            self.submitted_file_signal.emit(args)

    def validate_input(self, file_list):
        if not file_list:
            self.show_warning(UI.WARNING_TITLE_SELECT_FILE_MESSAGE)
            return False
        return True

    def show_warning(self, message):
        QMessageBox.warning(self, UI.WARNING_TITLE, message)

    def handle_submitted_prompt_signal(self, text):
        self.submitted_prompt_signal.emit(text)

    def add_user_question(self, chatType, text, file_list):
        user_question = ImageListWidget(chatType, text, file_list)
        self.result_layout.addWidget(user_question)

    def add_ai_answer(self, chatType, text, model):
        ai_answer = ChatWidget.with_model(chatType, text, model)
        self.result_layout.addWidget(ai_answer)

    def update_ui_submit(self, chatType, text, file_list):
        self.ai_answer_scroll_area.verticalScrollBar().rangeChanged.connect(self.adjust_scroll_bar)
        self.add_user_question(chatType, text, file_list)
        self.stop_widget.setVisible(True)

    def update_ui(self, result, stream):
        if stream:
            chatWidget = self.get_last_ai_widget()

            if chatWidget:
                chatWidget.add_text(result)
            else:
                chatWidget = ChatWidget(ChatType.AI)
                chatWidget.add_text(result)
                self.result_layout.addWidget(chatWidget)

        else:
            ai_answer = ChatWidget(ChatType.AI, result)
            self.result_layout.addWidget(ai_answer)

    def update_ui_finish(self, model, finish_reason, elapsed_time, stream):
        self.ai_answer_scroll_area.verticalScrollBar().rangeChanged.disconnect()

        chatWidget = self.get_last_ai_widget()
        if stream:
            if chatWidget:
                chatWidget.apply_style()
                self.stop_widget.setVisible(False)
        else:
            self.stop_widget.setVisible(False)

        if chatWidget and chatWidget.get_chat_type() == ChatType.AI:
            chatWidget.set_model_name(
                Constants.MODEL_PREFIX + model + Constants.RESPONSE_TIME + format(elapsed_time, ".2f"))

    def set_default_tab(self, name):
        index = self.tabs.indexOf(self.tabs.findChild(QWidget, name))
        if index != -1:
            self.tabs.setCurrentIndex(index)

    def get_last_ai_widget(self) -> ChatWidget | None:
        layout_item = self.result_widget.layout().itemAt(self.result_widget.layout().count() - 1)
        if layout_item:
            last_ai_widget = layout_item.widget()
            if last_ai_widget.get_chat_type() == ChatType.AI:
                return last_ai_widget
        else:
            return None

    def k_nearest_changed(self, value, name):
        self._settings.setValue(f"{name}_ColPali_Parameter/k_nearest", value)

    def size_changed(self, value, name):
        self._settings.setValue(f"{name}_ColPali_Parameter/size", value)

    def maxtokens_changed(self, value, name):
        self._settings.setValue(f"{name}_Vision_Parameter/max_tokens", value)

    def temperature_changed(self, value, name):
        self._settings.setValue(f"{name}_Vision_Parameter/temperature", value)

    def store_collection_with_index_changed(self, checked, name):
        if checked:
            self._settings.setValue(f"{name}_ColPali_Parameter/store_collection_with_index", 'True')
        else:
            self._settings.setValue(f"{name}_ColPali_Parameter/store_collection_with_index", 'False')

    def overwrite_changed(self, checked, name):
        if checked:
            self._settings.setValue(f"{name}_ColPali_Parameter/overwrite", 'True')
        else:
            self._settings.setValue(f"{name}_ColPali_Parameter/overwrite", 'False')

    def stream_changed(self, checked, name):
        if checked:
            self._settings.setValue(f"{name}_Vision_Parameter/stream", 'True')
        else:
            self._settings.setValue(f"{name}_Vision_Parameter/stream", 'False')

    def start_chat(self):
        self.prompt_text.clear()
        self.prompt_text.setEnabled(False)

    def finish_chat(self):
        self.prompt_text.setEnabled(True)
        self.prompt_text.setFocus()

        submitButton = self.findChild(QPushButton, f"{self._current_llm}_SubmitButton")
        submitButton.setEnabled(False)

    def force_stop(self):
        self.stop_signal.emit()
        self.stop_widget.setVisible(False)

    def clear_all(self):
        target_layout = self.result_layout
        if target_layout is not None:
            while target_layout.count():
                item = target_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def get_image_size(self, llm):
        sizeComboBox = self.findChild(CheckComboBox,
                                      f'{llm}_sizeComboBox').combo_box
        image_size = sizeComboBox.currentText() if sizeComboBox.isEnabled() else 0
        return int(image_size)

    def get_k_nearest(self, llm):
        k_nearest_spin_box = self.findChild(QSpinBox, f"{llm}_kNearestSpinBox")
        return k_nearest_spin_box.value()

    @property
    def vision_history(self):
        return self._vision_history

    @property
    def vision_model(self):
        return self.findChild(QComboBox, f'{self._current_llm}_ModelList').currentText()
