import logging
import sys
from os import path

from PyQt6.QtCore import QSize, QFile
from PyQt6.QtGui import QIcon, QAction, QGuiApplication, QPixmap, QFont
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QMenu, QToolBar, QHBoxLayout, \
    QPushButton, QWidgetAction, QSpacerItem, QSizePolicy, QStackedWidget, QStyleFactory, QSplashScreen, \
    QMessageBox, QLabel

from util.AnimatedProgressBar import AnimatedProgressBar
from util.AppInfoDialog import AppInfoDialog
from util.Constants import Constants, MainWidgetIndex, UI, AIProviderName
from util.DataManager import DataManager
from util.GlobalSetting import GlobalSetting
from util.SettingsManager import SettingsManager
from util.Utility import Utility
from util.VerticalLine import VerticalLine
from vision.VisionPresenter import VisionPresenter

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initialize_manager()
        self.initialize_variables()
        self.initialize_ui()

    def initialize_manager(self):
        if not QFile.exists(Constants.SETTINGS_FILENAME):
            QMessageBox.warning(self, UI.WARNING_TITLE, UI.WARNING_API_KEY_SETTING_MESSAGE)

        SettingsManager.initialize_settings()
        self._settings = SettingsManager.get_settings()

        DataManager.initialize_database()
        self._database = DataManager.get_database()

    def initialize_variables(self):
        self.progress_bar = None
        self.current_llm = None
        self.current_system = None

    def initialize_ui(self):

        self.initialize_window()

        self._vision = VisionPresenter()
        self._vision.model.thread_started_signal.connect(self.show_result_info)
        self._vision.model.response_finished_signal.connect(self.show_result_info)

        self._vision.colpali_model.thread_started_signal.connect(self.show_result_info)
        self._vision.colpali_model.file_index_finished_signal.connect(self.show_result_info)

        self.set_main_widgets()

        self.show()

    def set_main_widgets(self):
        self._main_widget = QStackedWidget()

        self._main_widget_index = {
            MainWidgetIndex.VISION_WIDGET: self._main_widget.addWidget(self._vision),
        }
        self.setCentralWidget(self._main_widget)
        self.set_current_widget(MainWidgetIndex.VISION_WIDGET)

    def set_current_widget(self, index: MainWidgetIndex):
        self._settings.setValue('AI_Provider/llm', AIProviderName.OPENAI.value)
        self._main_widget.setCurrentIndex(self._main_widget_index[index])

    def initialize_window(self):
        self.setWindowTitle(Constants.APPLICATION_TITLE)
        self.setWindowIcon(QIcon(Utility.get_icon_path('ico', 'app.svg')))
        self.setGeometry(*self.set_window_size(3 / 5))
        self.set_actions()
        self.set_menubar()
        self.set_toolbar()
        self.set_statusbar()

    def set_actions(self):
        self.vision_action = QAction("ColPali", self)
        self.vision_action.setStatusTip(UI.COLPALI_TIP)
        self.vision_action.triggered.connect(lambda: self.set_current_widget(MainWidgetIndex.VISION_WIDGET))

        self.setting_action = QAction("Setting", self)
        self.setting_action.setStatusTip(UI.SETTING_TIP)
        self.setting_action.triggered.connect(self.open_global_setting)

        self.close_action = QAction("Close", self)
        self.close_action.setStatusTip(UI.CLOSE_TIP)
        self.close_action.triggered.connect(self.close)

        self.app_info_action = QAction("About", self)
        self.app_info_action.setStatusTip(UI.ABOUT_TIP)
        self.app_info_action.triggered.connect(self.show_app_info)

    def set_window_size(self, ratio):
        sg = QGuiApplication.primaryScreen().availableGeometry()

        width = int(sg.width() * ratio)
        height = int(sg.height() * ratio)
        left = int((sg.width() - width) / 2)
        top = int((sg.height() - height) / 2)
        return left, top, width, height

    def set_menubar(self):
        menubar = self.menuBar()

        file_menu = QMenu(UI.FILE, self)
        file_menu.addAction(self.setting_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_action)
        menubar.addMenu(file_menu)

        view_menu = QMenu(UI.VIEW, self)
        view_menu.addAction(self.vision_action)
        menubar.addMenu(view_menu)

        help_menu = QMenu(UI.HELP, self)
        help_menu.addAction(self.app_info_action)
        menubar.addMenu(help_menu)

    def set_toolbar(self):
        self.buttons = []

        icon_size = QSize(32, 32)
        main_toolbar = QToolBar()

        main_toolbar_layout = QHBoxLayout()

        self.setting_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'setting.svg')), '')
        self.setting_button.setFixedSize(40, 40)
        self.setting_button.setIconSize(icon_size)
        self.setting_button.setCheckable(True)
        self.setting_button.setToolTip(UI.SETTING_TIP)
        self.setting_button.clicked.connect(self.open_global_setting)

        self.exit_button = QPushButton(QIcon(Utility.get_icon_path('ico', 'exit.svg')), '')
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setIconSize(icon_size)
        self.exit_button.setCheckable(True)
        self.exit_button.setToolTip(UI.CLOSE_TIP)
        self.exit_button.clicked.connect(self.close)

        self.vision_button = self.create_button('vision.svg', UI.VISION, MainWidgetIndex.VISION_WIDGET)

        self.buttons.extend([self.vision_button, self.setting_button, self.exit_button])

        main_toolbar_layout.addWidget(self.vision_button)
        main_toolbar_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_toolbar_layout.addWidget(self.setting_button)
        main_toolbar_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_toolbar_layout.addWidget(self.exit_button)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(main_toolbar_layout)

        self.toolbar_action = QWidgetAction(self)
        self.toolbar_action.setDefaultWidget(toolbar_widget)

        main_toolbar.addAction(self.toolbar_action)
        main_toolbar.setMovable(True)

        self.addToolBar(main_toolbar)

    def create_button(self, icon_path, tooltip, widget_index):
        button = QPushButton(QIcon(Utility.get_icon_path('ico', icon_path)), '')
        button.setFixedSize(40, 40)
        button.setIconSize(QSize(32, 32))
        button.setCheckable(True)
        button.setToolTip(tooltip)
        if widget_index:
            button.setProperty('widget_index', widget_index)
            button.clicked.connect(lambda _, btn=button: self.toggle_buttons(btn))
        return button

    def toggle_buttons(self, current_button):
        for button in self.buttons:
            button.setChecked(False)
        current_button.setChecked(True)
        widget_index = current_button.property('widget_index')
        if widget_index:
            self.set_current_widget(widget_index)

    def set_statusbar(self):
        self.status_bar = self.statusBar()

    def open_global_setting(self):
        self.toggle_buttons(self.setting_button)
        self.global_settings = GlobalSetting()
        self.global_settings.exec()

    def show_result_info(self, model=None, finish_reason=None, elapsed_time=None, stream=False):
        boldFont = QFont()
        boldFont.setBold(True)

        model_color = Utility.get_settings_value(section="Info_Label_Style", prop="model-color",
                                                 default="green",
                                                 save=True)

        model_time_label_style = f"""
                    QLabel {{
                        color: {model_color};
                    }}
                    """

        elapsed_time_color = Utility.get_settings_value(section="Info_Label_Style", prop="elapsedtime-color",
                                                        default="orange",
                                                        save=True)
        elapsed_time_label_style = f"""
                    QLabel {{
                        color: {elapsed_time_color};
                    }}
                    """

        finish_reason_color = Utility.get_settings_value(section="Info_Label_Style", prop="finishreason-color",
                                                         default="blue",
                                                         save=True)
        finish_reason_label_style = f"""
                    QLabel {{
                        color: {finish_reason_color};
                    }}
                    """

        status_bar = self.statusBar()
        status_bar.setFont(boldFont)

        for widget in status_bar.findChildren(QWidget):
            status_bar.removeWidget(widget)

        if self.progress_bar:
            self.progress_bar.stop_animation()
            self.progress_bar.deleteLater()
            self.progress_bar = None

        if all(parameter is not None for parameter in [model, finish_reason, elapsed_time]):
            model_label = QLabel()
            model_label.setText(Constants.MODEL_PREFIX + model)
            model_label.setFont(boldFont)
            model_label.setStyleSheet(model_time_label_style)

            elapsed_time_label = QLabel()
            elapsed_time_label.setText(Constants.ELAPSED_TIME + format(elapsed_time, ".2f"))
            elapsed_time_label.setFont(boldFont)
            elapsed_time_label.setStyleSheet(elapsed_time_label_style)

            finish_reason_label = QLabel()
            finish_reason_label.setText(Constants.FINISH_REASON + finish_reason)
            finish_reason_label.setFont(boldFont)
            if finish_reason == Constants.FORCE_STOP:
                finish_reason_label.setStyleSheet("color: red")
            else:
                finish_reason_label.setStyleSheet(finish_reason_label_style)

            status_bar.addPermanentWidget(model_label)
            status_bar.addPermanentWidget(VerticalLine())
            status_bar.addPermanentWidget(elapsed_time_label)
            status_bar.addPermanentWidget(VerticalLine())
            status_bar.addPermanentWidget(finish_reason_label)
            status_bar.addPermanentWidget(VerticalLine())

        else:
            self.progress_bar = AnimatedProgressBar()
            self.progress_bar.start_animation()
            status_bar.addPermanentWidget(self.progress_bar)

    def show_app_info(self):
        aboutDialog = AppInfoDialog()
        aboutDialog.exec()

    def closeEvent(self, event):
        self.toggle_buttons(self.exit_button)
        should_close = Utility.confirm_dialog(UI.EXIT_APPLICATION_TITLE, UI.EXIT_APPLICATION_MESSAGE)
        if should_close:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create(Constants.FUSION))

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = path.dirname(__file__)

    splash_image_path = path.join(base_path, 'splash', 'pyqt-small.png')
    app_splash = QSplashScreen(QPixmap(splash_image_path))
    app_splash.show()

    sg = QGuiApplication.primaryScreen().availableGeometry()
    screen_width = sg.width()

    mainWindow = MainWindow()
    app_splash.finish(mainWindow)

    if screen_width < 1450:
        mainWindow.showMaximized()
    else:
        mainWindow.show()

    sys.exit(app.exec())
