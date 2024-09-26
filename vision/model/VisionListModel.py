from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal


class VisionListModel(QAbstractListModel):
    new_vision_main_id_signal = pyqtSignal(int)
    remove_vision_signal = pyqtSignal(int)

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.vision_items = self.database.get_all_vision_main_list()
        self.filtered_vision_items = self.vision_items.copy()

    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_vision_items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.filtered_vision_items[index.row()]['title']

    def add_new_vision(self, title):
        vision_main_id = self.database.add_vision_main(title)
        if vision_main_id:
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.vision_items.insert(0, {'id': vision_main_id, 'title': title})
            self.filtered_vision_items = self.vision_items.copy()
            self.endInsertRows()
            self.new_vision_main_id_signal.emit(vision_main_id)

    def remove_vision(self, index):
        vision_id = self.vision_items[index]['id']
        if self.database.delete_vision_main(vision_id):
            self.beginRemoveRows(QModelIndex(), index, index)
            del self.vision_items[index]
            self.filtered_vision_items = self.vision_items.copy()
            self.endRemoveRows()
            self.remove_vision_signal.emit(vision_id)

    def update_vision(self, index, new_title):
        vision_id = self.vision_items[index.row()]['id']
        if self.database.update_vision_main(vision_id, new_title):
            self.vision_items[index.row()]['title'] = new_title
            self.filtered_vision_items = self.vision_items.copy()
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])

    def get_vision(self, index):
        return self.filtered_vision_items[index.row()]

    def get_index_by_vision_main_id(self, vision_id):
        for i, vision_item in enumerate(self.filtered_vision_items):
            if vision_item['id'] == vision_id:
                return i
        return None

    def filter_by_title(self, title):
        self.beginResetModel()
        if title and title.strip():
            self.filtered_vision_items = [item for item in self.vision_items if title.lower() in item['title'].lower()]
        else:
            self.filtered_vision_items = self.vision_items.copy()
        self.endResetModel()
