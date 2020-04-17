#!/usr/bin/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
    QLabel, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHBoxLayout,\
    QLineEdit
from PyQt5 import QtCore
import sys
import EtfBalance


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etf Balance")
        self.windowLayout = QVBoxLayout()
        self.originalWallet = EtfBalance.Wallet("Binck wallet")
        self.balancedWallet = self.originalWallet.balance(0.9)
        self.QWOriginalWallet = self.buildQTableWidget(self.originalWallet)
        self.QWBalancedWallet = self.buildQTableWidget(self.balancedWallet)
        self.initUi()

    def initUi(self):
        # Original Wallet
        self.windowLayout.addWidget(QLabel(self.originalWallet.name))
        self.windowLayout.addWidget(self.QWOriginalWallet)

        # Balanced Wallet
        self.windowLayout.addWidget(QLabel(self.balancedWallet.name))
        self.windowLayout.addWidget(self.QWBalancedWallet)

        # Precision
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Precision:"))
        hlayout.addWidget(QLineEdit("{}".format(self.balancedWallet.ratioPrecision)))
        hlayout.addStretch()
        self.windowLayout.addLayout(hlayout)

        # Button
        balanceButton = QPushButton('Balanced', self)
        balanceButton.clicked.connect(self.balanceButtonClicked)
        self.windowLayout.addWidget(balanceButton)

        self.setLayout(self.windowLayout)
        self.show()

    @QtCore.pyqtSlot()
    def balanceButtonClicked(self):
        print('prout')
        self.QWOriginalWallet = self.buildQTableWidget(self.balancedWallet)

    def buildQTableWidget(self, wallet):
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
    window = MainWindow()
    sys.exit(app.exec_())
