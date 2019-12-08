#!/usr/bin/python
'''
Created on 31 janv. 2019

@author: guillaume
'''

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
    QLabel, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QMainWindow
from PyQt5 import QtCore
import sys
import EtfBalance


class View(object):

    @staticmethod
    def buildQTableWidget(wallet):
        qtwWallet = QTableWidget()
        qtwWallet.setColumnCount(5)
        qtwWallet.setHorizontalHeaderLabels(['Label', 'Number', 'Rate',
                                             'Wished Ratio', 'Real Ratio'])
        for etf in wallet.etfList:
            index = wallet.etfList.index(etf)
            qtwWallet.insertRow(index)
            QTableWidget()
            qtwWallet.setItem(index, 0, QTableWidgetItem(etf.label))
            qtwWallet.setItem(index, 1, QTableWidgetItem(str(etf.number)))
            qtwWallet.setItem(index, 2, QTableWidgetItem(str(etf.rate)))
            qtwWallet.setItem(index, 3, QTableWidgetItem(str(etf.wishedRatio)))
            qtwWallet.setItem(index, 4, QTableWidgetItem(str(etf.realRatio)))

        qtwWallet.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        qtwWallet.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        qtwWallet.resizeColumnsToContents()
        qtwWallet.resizeRowsToContents()
        qtwWallet.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        return qtwWallet


if __name__ == '__main__':
    app = QApplication(sys.argv)

    binckWallet = EtfBalance.Wallet("Binck wallet")
    balancedWallet = binckWallet.balance(0.9)

    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel(binckWallet.name))
    layout.addWidget(View.buildQTableWidget(binckWallet))
    layout.addWidget(QLabel(balancedWallet.name))
    layout.addWidget(View.buildQTableWidget(balancedWallet))
    layout.addWidget(QPushButton('Balanced'))
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())
