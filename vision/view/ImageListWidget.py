import re
from shutil import copy2

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QFileDialog, \
    QMessageBox

from util.ChatType import ChatType
from util.Constants import UI
from util.Utility import Utility
from vision.view.ThumbnailListWidget import ThumbnailListWidget


class ImageListWidget(QWidget):
    def __init__(self, chat_type: ChatType, text: str = None, file_list: list = None):
        super().__init__()
        self.chat_type = chat_type
        self.text_result = text

        self.user_text = QLabel(text)
        self.format_text_label()
        self.file_list = file_list
        self.initialize_ui()

    def initialize_ui(self):
        layout = QVBoxLayout(self)
        self._thumbnail_list = ThumbnailListWidget()
        for file_path in self.file_list:
            self._thumbnail_list.add_thumbnail(Utility.base64_encode_file(file_path))

        top_widget = self.create_top_widget()
        layout.addWidget(top_widget)
        layout.addWidget(self.thumbnail_list)
        layout.addWidget(self.user_text)

    @property
    def thumbnail_list(self):
        return self._thumbnail_list

    def format_text_label(self):
        self.user_text.setTextFormat(Qt.TextFormat.MarkdownText)
        self.user_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.user_text.setWordWrap(True)
        self.user_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.user_text.setOpenExternalLinks(True)

        padding = Utility.get_settings_value(section="Common_Label_Style", prop="padding",
                                             default="5px",
                                             save=True)
        color = Utility.get_settings_value(section="Common_Label_Style", prop="color",
                                           default="#000000",
                                           save=True)
        font_size = Utility.get_settings_value(section="Common_Label_Style", prop="font-size",
                                               default="14px",
                                               save=True)
        font_family = Utility.get_settings_value(section="Common_Label_Style", prop="font-family",
                                                 default="sans-serif",
                                                 save=True)
        user_text_style = f"""
            QLabel {{
                padding: {padding};
                color: {color};
                font-size: {font_size};
                font-family: {font_family};
            }}
            """
        self.user_text.setStyleSheet(user_text_style)

    def create_top_widget(self):

        boldFont = QFont()
        boldFont.setBold(True)

        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        human_titlebar_background_color = Utility.get_settings_value(section="Chat_TitleBar_Style", prop="human_color",
                                                                     default="#dfccff",
                                                                     save=True)
        ai_titlebar_background_color = Utility.get_settings_value(section="Chat_TitleBar_Style", prop="ai_color",
                                                                  default="#d8fabe",
                                                                  save=True)

        if self.chat_type != ChatType.HUMAN:
            top_widget.setStyleSheet(f"background-color: {ai_titlebar_background_color}")
        else:
            top_widget.setStyleSheet(f"background-color: {human_titlebar_background_color}")

        padding = Utility.get_settings_value(section="Common_Label_Style", prop="padding",
                                             default="5px",
                                             save=True)

        model_color = Utility.get_settings_value(section="Info_Label_Style", prop="model-color",
                                                 default="green",
                                                 save=True)

        self.model_label = QLabel("")
        self.model_label.setFont(boldFont)

        model_label_style = f"""
                    QLabel {{
                        padding: {padding};
                        color: {model_color};
                    }}
                    """

        self.model_label.setStyleSheet(model_label_style)
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create Buttons
        copy_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'card--plus.png')), UI.COPY_TEXT)
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(self.get_original_text()))

        # Save Button
        save_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'disk--plus.png')), UI.SAVE_IMAGES)
        save_button.clicked.connect(self.save_image)

        # Create layouts for label and buttons
        model_label_layout = QHBoxLayout()
        model_label_layout.addWidget(self.model_label)
        model_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(save_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add both layouts to the top layout
        top_layout.addLayout(model_label_layout)
        top_layout.addLayout(button_layout)

        return top_widget

    def highlight_search_text(self, target_text, search_text):
        color = Utility.get_settings_value(section="AI_Code_Style", prop="color",
                                           default="#ccc",
                                           save=True)
        background_color = Utility.get_settings_value(section="AI_Code_Style", prop="background-color",
                                                      default="#333333",
                                                      save=True)

        search_text_escaped = re.escape(search_text)
        search_pattern = re.compile(search_text_escaped, re.IGNORECASE)

        matches = search_pattern.findall(target_text)
        for match in matches:
            formatted_code = f'<span style="color: {color}; background-color: {background_color};">{match}</span>'
            target_text = target_text.replace(match, formatted_code)

        return target_text

    def get_chat_type(self):
        return self.chat_type

    def apply_highlight(self, text: str):
        self.user_text.setText(text)

    def get_original_text(self):
        return self.text_result

    def show_original_text(self):
        self.user_text.setText(self.get_original_text())

    def save_image(self):
        dest_dir = QFileDialog.getExistingDirectory(self, UI.SELECT_FOLDER)
        if dest_dir:
            try:
                for file_path in self.file_list:
                    copy2(file_path, dest_dir)
                QMessageBox.information(self, UI.SUCCESS, UI.FILE_COPY_SUCCESS)
            except Exception as e:
                QMessageBox.critical(self, UI.ERROR, f"{UI.FILE_COPY_ERROR} {str(e)}")