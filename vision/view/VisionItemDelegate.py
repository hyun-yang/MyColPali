from PyQt6.QtCore import QRect, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QStyledItemDelegate

from util.Constants import UI
from util.Utility import Utility


class VisionItemDelegate(QStyledItemDelegate):
    row_id_signal = pyqtSignal(int)

    def __init__(self, vision_view, parent=None):
        super().__init__(parent)
        self.vision_view = vision_view
        self.mouse_over_index = None

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if self.mouse_over_index == index:
            # Draw buttons when mouse is over the item
            minus_button_icon = QIcon(Utility.get_icon_path('ico', 'card--minus.png'))
            edit_button_icon = QIcon(Utility.get_icon_path('ico', 'card--pencil.png'))

            minus_button_rect = QRect(option.rect.right() - UI.ITEM_ICON_SIZE * 2 - UI.ITEM_PADDING,
                                      option.rect.top(), UI.ITEM_ICON_SIZE, UI.ITEM_ICON_SIZE)
            edit_button_rect = QRect(option.rect.right() - UI.ITEM_ICON_SIZE, option.rect.top(),
                                     UI.ITEM_ICON_SIZE, UI.ITEM_ICON_SIZE)
            painter.drawPixmap(minus_button_rect,
                               minus_button_icon.pixmap(UI.ITEM_ICON_SIZE, UI.ITEM_ICON_SIZE))
            painter.drawPixmap(edit_button_rect,
                               edit_button_icon.pixmap(UI.ITEM_ICON_SIZE, UI.ITEM_ICON_SIZE))

    def editorEvent(self, event, model, option, index):
        if event.type() == QMouseEvent.Type.MouseButtonPress:
            if QRect(option.rect.right() - UI.ITEM_ICON_SIZE * 2 - UI.ITEM_PADDING, option.rect.top(),
                     UI.ITEM_ICON_SIZE, UI.ITEM_ICON_SIZE).contains(event.pos()):
                self.row_id_signal.emit(index.row())
            elif QRect(option.rect.right() - UI.ITEM_ICON_SIZE, option.rect.top(), UI.ITEM_ICON_SIZE,
                       UI.ITEM_ICON_SIZE).contains(event.pos()):
                vision_item = model.get_vision(index)
                self.vision_view.rename_chat(index, vision_item['title'])
        return super().editorEvent(event, model, option, index)

    def set_mouse_over_index(self, index):
        self.mouse_over_index = index

    def sizeHint(self, option, index):
        original_size = super().sizeHint(option, index)
        return QSize(original_size.width(),
                     original_size.height() + UI.ITEM_EXTRA_SIZE)
