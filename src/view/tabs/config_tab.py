import os
import re
from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore

from model.builder import builder_config

from log import LOG
import paths


class DraggableWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Style Sheets
        self.default_style_sheet = "QLabel {border: 0px solid black;" \
                                   "border-radius: 0px;}"
        self.highlighted_style_sheet = "QLabel {border: 4px solid blue;" \
                                       "border-radius: 4px;}"

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = e.pos()

        # MOUSE HOVERS

    def enterEvent(self, e):
        e.accept()
        self.setStyleSheet(self.highlighted_style_sheet)

    def leaveEvent(self, e):
        e.accept()
        self.setStyleSheet(self.default_style_sheet)

        # DRAG AND DROP - LEAVE

    def mouseMoveEvent(self, e):
        if not (e.buttons() and QtCore.Qt.LeftButton):
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return
        drag = QtGui.QDrag(self)

        mimedata = QtCore.QMimeData()
        mimedata.setText(self.name)

        # Drag and dropping data
        drag.setMimeData(mimedata)
        pixmap = QtGui.QPixmap(self.size())
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

        # DRAG AND DROP - ENTER

    def dragEnterEvent(self, e):
        e.accept()
        self.setStyleSheet(self.highlighted_style_sheet)

    def dragLeaveEvent(self, e):
        e.accept()
        self.setStyleSheet(self.default_style_sheet)


class StepWidget(DraggableWidget):
    delete_tag_signal = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, step, editable=False):
        super().__init__()
        self._name = step
        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)

        pixmap = QtGui.QPixmap(os.path.join(paths.get_icons_root(), "step_dark.png"))
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(pixmap)
        self._layout.addWidget(icon_lbl)

        self._layout.addWidget(QtWidgets.QLabel(step))

        self._editable = editable
        if self._editable:
            delete_bttn = QtWidgets.QPushButton(
                QtGui.QIcon(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "close_dark.png"))), "")
            delete_bttn.clicked.connect(self.on_delete)
            self._layout.addWidget(delete_bttn)

    @property
    def name(self):
        return self._name

    def on_delete(self):
        self.delete_tag_signal.emit(self)


class StepsListWidget(QtWidgets.QListWidget):
    items_changed_signal = QtCore.Signal()

    def __init__(self, editable=False):
        super().__init__()
        self.setFlow(QtWidgets.QListWidget.Flow.LeftToRight)
        self._editable = editable
        if self._editable:
            self.setAcceptDrops(True)

    def mimeTypes(self):
        mimetypes = super().mimeTypes()
        if self._editable:
            mimetypes.append('text/plain')
        return mimetypes

    def dropMimeData(self, index, data, action):
        if data.hasText() and self._editable:
            self.add_step(data.text())
            return True
        else:
            return super().dropMimeData(index, data, action)

    def set_steps(self, steps):
        self.clear()
        for s in steps:
            self.add_step(s)

    def add_step(self, step):
        list_item = QtWidgets.QListWidgetItem()
        self.addItem(list_item)
        step_widget = StepWidget(step, self._editable)
        step_widget.delete_tag_signal.connect(self.on_step_delete)
        list_item.setSizeHint(step_widget.sizeHint())
        self.setItemWidget(list_item, step_widget)
        self.items_changed_signal.emit()

    def on_step_delete(self, step_widget):
        if self._editable:
            remove_items = [i for i in range(self.count()) if self.itemWidget(self.item(i)) == step_widget]
            for i in remove_items:
                i = self.takeItem(i)
                del i
                self.items_changed_signal.emit()

    @property
    def steps(self):
        return [self.itemWidget(self.item(i)).name for i in range(self.count())]


class ConfigButton(QtWidgets.QPushButton):
    def __init__(self, config):
        self._config = config
        icon = QtGui.QIcon(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "config_dark.png")))
        QtWidgets.QPushButton.__init__(self, icon, config.name)
        # Style Sheets
        self.default_style_sheet = "QLabel {border: 0px solid black;" \
                                   "border-radius: 0px;}"
        self.highlighted_style_sheet = "QLabel {border: 4px solid blue;" \
                                       "border-radius: 4px;}"

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = e.pos()
        super().mousePressEvent(e)

    def enterEvent(self, e):
        e.accept()
        self.setStyleSheet(self.highlighted_style_sheet)

    def leaveEvent(self, e):
        e.accept()
        self.setStyleSheet(self.default_style_sheet)

        # DRAG AND DROP - LEAVE

    def mouseMoveEvent(self, e):
        if not (e.buttons() and QtCore.Qt.LeftButton):
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return
        drag = QtGui.QDrag(self)

        mimedata = QtCore.QMimeData()
        mimedata.setText(self._config.name)

        # Drag and dropping data
        drag.setMimeData(mimedata)
        pixmap = QtGui.QPixmap(self.size())
        painter = QtGui.QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

        # DRAG AND DROP - ENTER

    def dragEnterEvent(self, e):
        e.accept()
        self.setStyleSheet(self.highlighted_style_sheet)

    def dragLeaveEvent(self, e):
        e.accept()
        self.setStyleSheet(self.default_style_sheet)


class ConfigsListWidget(QtWidgets.QWidget):
    set_config_signal = QtCore.Signal(builder_config.BuildConfig)

    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        configs_search = QtWidgets.QLineEdit("Search...")
        configs_search.textChanged.connect(self.on_search_text_changed)
        self._layout.addWidget(configs_search)

        self._configs = []
        self._search_text = ""

        self._configs_list = QtWidgets.QListWidget()
        self._configs_list.setFlow(QtWidgets.QListWidget.Flow.LeftToRight)
        self._layout.addWidget(self._configs_list)

    def on_search_text_changed(self, search_text):
        self._search_text = search_text
        self.refresh_configs(self._search_text)

    def refresh_configs(self, search_text):
        self._configs_list.clear()

        if not search_text:
            for c in self._configs:
                list_item = QtWidgets.QListWidgetItem()
                self._configs_list.addItem(list_item)
                config_widget = ConfigButton(c)
                config_widget.clicked.connect(partial(self.set_config, config=c))
                list_item.setSizeHint(config_widget.sizeHint())
                self._configs_list.setItemWidget(list_item, config_widget)
        else:
            for c in self._configs:
                if search_text.lower() in c.name.lower():
                    list_item = QtWidgets.QListWidgetItem()
                    self._configs_list.addItem(list_item)
                    config_widget = ConfigButton(c)
                    config_widget.clicked.connect(partial(self.set_config, config=c))
                    list_item.setSizeHint(config_widget.sizeHint())
                    self._configs_list.setItemWidget(list_item, config_widget)

    def set_configs(self, configs):
        self._configs = configs
        self.refresh_configs(self._search_text)

    def set_config(self, config):
        self.set_config_signal.emit(config)

    @property
    def steps(self):
        return [self.itemWidget(self.item(i)).name for i in range(self.count())]


class NewConfigWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._config = builder_config.BuildConfig()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()

    def _create_widgets(self):
        # new config
        header_layout = QtWidgets.QHBoxLayout()
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "config_dark.png")))
        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(QtWidgets.QLabel("Config Name"))
        self._config_name = QtWidgets.QLineEdit("New config...")
        self._config_name.textChanged.connect(self._on_config_name_changed)
        header_layout.addWidget(self._config_name)
        self._layout.addLayout(header_layout)

        # regex
        header_layout = QtWidgets.QHBoxLayout()
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "regex_dark.png")))
        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(QtWidgets.QLabel("Regex"))
        self._regex_edit = QtWidgets.QLineEdit("...")
        self._regex_edit.textChanged.connect(self._on_regex_changed)
        header_layout.addWidget(self._regex_edit)
        # test string
        header_layout.addWidget(QtWidgets.QLabel("Test string : "))
        self._test_regex_edit = QtWidgets.QLineEdit("TestString")
        self._test_regex_edit.setStyleSheet("border: 0px solid black;")
        self._test_regex_edit.textChanged.connect(self._on_regex_test_changed)
        header_layout.addWidget(self._test_regex_edit)
        self._layout.addLayout(header_layout)

        # parent config
        header_layout = QtWidgets.QHBoxLayout()
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setPixmap(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "parent_dark.png")))
        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(QtWidgets.QLabel("Parent Config"))
        self._parent_config = QtWidgets.QLabel("Drag and drop parent config.")
        self._parent_config.setAcceptDrops(True)
        header_layout.addWidget(self._parent_config)
        self._layout.addLayout(header_layout)

        # config steps
        steps_layout = QtWidgets.QHBoxLayout()
        steps_icon_lbl = QtWidgets.QLabel()
        steps_icon_lbl.setPixmap(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "step_dark.png")))
        steps_layout.addWidget(steps_icon_lbl)
        steps_layout.addWidget(QtWidgets.QLabel("Steps"))
        self._steps_list = StepsListWidget(editable=True)
        self._steps_list.items_changed_signal.connect(self._update_preview)
        steps_layout.addWidget(self._steps_list)
        self._layout.addLayout(steps_layout)

        self._preview = QtWidgets.QLabel(str(self._config.json))
        self._layout.addWidget(self._preview)

        bttns_layout = QtWidgets.QHBoxLayout()
        save_bttn = QtWidgets.QPushButton(
            QtGui.QIcon(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "save_dark.png"))), "")
        save_bttn.clicked.connect(self._on_config_save)
        bttns_layout.addWidget(save_bttn)
        clear_bttn = QtWidgets.QPushButton(
            QtGui.QIcon(QtGui.QPixmap(os.path.join(paths.get_icons_root(), "delete_dark.png"))), "")
        bttns_layout.addWidget(clear_bttn)
        self._layout.addLayout(bttns_layout)

    def _on_parent_config_changed(self, text):
        LOG.info("Parent config set to : {}".format(text))
        self._config.name = text
        self._update_preview()

    def _on_config_save(self):
        LOG.info("Saving config...")

    def _on_config_name_changed(self, name):
        self._config.name = name
        self._update_preview()

    def _on_regex_changed(self, regex):
        self._config.regex = regex
        self._on_regex_test_changed()
        self._update_preview()

    def _on_regex_test_changed(self, test_string=""):
        if self._regex_edit.text():
            try:
                if re.match(self._regex_edit.text(), self._test_regex_edit.text()):
                    self._test_regex_edit.setStyleSheet("border: 3px solid green;")
                    return
            except BaseException as e:
                LOG.error(e)
        elif not test_string:
            self._test_regex_edit.setStyleSheet("border: 0px solid green;")
            return
        self._test_regex_edit.setStyleSheet("border: 3px solid red;")


    def _update_preview(self):
        self._config.steps = self._steps_list.steps
        self._preview.setText(str(self._config.json))

    @property
    def config_name(self):
        return self._config.name

    @property
    def config(self):
        return self._config


class ConfigTab(QtWidgets.QWidget):
    refresh_configs = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()

    def _create_widgets(self):
        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addWidget(QtWidgets.QLabel("Existing Configs..."))
        refresh_builders_bttn = QtWidgets.QPushButton("Refresh")
        refresh_builders_bttn.clicked.connect(self.refresh_configs)
        header_layout.addWidget(refresh_builders_bttn)
        self._layout.addLayout(header_layout)

        # configs list
        self._configs_list = ConfigsListWidget()
        self._configs_list.set_config_signal.connect(self.set_existing_config)
        self._layout.addWidget(self._configs_list)

        # steps list
        self._steps_list = StepsListWidget()
        self._layout.addWidget(self._steps_list)

        # new config
        self._new_config = NewConfigWidget()
        self._layout.addWidget(self._new_config)

    def set_existing_config(self, config):
        self._steps_list.set_steps(config.steps)

    def set_configs(self, configs):
        self._configs_list.set_configs(configs)
