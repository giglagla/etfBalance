#!/usr/bin/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
QLabel, QAbstractScrollArea, QHBoxLayout, QLineEdit, QTableView, QSizePolicy, \
QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot
from PyQt5.QtGui import QFont
import qdarkstyle
import sys
import EtfBalance



class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.originalWallet = EtfBalance.Wallet("Binck wallet")
        self.balancedWallet = self.originalWallet.balance(0.9)
        self.initUi()

    def initUi(self):
        """ GUI initialization """
        self.setWindowTitle("ETF Wallet Balancer")
        self.windowLayout = QVBoxLayout()

        # Original Wallet
        self.originalWalletWidget = WalletView(self.originalWallet)
        self.windowLayout.addWidget(self.originalWalletWidget)
        total = self.originalWalletWidget.model.wallet.totalAmount()

        # Precision + Balance
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Precision:"))
        self.ratioPrecisionWidget = QLineEdit("{}".format(self.balancedWallet.ratioPrecision))
        hlayout.addWidget(self.ratioPrecisionWidget)
        #hlayout.addWidget(QLabel("[0.0;1.0]"))

        balanceButton = QPushButton('Balanced', self)
        balanceButton.clicked.connect(self.balanceButtonClicked)
        hlayout.addWidget(balanceButton)
        #hlayout.addStretch()
        self.windowLayout.addLayout(hlayout)

        # Balanced Wallet
        self.balancedWalletWidget = WalletView(self.balancedWallet)
        self.balancedWalletWidget.view.setEditTriggers(QAbstractItemView.NoEditTriggers);
        self.windowLayout.addWidget(self.balancedWalletWidget)


        self.setLayout(self.windowLayout)

    @pyqtSlot()
    def balanceButtonClicked(self):
        newPrecision = float(self.ratioPrecisionWidget.text())
        self.balancedWallet = self.originalWallet.balance(newPrecision)
        self.balancedWalletWidget.view.setModel(WalletModel(self.balancedWallet))
        self.balancedWalletWidget.updateWalletValue()


class WalletView(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        self.model = WalletModel(data)
        self.model.dataChanged.connect(self.updateWalletValue)

        # Creating a QTableView
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.name = QLabel(self.model.wallet.name)

        self.totalAmount = QLabel("Wallet value: %.2f €" % self.model.wallet.totalAmount())

        # QWidget Layout
        self.mainlayout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setVerticalStretch(1)
        self.view.setSizePolicy(size)

        self.mainlayout.addWidget(self.name)
        self.mainlayout.addWidget(self.view)
        self.mainlayout.addWidget(self.totalAmount)

        # Set the layout to the QWidget
        self.setLayout(self.mainlayout)

    @pyqtSlot()
    def updateWalletValue(self):
        currentSelectedModel = self.view.selectionModel().model()
        self.totalAmount.setText("Wallet value: %.2f €" % currentSelectedModel.wallet.totalAmount())


class WalletModel(QAbstractTableModel):
    def __init__(self, wallet=None):
        QAbstractTableModel.__init__(self)
        self.wallet = wallet
        self.headerLabels = ["Label", "Number", "Rate", "Wished Ratio", "Real Ratio"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.wallet.etfList)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headerLabels)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headerLabels[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row, column = index.row(), index.column()
            value = self.wallet.etfList[row][column]

            # Perform per-type checks and render accordingly.
            if isinstance(value, float):
                return "%.2f" % value
            if isinstance(value, int):
                return "%d" % value
            if isinstance(value, str):
                return "%s" % value
        else:
            return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            row, column = index.row(), index.column()
            self.wallet.etfList[row][column] = type(self.wallet.etfList[row][column])(value)
            self.dataChanged.emit(index, index, [])
            return True
        else:
            return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled


""" MAIN """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setFont(QFont("Arial", 9, 60))
    window = Widget()
    window.show()
    sys.exit(app.exec_())
