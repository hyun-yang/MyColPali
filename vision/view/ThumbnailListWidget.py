from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget, QSizePolicy

from custom.ImageDisplay import ImageDisplay
from util.Constants import Constants


class ThumbnailListWidget(QScrollArea):

    def __init__(self):
        super().__init__()
        self.max_columns = Constants.THUMBNAIL_LIST_MAX_COLUMN
        self.initialize_ui()

    def initialize_ui(self):
        self.thumbnail_layout = QGridLayout()
        self.thumbnail_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.config_grid_columns(self.max_columns)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.thumbnail_layout)

        self.setWidget(self.mainWidget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_thumbnail(self, image_data):
        thumbnail = ImageDisplay(image_data)
        thumbnail.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.thumbnail_layout.addWidget(thumbnail)

    def config_grid_columns(self, num_columns):
        for col in range(num_columns):
            self.thumbnail_layout.setColumnStretch(col, 1)
