#!/usr/bin/env python3.7

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
     QLabel, QAbstractScrollArea, QHBoxLayout, QLineEdit, QTableView,  \
     QSizePolicy, QAbstractItemView, QMainWindow, QHeaderView, QSpacerItem
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSlot
import qdarkstyle
import sys
import etfwallet


class CentralWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.originalWallet = etfwallet.Wallet("Original Wallet")
        self.balancedWallet = self.originalWallet.balance(ratioPrecision=0.9)
        self.initUi()

    def initUi(self):
        """ GUI initialization """
        self.setWindowTitle("ETF Wallet Balancer")

        # Original Wallet
        self.originalWalletWidget = WalletView(self.originalWallet)
        # Precision
        self.lPrecision = QLabel("Precision:")
        self.ratioPrecisionWidget = QLineEdit("{}".format(self.balancedWallet.ratioPrecision))
        # Balance button
        self.balanceButton = QPushButton('Balance', self)
        self.balanceButton.clicked.connect(self.balanceButtonClicked)
        # Reset button
        self.resetButton = QPushButton('Reset', self)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        # Balanced Wallet
        self.balancedWalletWidget = WalletView(self.balancedWallet)
        self.balancedWalletWidget.view.setEditTriggers(QAbstractItemView.NoEditTriggers);

        # Layouts
        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.originalWalletWidget)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.lPrecision)
        hlayout.addWidget(self.ratioPrecisionWidget)
        hlayout.addStretch()
        hlayout.addWidget(self.balanceButton)
        hlayout.addWidget(self.resetButton)
        self.windowLayout.addLayout(hlayout)
        self.windowLayout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Expanding))
        self.windowLayout.addWidget(self.balancedWalletWidget)
        self.setLayout(self.windowLayout)

    @pyqtSlot()
    def resetButtonClicked(self):
        self.originalWallet = etfwallet.Wallet("Original Wallet")
        self.originalWalletWidget.view.setModel(WalletModel(self.originalWallet))
        self.originalWalletWidget.updateWalletValue()
        return

    @pyqtSlot()
    def balanceButtonClicked(self):
        newPrecision = float(self.ratioPrecisionWidget.text())
        self.balancedWallet = self.originalWallet.balance(ratioPrecision=newPrecision)
        self.balancedWalletWidget.view.setModel(WalletModel(self.balancedWallet))
        self.balancedWalletWidget.updateWalletValue()


class WalletView(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        self.model = WalletModel(data)
        self.model.dataChanged.connect(self.updateWalletValue)

        # Wallet Name
        self.name = QLabel(self.model.wallet.name, self)
        self.name.setStyleSheet("font: 20px arial;")

        # QTableView
        self.view = QTableView(self)
        self.view.setModel(self.model)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.verticalHeader().hide()
        self.view.resizeRowsToContents()
        self.view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.view.resizeColumnsToContents()
        self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Total Value
        self.totalAmount = QLabel("Value: %.2f €" % self.model.wallet.totalAmount(), self)
        self.totalAmount.setStyleSheet("color: #00909e; font-size: 14px")

        # Widget layout
        self.mainlayout = QVBoxLayout(self)
        self.mainlayout.addWidget(self.name)
        self.mainlayout.addWidget(self.view)
        self.mainlayout.addWidget(self.totalAmount)
        self.setLayout(self.mainlayout)

    @pyqtSlot()
    def updateWalletValue(self):
        currentSelectedModel = self.view.selectionModel().model()
        self.totalAmount.setText("Value: %.2f €" % currentSelectedModel.wallet.totalAmount())


class WalletModel(QAbstractTableModel):
    def __init__(self, wallet=None):
        QAbstractTableModel.__init__(self)
        self.wallet = wallet
        self.headerLabels = ["Label", "Nb", "Price", "Weight", "Wished weight"]

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


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("ETF Wallet Balancer")
        self.setCentralWidget(widget)
        self.setStyleSheet("color: #dae1e7; font-size:13px")


if __name__ == '__main__':
    # Qt Application
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    # QWidget
    widget = CentralWidget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.show()

    # Execute application
    sys.exit(app.exec_())
