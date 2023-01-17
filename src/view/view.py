"""
Main Entry Point for Character Setup's UI
"""

import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Signal

from view.tabs import import_tab
from view.tabs import config_tab
from view.tabs import batch_tab


QT_APP = QtWidgets.QApplication(sys.argv)


class CharacterBuilderView(QtWidgets.QMainWindow):
    import_triggered_signal = Signal()
    set_builders_signal = Signal(list)
    get_builders_from_directory_signal = Signal(str)

    def __init__(self, parent=None):
        super(CharacterBuilderView, self).__init__(parent)
        self.setWindowTitle("Asset Builder")
        # Window attrs
        self.left = 0
        self.top = 0
        self.width = 750
        self.height = 750
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Add central widget
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        self._create_widgets()
        self._connect_signals()

    def _create_widgets(self):
        self._layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self._layout)

        self.import_tab = import_tab.ImportTab()
        self.config_tab = config_tab.ConfigTab()
        self.batch_tab = batch_tab.BatchTab()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.import_tab, "Import")
        self.tabs.addTab(self.config_tab, "Config")
        self.tabs.addTab(self.batch_tab, "Batch")

        self._layout.addWidget(self.tabs)

    def _connect_signals(self):
        self.import_tab.import_triggered_signal.connect(self.import_triggered_signal)
        self.set_builders_signal.connect(self.import_tab.set_builders_signal)
        self.import_tab.get_builders_from_directory_signal.connect(self.get_builders_from_directory_signal)

    def launch_ui(self):
        # Create and show the form
        self.show()
        # Run the main Qt loop
        sys.exit(QT_APP.exec_())
