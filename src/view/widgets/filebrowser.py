import os
from PySide2 import QtWidgets
from PySide2.QtCore import Signal


class FileBrowser(QtWidgets.QWidget):
    file_selected_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)
        self._filepath = QtWidgets.QLineEdit("...")
        self._create_widgets()
        self._start_directory = self._get_start_directory()

    def _get_start_directory(self):
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        return os.path.join(desktop, "CharacterBuilder")

    @property
    def filepath(self):
        return self._filepath.text()

    def _create_widgets(self):
        lbl = QtWidgets.QLabel("Search Dir")
        self._layout.addWidget(lbl)

        self._layout.addWidget(self._filepath)

        self._open_file_browser_bttn = QtWidgets.QPushButton("Browse")
        self._open_file_browser_bttn.clicked.connect(self._launch_file_browser)
        self._layout.addWidget(self._open_file_browser_bttn)

    def _launch_file_browser(self):

        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setDirectory(self._start_directory)
        if dialog.exec_():
            fname = dialog.selectedFiles()
            if fname:
                self._filepath.setText(str(fname[0]))
                self.file_selected_signal.emit(self.filepath)
