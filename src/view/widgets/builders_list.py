from model.builder import builder

from PySide2 import QtWidgets
from PySide2.QtCore import Signal


class BuilderWidget(QtWidgets.QWidget):
    def __init__(self, builder: builder.Builder):
        super().__init__()
        self.setMaximumHeight(120)
        self._builder = builder
        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()

    @property
    def builder(self):
        return self._builder

    @property
    def checked(self):
        return self._checkbox.isChecked()

    def _create_widgets(self):
        self._checkbox = QtWidgets.QCheckBox("Import")
        self._checkbox.setChecked(True)
        self._layout.addWidget(self._checkbox)

        print(self._builder.asset.raw_path)
        self.asset_path = QtWidgets.QLabel(self._builder.asset.raw_path)
        self._layout.addWidget(self.asset_path)


class BuildersList(QtWidgets.QListWidget):
    builder_selected_signal = Signal(builder.Builder)
    def __init__(self):
        super().__init__()
        self.setSelectionMode(self.__class__.ExtendedSelection)
        self.itemSelectionChanged.connect(self._on_item_changed)

    def _on_item_changed(self):
        selected_builders = [self.itemWidget(item).builder for item in self.selectedItems()]
        if selected_builders:
            self.builder_selected_signal.emit(selected_builders[0])

    def set_builders(self, builders: [builder.Builder]):
        self.clear()
        for blder in builders:
            item_widget = BuilderWidget(blder)
            new_item = QtWidgets.QListWidgetItem(self)
            new_item.setSizeHint(item_widget.size())
            self.addItem(new_item)
            self.setItemWidget(new_item, item_widget)

