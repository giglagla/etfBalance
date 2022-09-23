#!/usr/bin/env python3.7

from copy import deepcopy
import sys
import stockexchange
import asyncio


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

    def __init__(self, label, number, price, wishedRatio):
        self.label = label
        self.number = number
        self.price = price
        self.realRatio = 0
        self.wishedRatio = wishedRatio

    def __repr__(self):
        return "<Etf label:'%s'\t number:%s\t price:%s\t wishedRatio:%s\t realRatio:%s>" % \
            (self.label, self.number, self.price, self.wishedRatio, self.realRatio)

    def __eq__(self, other):
        return (self.label == self.label
                and self.number == other.number
                and self.price == other.price
                and self.wishedRatio == other.wishedRatio
                and self.realRatio == other.realRatio)

    def __hash__(self):
        return hash((self.label, self.number, self.price, self.wishedRatio,
                     self.realRatio))

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        yield self.label
        yield self.number
        yield self.price
        yield self.realRatio
        yield self.wishedRatio

    def __getitem__(self, key):
        etfElems = list(self)
        return etfElems[key]

    def __setitem__(self, key, value):
        attrName = list(self.__dict__.keys())[key]
        setattr(self, attrName, value)

    def value(self):
        return float(self.number) * float(self.price)


class Wallet:
    def __init__(self, name):
        self.ratioPrecision = 0.9
        self.name = name
        paaem, ese, etz, ptpxe, paasi, rs2k = asyncio.run(
            stockexchange.currentPrice('PAEEM.PA',
                                       'ESE.PA',
                                       'ETZ.PA',
                                       'PTPXE.PA',
                                       'PAASI.PA',
                                       'RS2K.PA'))
        self.etfList = [Etf('Amundi ETF PEA MSCI Emg Markets', 7, paaem, 0.12), # WW Emg
                        Etf('BNP Easy S&P 500', 36, ese, 0.45),                 # US
                        Etf('BNP Paribas Easy Stoxx Europe 600', 25, etz, 0.1), # Europe
                        Etf('Amundi ETF PEA Japan TOPIX', 6, ptpxe, 0.08),       # Japan
                        Etf('Amundi MSCI EM ASIA', 5, paasi, 0.1),              # Asia
                        Etf('Amundi ETF Russel 2000', 1, rs2k, 0.15)]           # US small
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

    def balance(self, newWalletName="Balanced Wallet", ratioPrecision=0.9):
        """ Balance the wallet with a given precision,
        in order to reach the wished ratio for each etf"""
        if ratioPrecision >= 1:
            ratioPrecision = 1
        lastBalancedWallet = Wallet("")
        walletToBalance = deepcopy(self)
        walletToBalance.name = newWalletName
        walletToBalance.ratioPrecision = ratioPrecision

        while(lastBalancedWallet != walletToBalance):
            for elem in walletToBalance.etfList:
                walletToBalance.computeEtfRatio()
                while (elem.realRatio < float(elem.wishedRatio * ratioPrecision)):
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
            elem.number = elem.number / pgcdFound

        """ Reduce Etf numbers """
        while (self.totalAmount() < minVal):
            for elem in self.etfList:
                elem.number += pgcdFound


""" for test purpose only """
if __name__ == '__main__':
    binckWallet = Wallet("Binck wallet")
    print("%s:\n%s" % (binckWallet.name, binckWallet))
    print("Total Wallet: %s" % binckWallet.totalAmount())

    balancedWallet = binckWallet.balance(0.9)
    print("%s:\n%s" % (balancedWallet.name, balancedWallet))
    print("Total Wallet: %s" % balancedWallet.totalAmount())

    sys.exit()
