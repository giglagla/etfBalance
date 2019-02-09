#!/usr/bin/python

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
    QLabel
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
        
 
def balanceWallet(wallet, ratioPrecision=1): 
    lastBalancedWallet = Wallet()
    newBalancedWallet = deepcopy(wallet)

    while(lastBalancedWallet != newBalancedWallet):
        lastBalancedWallet = deepcopy(newBalancedWallet)
        
        for elem in newBalancedWallet.etfList:
            newBalancedWallet.computeEtfRatio()
            while (elem.realRatio < (elem.wishedRatio * ratioPrecision)):
                elem.number += 1
                newBalancedWallet.computeEtfRatio()  
       
        #print("balancedWallet : \n%s" % newBalancedWallet)
    reduceWallet(newBalancedWallet, wallet)
    return newBalancedWallet
 
 
def reduceWallet(walletToReduce, initialWallet):
    test = []
    for elem in walletToReduce.etfList:
        test.append(elem.number)
    
    pgcdFounded = pgcd(*test)
    
    for elem in walletToReduce.etfList:
        elem.number = int(elem.number / pgcdFounded)
        
    while ( walletToReduce.total() < initialWallet.total() ):
        for elem in walletToReduce.etfList:
            elem.number += pgcdFounded
    
  
            
if __name__ == '__main__':
    etfList = []
    etfList.append(Etf('Amundi ETF MSCI Emg Markets UCITS EUR C', 5, 4.01, 0.25))
    etfList.append(Etf('BNP Easy S&P 500 UCITS ETF EUR -C-', 8, 10.88, 0.25))
    etfList.append(Etf('SPDR MSCI Europe Small Cp Value Weighted', 1, 32.10, 0.50))               
    binckWallet = Wallet(etfList)
    
    print("Binck wallet:\n%s" % binckWallet)
    print("Total Wallet: %s" % binckWallet.total())
    
    balancedWallet = balanceWallet(binckWallet, 0.6)
    print("\nBalanced wallet:\n%s" % balancedWallet)
    print("Total Wallet: %s" % balancedWallet.total())  
    
    '''
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    
    label1 = QLabel()
    label1.setText(str(binckWallet))
    layout.addWidget(label1)
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()
    app.exec_()
    '''
