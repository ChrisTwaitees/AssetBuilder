from PySide2 import QtWidgets
from PySide2.QtCore import Signal

from model.tweakables import tweakables
from model.builder import builder


class TweakableWidget(QtWidgets.QWidget):
    def __init__(self, tweakable: tweakables.TweakableBase | tweakables.TweakableListBase):
        super().__init__()
        self.setMaximumHeight(75)
        self._tweakable = tweakable
        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()

    def _create_widgets(self):
        self._layout.addWidget(QtWidgets.QLabel(self._tweakable.name))
        self._value_line_edit = QtWidgets.QLineEdit(str(self._tweakable.value))
        self._value_line_edit.textChanged.connect(self._on_value_changed)
        self._layout.addWidget(self._value_line_edit)

    def _on_value_changed(self):
        self._tweakable.value = self._value_line_edit.text()


class SettingsWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._current_builder: builder.Builder | None = None

        self._create_widgets()

    def _create_widgets(self):
        self._info_label = QtWidgets.QLabel("Settings")
        self._layout.addWidget(self._info_label)

        self._layout.addWidget(QtWidgets.QLabel("AssetSettings"))
        self._asset_settings_list = QtWidgets.QListWidget()
        self._layout.addWidget(self._asset_settings_list)

        # self._layout.addWidget(QtWidgets.QLabel("BuildStepSettings"))
        # self._build_step_settings_list = QtWidgets.QListWidget()
        # self._layout.addWidget(self._build_step_settings_list)

    def _populate_asset_settings(self):
        self._asset_settings_list.clear()

        for builder_tweakable in self._current_builder.tweakables:
            for val, tweakable in builder_tweakable.build_step_tweakables.items():
                item_widget = TweakableWidget(tweakable)
                new_item = QtWidgets.QListWidgetItem(self._asset_settings_list)
                new_item.setSizeHint(item_widget.size())
                self._asset_settings_list.addItem(new_item)
                self._asset_settings_list.setItemWidget(new_item, item_widget)

    def set_builder(self, builder: builder.Builder):
        self._current_builder = builder
        steps_names = [step.__step_name__ for step in builder.build_steps]
        self._info_label.setText(f"Asset : {builder.asset.raw_path},\nSteps : {steps_names}")

        self._populate_asset_settings()
