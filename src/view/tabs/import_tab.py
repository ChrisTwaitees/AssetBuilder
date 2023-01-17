from model.builder import builder

from view.widgets import filebrowser
from view.widgets import builders_list
from view.widgets import settings

from PySide2 import QtWidgets
from PySide2.QtCore import Signal


class ImportTab(QtWidgets.QWidget):
    import_triggered_signal = Signal()
    set_builders_signal = Signal(list)
    get_builders_from_directory_signal = Signal(str)

    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()
        self._connect_signals()

    def _create_widgets(self):
        # File browser
        self.file_browser = filebrowser.FileBrowser()
        self._layout.addWidget(self.file_browser, stretch=1)

        # Assets list and settings
        self._builders_splitter = QtWidgets.QSplitter()
        self._builders_list = builders_list.BuildersList()
        self._builders_splitter.addWidget(self._builders_list)
        self._settings = settings.SettingsWidget()
        self._builders_splitter.addWidget(self._settings)
        self._layout.addWidget(self._builders_splitter, stretch=9)

        # Run button
        self._import_bttn = QtWidgets.QPushButton("Import")
        self._import_bttn.clicked.connect(self._import_bttn_clicked)
        self._layout.addWidget(self._import_bttn)

    def _connect_signals(self):
        self.file_browser.file_selected_signal.connect(self.get_builders_from_directory_signal)
        self.set_builders_signal.connect(self._set_builders)
        self._builders_list.builder_selected_signal.connect(self._settings.set_builder)

    def _import_bttn_clicked(self):
        print("Import Bttn Clicked")
        self.import_triggered_signal.emit()

    def _set_builders(self, builders):
        self._builders_list.set_builders(builders)
