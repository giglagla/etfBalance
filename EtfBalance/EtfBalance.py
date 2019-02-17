#!/usr/bin/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
    QLabel, QTableWidget,QTableWidgetItem
from copy import deepcopy
import sys


def pgcd(*n):
    """Calcul du 'Plus Grand Commun Diviseur' de n (>=2) valeurs entières (Euclide)"""

    def _pgcd(a, b):
        while b: a, b = b, a % b
        return a

    p = _pgcd(n[0], n[1])
    for x in n[2:]:
        p = _pgcd(p, x)
    return p


class Etf:

    def __init__(self, label, number, rate, wishedRatio):
        self.label = label
        self.number = number
        self.rate = rate
        self.wishedRatio = wishedRatio
        self.realRatio = 0
        
    def __repr__(self):
        return "<Etf label:'%s'\t number:%s\t rate:%s\t wishedRatio:%s\t realRatio:%s>" % (self.label, self.number, self.rate, self.wishedRatio, self.realRatio)
        
    def __eq__(self, other):
            return (self.label == self.label
                    and self.number == other.number
                    and self.rate == other.rate 
                    and self.wishedRatio == other.wishedRatio
                    and self.realRatio == other.realRatio)
            
    def __hash__(self):
        return hash((self.label, self.number, self.rate, self.wishedRatio, self.realRatio))
    
    def __ne__(self, other):
        return not self == other
        
    def value(self):
        return self.number * self.rate
        
        
class Wallet:
        
    def __init__(self, etfList=[]):
        self.etfList = etfList
        self.computeEtfRatio()
        
    def __repr__(self):
        return ('[%s]' % ',\n '.join(map(str, self.etfList)))
    
    def __eq__(self, other):
        return self.etfList == other.etfList
        
    def __ne__(self, other):         
        return not self == other
    
    def computeEtfRatio(self):
        for elem in self.etfList:
            elem.realRatio = round(elem.value() / self.total(), 2)
            
    def total(self):
        total = 0
        for elem in self.etfList:
            total += elem.value()
        return total

   
class WalletManager:

    def __init__(self, originalWallet):
        self.originalWallet = originalWallet
        self.balancedWallet = originalWallet
 
    def balanceWallet(self, ratioPrecision=1): 
        lastBalancedWallet = self.originalWallet
        newBalancedWallet = deepcopy(self.originalWallet)
    
        while(lastBalancedWallet != newBalancedWallet):
            lastBalancedWallet = deepcopy(newBalancedWallet)
            
            for elem in newBalancedWallet.etfList:
                newBalancedWallet.computeEtfRatio()
                while (elem.realRatio < (elem.wishedRatio * ratioPrecision)):
                    elem.number += 1
                    newBalancedWallet.computeEtfRatio()  
           
            #print("balancedWallet : \n%s" % newBalancedWallet)
        self.reduceWallet(newBalancedWallet)
        self.balancedWallet = newBalancedWallet
        return self.balancedWallet
 
    def reduceWallet(self, walletToReduce):
        test = []
        for elem in walletToReduce.etfList:
            test.append(elem.number)
        
        pgcdFounded = pgcd(*test)
        
        for elem in walletToReduce.etfList:
            elem.number = int(elem.number / pgcdFounded)
            
        while ( walletToReduce.total() > self.originalWallet.total() ):
            for elem in walletToReduce.etfList:
                elem.number += pgcdFounded
    
  
            
if __name__ == '__main__':
    etfList = []
    etfList.append(Etf('Amundi ETF MSCI Emg Markets', 5, 4.05, 0.2))
    etfList.append(Etf('BNP Easy S&P 500', 8, 11.22, 0.6))
    #etfList.append(Etf('SPDR MSCI Europe Small Cp Value Weighted', 1, 32.70, 0.2))    
    etfList.append(Etf('Vanguard FTSE Developed Europe', 2, 29.00, 0.2))
    binckWallet = Wallet(etfList)
    
    print("Binck wallet:\n%s" % binckWallet)
    print("Total Wallet: %s" % binckWallet.total())
    
    wm = WalletManager(binckWallet)
    balancedWallet = wm.balanceWallet(0.8)
    print("\nBalanced wallet:\n%s" % balancedWallet)
    print("Total Wallet: %s" % balancedWallet.total())  
    
    
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    
    label1 = QLabel("Binck Wallet:")
    
    # Binck Wallet
    tableWidget = QTableWidget()
    tableWidget.setColumnCount(5)
    tableWidget.setHorizontalHeaderLabels(['Label', 'Number', 'Rate', 'Wished Ratio', 'Real Ratio'])
    for etf in binckWallet.etfList:
        index = binckWallet.etfList.index(etf)
        tableWidget.insertRow(index)
        QTableWidgetItem()
        tableWidget.setItem(index, 0, QTableWidgetItem(etf.label))
        tableWidget.setItem(index, 1, QTableWidgetItem(str(etf.number)))
        tableWidget.setItem(index, 2, QTableWidgetItem(str(etf.rate)))
        tableWidget.setItem(index, 3, QTableWidgetItem(str(etf.wishedRatio)))
        tableWidget.setItem(index, 4, QTableWidgetItem(str(etf.realRatio)))
    tableWidget.resizeColumnsToContents()
    tableWidget.resizeRowsToContents()
    
    layout.addWidget(label1)
    layout.addWidget(tableWidget)
    layout.addWidget(QPushButton('Bottom'))
    
    window.setLayout(layout)

    window.show()
    app.exec_()
    
