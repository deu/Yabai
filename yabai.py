#!/usr/bin/env python

from sys import argv, exit
from PyQt4.QtGui import QApplication

from gui.mainwindow import MainWindow


class Yabai(QApplication):

    def __init__(self, args):

        super().__init__(args)
        self.mainwindow = MainWindow()


if __name__ == '__main__':
    yabai = Yabai(argv)
    exit(yabai.exec_())
