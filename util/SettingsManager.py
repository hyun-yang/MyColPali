from PyQt6.QtCore import QSettings
from util.Constants import Constants


class SettingsManager:
    __settings = None

    @classmethod
    def initialize_settings(cls):
        if cls.__settings is None:
            cls.__settings = QSettings(Constants.SETTINGS_FILENAME, QSettings.Format.IniFormat)

    @classmethod
    def get_settings(cls) -> QSettings:
        if cls.__settings is None:
            cls.initialize_settings()
        return cls.__settings
