from functools import partial

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QGridLayout, QColorDialog, QFontDialog, QMessageBox, QHBoxLayout

from util.Constants import get_ai_provider_names, UI
from util.SettingsManager import SettingsManager
from util.Utility import Utility


class GlobalSetting(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(UI.SETTINGS)
        self._settings = SettingsManager.get_settings()

        mainLayout = QVBoxLayout(self)

        row1Layout = QHBoxLayout()
        row2Layout = QHBoxLayout()

        mainLayout.addLayout(row1Layout)
        mainLayout.addLayout(row2Layout)

        self.create_ai_provider_group(row1Layout)
        self.create_chat_title_bar_style_group(row1Layout)
        self.create_common_label_style_group(row1Layout)
        self.create_ai_code_view_style_group(row2Layout)
        self.create_info_label_style_group(row2Layout)

    def create_info_label_style_group(self, layout):
        info_label_window_group = QGroupBox('Info Label Style')
        info_label_window_layout = QGridLayout()
        color_types = ["Model", "Elapsed Time", "Finish Reason"]

        self.info_labels = [f"{color_type} Color" for color_type in color_types]
        self.info_keys = ['model-color', 'elapsedtime-color', 'finishreason-color']
        self.info_color_editors = [QLineEdit() for _ in self.info_labels]
        self.info_buttons = [QPushButton('...') for _ in self.info_labels]

        for i in range(len(self.info_color_editors)):
            self.info_color_editors[i].textChanged.connect(partial(self.handle_info_label_text_change, i))

        for i, button in enumerate(self.info_buttons):
            button.setMaximumWidth(30)
            button.clicked.connect(partial(self.color_pick, color_types[i], self.info_color_editors[i]))

        for i, label in enumerate(self.info_labels):
            info_label_window_layout.addWidget(QLabel(label), i, 0)
            info_label_window_layout.addWidget(self.info_color_editors[i], i, 1)
            info_label_window_layout.addWidget(self.info_buttons[i], i, 2)

            info_key = self._settings.value(f'Info_Label_Style/{self.info_keys[i]}')
            if info_key:
                self.info_color_editors[i].setText(info_key)

        info_label_window_group.setLayout(info_label_window_layout)
        layout.addWidget(info_label_window_group)

    def handle_info_label_text_change(self, index, text):
        self._settings.setValue(f'Info_Label_Style/{self.info_keys[index]}', text)

    def create_ai_code_view_style_group(self, mainLayout):
        ai_code_view_group = QGroupBox('AI Code-View Style')
        ai_code_view_layout = QGridLayout()
        self.ai_labels = ['Color', 'Background Color', 'Font-Family', 'Font-Size']
        self.ai_keys = ['color', 'background-color', 'font-family', 'font-size']
        self.ai_values = [self._settings.value(f'AI_Code_Style/{self.ai_keys[i]}', '') for i in
                          range(len(self.ai_keys))]

        self.ai_editors = [QLineEdit(self.ai_values[i]) for i in range(len(self.ai_labels))]
        self.ai_buttons = [QPushButton('...') if i != 3 else None for i in range(len(self.ai_labels))]

        for i in range(len(self.ai_editors)):
            self.ai_editors[i].textChanged.connect(partial(self.handle_ai_code_view_text_change, i))

        for i, button in enumerate(self.ai_buttons):
            if button is not None:
                button.setMaximumWidth(30)
                if i < 2:
                    button.clicked.connect(partial(self.ai_color_dialog, i))
                else:
                    button.clicked.connect(self.ai_font_dialog)

        for i, label in enumerate(self.ai_labels):
            ai_code_view_layout.addWidget(QLabel(label), i, 0)
            if self.ai_buttons[i] is not None:
                ai_code_view_layout.addWidget(self.ai_editors[i], i, 1)
                ai_code_view_layout.addWidget(self.ai_buttons[i], i, 2)
            else:
                ai_code_view_layout.addWidget(self.ai_editors[i], i, 1, 1, 2)

        ai_code_view_group.setLayout(ai_code_view_layout)
        mainLayout.addWidget(ai_code_view_group)

    def handle_ai_code_view_text_change(self, index, text):
        self._settings.setValue(f'AI_Code_Style/{self.ai_keys[index]}', text)

    def create_common_label_style_group(self, mainLayout):
        commonLabelStyleGroup = QGroupBox('Common Label Style')
        commonLabelStyleLayout = QGridLayout()
        self.commonLabelStyle_labels = ['Padding', 'Color', 'Font-Family', 'Font-Size']
        self.commonLabelStyle_keys = ['padding', 'color', 'font-family', 'font-size']
        self.commonLabelStyle_editors = [QLineEdit() if i != 1 else QLineEdit() for i in
                                         range(len(self.commonLabelStyle_labels))]
        self.commonLabelStyle_buttons = [QPushButton('...') if i != 0 and i != 3 else None for i in
                                         range(len(self.commonLabelStyle_labels))]

        for i in range(len(self.commonLabelStyle_editors)):
            self.commonLabelStyle_editors[i].textChanged.connect(partial(self.handle_common_label_text_change, i))

        for button in self.commonLabelStyle_buttons:
            if button is not None:
                button.setMaximumWidth(30)

        self.commonLabelStyle_buttons[1].clicked.connect(self.human_window_color)
        self.commonLabelStyle_buttons[2].clicked.connect(self.human_window_font)

        for i, label in enumerate(self.commonLabelStyle_labels):
            commonLabelStyleLayout.addWidget(QLabel(label), i, 0)
            if self.commonLabelStyle_buttons[i] is not None:
                commonLabelStyleLayout.addWidget(self.commonLabelStyle_editors[i], i, 1)
                commonLabelStyleLayout.addWidget(self.commonLabelStyle_buttons[i], i, 2)
            else:
                # span two columns for first QLineEdit
                commonLabelStyleLayout.addWidget(self.commonLabelStyle_editors[i], i, 1, 1, 2)

            human_key = self._settings.value(f'Common_Label_Style/{self.commonLabelStyle_keys[i]}')
            if human_key:
                self.commonLabelStyle_editors[i].setText(human_key)

        commonLabelStyleGroup.setLayout(commonLabelStyleLayout)
        mainLayout.addWidget(commonLabelStyleGroup)

    def handle_common_label_text_change(self, index, text):
        self._settings.setValue(f'Common_Label_Style/{self.commonLabelStyle_keys[index]}', text)

    def create_chat_title_bar_style_group(self, mainLayout):
        chat_title_window_group = QGroupBox('Chat TitleBar Style')
        chat_title_window_layout = QGridLayout()
        color_types = ["Human", "AI"]

        self.chat_labels = [f"{color_type} Color" for color_type in color_types]
        self.chat_keys = ['human_color', 'ai_color']
        self.chat_color_editors = [QLineEdit() for _ in self.chat_labels]
        self.chat_buttons = [QPushButton('...') for _ in self.chat_labels]

        for i in range(len(self.chat_color_editors)):
            self.chat_color_editors[i].textChanged.connect(partial(self.handle_chat_title_bar_text_change, i))

        for i, button in enumerate(self.chat_buttons):
            button.setMaximumWidth(30)
            button.clicked.connect(partial(self.color_pick, color_types[i], self.chat_color_editors[i]))

        for i, label in enumerate(self.chat_labels):
            chat_title_window_layout.addWidget(QLabel(label), i, 0)
            chat_title_window_layout.addWidget(self.chat_color_editors[i], i, 1)
            chat_title_window_layout.addWidget(self.chat_buttons[i], i, 2)

            chat_key = self._settings.value(f'Chat_TitleBar_Style/{self.chat_keys[i]}')
            if chat_key:
                self.chat_color_editors[i].setText(chat_key)

        chat_title_window_group.setLayout(chat_title_window_layout)
        mainLayout.addWidget(chat_title_window_group)

    def handle_chat_title_bar_text_change(self, index, text):
        self._settings.setValue(f'Chat_TitleBar_Style/{self.chat_keys[index]}', text)

    def create_ai_provider_group(self, mainLayout):
        LLM_group = QGroupBox('AI Provider')
        LLM_layout = QGridLayout()
        self.api_labels = ['OpenAI API']
        self.api_keys = get_ai_provider_names()
        self.api_key_editors = [QLineEdit() for _ in self.api_labels]
        self.api_buttons = [QPushButton('Check') for _ in self.api_labels]

        for i, label in enumerate(self.api_labels):
            LLM_layout.addWidget(QLabel(label), i, 0)
            LLM_layout.addWidget(self.api_key_editors[i], i, 1)

            button = self.api_buttons[i]
            if button:
                button.clicked.connect(partial(self.validate_api_key, self.api_keys[i]))
            LLM_layout.addWidget(button, i, 2)

            api_key = self._settings.value(f'AI_Provider/{self.api_keys[i]}')
            if api_key:
                self.api_key_editors[i].setText(api_key)

        LLM_group.setLayout(LLM_layout)
        mainLayout.addWidget(LLM_group)

    def validate_api_key(self, provider_name):
        editor_index = self.api_keys.index(provider_name)
        api_key = self.api_key_editors[editor_index].text()
        validation_method = getattr(Utility, f'check_{provider_name.lower()}_api_key')
        if validation_method(api_key):
            self._settings.setValue(f'AI_Provider/{provider_name}', api_key)
            QMessageBox.information(self, 'API Key Validation',
                                    'API key is valid, please restart the app for the changes to take effect',
                                    QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.critical(self, 'API Key Validation', 'Please check your API key.',
                                 QMessageBox.StandardButton.Ok)

    def ai_color_dialog(self, i):
        color = QColorDialog.getColor()
        if color.isValid():
            self.ai_editors[i].setText(color.name())

    def ai_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.ai_editors[2].setText(font.family())
            self.ai_editors[3].setText(str(font.pointSize()) + UI.SETTINGS_PIXEL)

    def human_window_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.commonLabelStyle_editors[1].setText(color.name())

    def human_window_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.commonLabelStyle_editors[2].setText(font.family())
            self.commonLabelStyle_editors[3].setText(str(font.pointSize()) + UI.SETTINGS_PIXEL)

    def color_pick(self, color_type, color_display):
        color = QColorDialog.getColor()
        if color.isValid():
            color_display.setText(color.name())

    def update_color_display(self, color_type, new_value):
        color_display_widget = self.info_color_editors[color_type]
        color_display_widget.setText(new_value)
