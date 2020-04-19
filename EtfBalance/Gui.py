#!/usr/bin/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
QLabel, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHBoxLayout,\
    QLineEdit, QTableView
from PyQt5 import QtCore
import sys
import EtfBalance


""" VIEW """
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.originalWallet = EtfBalance.Wallet("Binck wallet")
        self.balancedWallet = self.originalWallet.balance(0.9)
        self.initUi()

    def initUi(self):
        """ Creation of the GUI """
        self.setWindowTitle("Etf Balance")
        self.windowLayout = QVBoxLayout()

        # Original Wallet
        self.originalWalletModel = WalletTableModel(self.originalWallet)
        self.originaltableview = QTableView()
        self.originaltableview.setModel(self.originalWalletModel)
        self.originaltableview.resizeColumnsToContents()
        self.originaltableview.resizeRowsToContents()
        self.originaltableview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.windowLayout.addWidget(self.originaltableview)

        # Balanced Wallet
        self.balancedWalletModel = WalletTableModel(self.balancedWallet)
        self.balancedtableview = QTableView()
        self.balancedtableview.setModel(self.balancedWalletModel)
        self.balancedtableview.resizeColumnsToContents()
        self.balancedtableview.resizeRowsToContents()
        self.balancedtableview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.windowLayout.addWidget(self.balancedtableview)

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

    @QtCore.pyqtSlot()
    def balanceButtonClicked(self):
        # TODO : from QTableWidget to EtfBalance.Wallet
        print("%s " % self.originalWallet.etfList[0][1])


""" Wallet model class """
class WalletTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.datain = data
        print('Data : {0}'.format(data))

    def rowCount(self, parent=QtCore.QModelIndex()):
        print("rowCount: %s " % len(self.datain.etfList))
        return len(self.datain.etfList)

    def columnCount(self, parent=QtCore.QModelIndex()):
        # TODO hardcoded 5 val
        print("columnCount: %s " % 5)
        return 5

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ("Label", "Number", "Rate", "Wished Ratio", "Real Ratio")[section]
        else:
            return "{}".format(section)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            print('{0}'.format(self.datain.etfList[i][j]))
            return '{0}'.format(self.datain.etfList[i][j])
        else:
            return QtCore.QVariant()


""" MAIN """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Widget()
    window.show()
    sys.exit(app.exec_())
