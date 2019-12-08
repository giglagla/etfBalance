#!/usr/bin/python

from copy import deepcopy
import sys


def pgcd(*n):
    """Calcul du 'Plus Grand Commun Diviseur' de n (>=2) valeurs entières"""

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
        return "<Etf label:'%s'\t number:%s\t rate:%s\t wishedRatio:%s\t realRatio:%s>" % \
            (self.label, self.number, self.rate, self.wishedRatio, self.realRatio)

    def __eq__(self, other):
        return (self.label == self.label
                and self.number == other.number
                and self.rate == other.rate
                and self.wishedRatio == other.wishedRatio
                and self.realRatio == other.realRatio)

    def __hash__(self):
        return hash((self.label, self.number, self.rate, self.wishedRatio,
                     self.realRatio))

    def __ne__(self, other):
        return not self == other

    def value(self):
        return self.number * self.rate


class Wallet:
    def __init__(self, name):
        self.ratioPrecision = 0.9
        self.name = name
        self.etfList = [Etf('Amundi ETF MSCI Emg Markets', 1, 19.979, 0.2),
                        Etf('BNP Easy S&P 500', 8, 13.3035, 0.6),
                        Etf('Vanguard FTSE Developed Europe', 1, 31.988, 0.2)]
        self.computeEtfRatio()

    def __repr__(self):
        return ('[%s]' % ',\n '.join(map(str, self.etfList)))

    def __eq__(self, other):
        return (self.etfList == other.etfList
                and self.name == other.name)

    def __ne__(self, other):
        return not self == other

    def computeEtfRatio(self):
        """ Compute each Etf ratio inside this wallet"""
        for elem in self.etfList:
            elem.realRatio = round(elem.value() / self.totalAmount(), 2)

    def totalAmount(self):
        """ Compute the total wallet amount """
        total = 0
        for elem in self.etfList:
            total += elem.value()
        return total

    def balance(self, ratioPrecision=0.9):
        """ Balance the wallet with a given precision,
        in order to reach the wished ratio for each etf"""
        lastBalancedWallet = Wallet("")
        walletToBalance = deepcopy(self)
        walletToBalance.name = "Balanced wallet"
        walletToBalance.ratioPrecision = ratioPrecision

        while(lastBalancedWallet != walletToBalance):
            for elem in walletToBalance.etfList:
                walletToBalance.computeEtfRatio()
                while (elem.realRatio < (elem.wishedRatio * ratioPrecision)):
                    elem.number += 1
                    walletToBalance.computeEtfRatio()
            lastBalancedWallet = deepcopy(walletToBalance)

        walletToBalance.reduce(self.totalAmount())
        return walletToBalance

    def reduce(self, minVal):
        """ Try to reduce the wallet, keeping the etf ratio untouched """
        etfNumbers = []
        for elem in self.etfList:
            etfNumbers.append(elem.number)

        pgcdFound = pgcd(*etfNumbers)

        """ Set Etf numbers to PGCD """
        for elem in self.etfList:
            elem.number = int(elem.number / pgcdFound)

        """ Reduce Etf numbers """
        while (self.totalAmount() < minVal):
            for elem in self.etfList:
                elem.number += pgcdFound


if __name__ == '__main__':

    binckWallet = Wallet("Binck wallet")
    print("%s:\n%s" % (binckWallet.name, binckWallet))
    print("Total Wallet: %s" % binckWallet.totalAmount())

    balancedWallet = binckWallet.balance(0.9)
    print("%s:\n%s" % (balancedWallet.name, balancedWallet))
    print("Total Wallet: %s" % balancedWallet.totalAmount())

    sys.exit()
