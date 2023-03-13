from PySide2 import QtWidgets
import logging


class LogWidget(QtWidgets.QWidget, logging.Handler):
    __loggers__ = []

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        logging.Handler.__init__(self)
        self.setLevel(logging.DEBUG)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._message_box = QtWidgets.QTextEdit()
        self._layout.addWidget(self._message_box)

    def emit(self, record):
        self._message_box.textCursor().insertText(("\n{}".format(record.message)))

    def close(self):
        # dettach loggers
        for logger in self.__loggers__:
            logger.removeHandler(self)

    def attach_logger(self, logger):
        if logger not in self.__loggers__:
            self.__loggers__.append(logger)
            logger.addHandler(self)
