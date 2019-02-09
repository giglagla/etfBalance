#!/usr/bin/python
'''
Created on 31 janv. 2019

@author: guillaume
'''

from PyQt5.QtWidgets import QApplication
import sys


class MainWindow():
    def __init__(self):
        self.nom=0
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("EtfBalance")
    app.setStyle("Fusion")
    sys.exit(app.exec_())
