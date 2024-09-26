import base64
import os
import sys
import tempfile
from pathlib import Path

import openai
import torch
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

from util.Constants import UI, MODEL_MESSAGE
from util.SettingsManager import SettingsManager


class Utility:

    @staticmethod
    def check_openai_api_key(api_key):
        openai.api_key = api_key

        try:
            response = openai.models.list().model_dump()
            if response['data']:
                return True
            else:
                return False
        except openai.AuthenticationError:
            print(f"{MODEL_MESSAGE.AUTHENTICATION_FAILED_OPENAI}")
            return False
        except Exception as exception:
            print(f"{MODEL_MESSAGE.UNEXPECTED_ERROR} {str(exception)}")
            return False

    @staticmethod
    def get_openai_model_list(api_key):
        openai.api_key = api_key

        try:
            response = openai.models.list().model_dump()
            response_data = response['data']
            gtp_ids = sorted([item['id'] for item in response_data if
                              'instruct' not in item['id'] and item['id'].strip().startswith('gpt')],
                             key=lambda x: ('gpt-3.5' in x, x))
            return gtp_ids
        except openai.AuthenticationError:
            print(f"{MODEL_MESSAGE.AUTHENTICATION_FAILED_OPENAI}")
            return []
        except Exception as exception:
            print(f"{MODEL_MESSAGE.UNEXPECTED_ERROR} {str(exception)}")
            return []

    @staticmethod
    def get_icon_path(folder: str, icon: str):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = Path(os.path.dirname(__file__))
            base_path = base_path.parents[0]  # root path

        icon_path = os.path.join(base_path, folder, icon)
        icon_path = icon_path.replace(os.sep, '/')

        if not os.path.exists(icon_path):
            print(f"{UI.ICON_FILE_ERROR} {icon_path} {UI.ICON_FILE_NOT_EXIST}")
            return None
        return icon_path

    @staticmethod
    def get_settings_value(section: str, prop: str, default: str, save: bool) -> str:
        settings = SettingsManager.get_settings()
        settings.beginGroup(section)

        value = settings.value(prop, None)

        if value is None:
            if save:
                settings.setValue(prop, default)
                settings.sync()
            value = default

        settings.endGroup()
        return value

    @staticmethod
    def confirm_dialog(title: str, message: str) -> bool:
        dialog = QDialog()
        dialog.setWindowTitle(title)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.setLayout(QVBoxLayout())

        message_label = QLabel(message)
        dialog.layout().addWidget(message_label)

        dialog_buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No)
        dialog.layout().addWidget(dialog_buttonbox)

        no_button = dialog_buttonbox.button(QDialogButtonBox.StandardButton.No)
        no_button.setDefault(True)
        no_button.setFocus()

        def on_click(button):
            dialog.done(dialog_buttonbox.standardButton(button) == QDialogButtonBox.StandardButton.Yes)

        dialog_buttonbox.clicked.connect(on_click)

        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted

    @staticmethod
    def base64_encode_file(path):
        with open(path, UI.FILE_READ_IN_BINARY_MODE) as file:
            return base64.b64encode(file.read()).decode(UI.UTF_8)

    @staticmethod
    def detele_icc_profile(image_path):
        img = Image.open(image_path)
        img.info.pop('icc_profile', None)
        img.save(image_path)

    @staticmethod
    def create_temp_file(content, extension_name, apply_decode):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + extension_name) as temp_file:
            if apply_decode:
                temp_file.write(base64.b64decode(content))
            else:
                temp_file.write(content)
            temp_file.flush()
            temp_file_name = temp_file.name
        return temp_file_name

    @staticmethod
    def resize_image(image_path, image_size):
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            max_dimension = max(original_width, original_height)
            if max_dimension > image_size:
                scale_factor = image_size / max_dimension
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
            else:
                new_width, new_height = original_width, original_height

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            base, ext = os.path.splitext(image_path)
            new_image_path = f"{base}_new{ext}"
            resized_img.save(new_image_path)

            return new_image_path

    @staticmethod
    def get_torch_device(device: str = "auto"):
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda:0"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        else:
            return device
