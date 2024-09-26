import html
import re

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication
)

from util import Utility
from util.SettingsManager import SettingsManager
from util.ChatType import ChatType
from util.Utility import Utility


class ChatWidget(QWidget):
    def __init__(self, chat_type: ChatType, text: str = None):
        super().__init__()
        self._settings = SettingsManager.get_settings()
        self.no_style = True
        self.text_result = []
        self.chat_type = chat_type
        self.user_text = QLabel(text)
        self.format_text_label()

        self.initialize_ui()
        self.set_text(text)

    @classmethod
    def with_model(cls, chat_type: ChatType, text: str, model: str):
        chat_widget_instance = cls(chat_type, text)
        chat_widget_instance.set_model_name(model)
        return chat_widget_instance

    def initialize_ui(self):
        layout = QVBoxLayout(self)
        top_widget = self.create_top_widget()
        layout.addWidget(top_widget)
        layout.addWidget(self.user_text)

    def format_text_label(self):
        if self.chat_type == ChatType.AI:
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

        copy_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'card--plus.png')), "")
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(self.get_original_text()))

        show_original_text_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'chat.svg')), "")
        show_original_text_button.clicked.connect(self.show_original_text)

        clear_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'erase.svg')), "")
        clear_button.clicked.connect(self.clear_text)

        # Create layouts for label and buttons
        model_label_layout = QHBoxLayout()
        model_label_layout.addWidget(self.model_label)
        model_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(show_original_text_button)
        button_layout.addWidget(clear_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add both layouts to the top layout
        top_layout.addLayout(model_label_layout)
        top_layout.addLayout(button_layout)

        return top_widget

    def set_text(self, text):
        self.text_result.append(text)
        if self.chat_type == ChatType.AI:
            formatted_text = self.format_code_snippet(text)
            self.user_text.setText(formatted_text)
        else:
            self.user_text.setText(text)

    def get_text(self):
        return self.user_text.text()

    def format_code_snippet(self, text):
        color = Utility.get_settings_value(section="AI_Code_Style", prop="color",
                                           default="#ccc",
                                           save=True)
        background_color = Utility.get_settings_value(section="AI_Code_Style", prop="background-color",
                                                      default="#333333",
                                                      save=True)
        font_size = Utility.get_settings_value(section="AI_Code_Style", prop="font-size",
                                               default="14px",
                                               save=True)
        font_family = Utility.get_settings_value(section="AI_Code_Style", prop="font-family",
                                                 default="monospace",
                                                 save=True)

        code_pattern = re.compile(r'```(\w+)\n(.*?)\n```', re.DOTALL)
        if text:
            matches = code_pattern.findall(text)
            for language, code in matches:
                escaped_code = html.escape('\n' + code)
                formatted_code = (
                    f'<pre style="font-size: {font_size}; font-family: {font_family}; background-color: {background_color}; color: {color};"><code>{escaped_code}</code></pre>')
                text = text.replace(f'```{language}\n{code}\n```', formatted_code)
        return text

    def highlight_search_text(self, target_text, search_text):
        color = Utility.get_settings_value(section="AI_Code_Style", prop="color",
                                           default="#ccc",
                                           save=True)
        background_color = Utility.get_settings_value(section="AI_Code_Style", prop="background-color",
                                                      default="#333333",
                                                      save=True)

        # Escape HTML characters
        target_text = html.escape(target_text)

        # Preserve carriage returns and tabs
        target_text = target_text.replace('\n', '<br>')
        target_text = target_text.replace('\t', '&nbsp;' * 4)

        search_text_escaped = re.escape(search_text)
        search_pattern = re.compile(search_text_escaped, re.IGNORECASE)

        matches = search_pattern.findall(target_text)
        for match in matches:
            formatted_code = f'<span style="color: {color}; background-color: {background_color};">{match}</span>'
            target_text = target_text.replace(match, formatted_code)

        return target_text

    def apply_highlight(self, text: str):
        self.user_text.setTextFormat(Qt.TextFormat.RichText)
        self.user_text.setText(text)

    def get_chat_type(self):
        return self.chat_type

    def add_text(self, text: str):
        self.text_result.append(text)
        self.user_text.setText(self.user_text.text() + text)

    def apply_style(self):
        formatted_text = self.format_code_snippet(self.get_original_text())
        self.user_text.setText(formatted_text)

    def clear_text(self):
        if self.user_text.text() == "":
            self.user_text.setText(
                self.get_original_text())
            self.apply_style()
        else:
            self.user_text.setText("")

    def show_original_text(self):
        self.user_text.setText(self.get_original_text())
        if self.no_style:
            self.no_style = False
        else:
            self.apply_style()
            self.no_style = True

    def get_original_text(self):
        return "".join(filter(None, self.text_result))

    def set_model_name(self, name):
        self.model_label.setText(name)

    def toggle_text_format(self, enable_markdown):
        current_format = self.user_text.textFormat()
        if enable_markdown and (current_format == Qt.TextFormat.PlainText):
            self.user_text.setTextFormat(Qt.TextFormat.MarkdownText)
        else:
            self.user_text.setTextFormat(Qt.TextFormat.PlainText)
