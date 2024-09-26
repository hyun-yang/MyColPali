import base64

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class ImageDisplay(QGraphicsView):
    def __init__(self, image_data):
        super().__init__()

        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem()
        self._pixmap = QPixmap()
        self.image_data = base64.b64decode(image_data)
        self.pixmap.loadFromData(self.image_data)

        self.show_image()

    @property
    def pixmap(self):
        return self._pixmap

    def show_image(self):
        self.scene.clear()
        self.item = self.scene.addPixmap(self.pixmap)
        self.setScene(self.scene)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
