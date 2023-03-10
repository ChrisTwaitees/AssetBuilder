from PySide2 import QtWidgets


class BatchTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._create_widgets()

    def _create_widgets(self):
        self._test_bttn = QtWidgets.QPushButton("Batch Tab")
        self._layout.addWidget(self._test_bttn)