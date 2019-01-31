class Etf:
    
    def __init__(self, label, number, rate):
        self.label = label
        self.number = number
        self.rate = rate
        
    def computeVal(self):
        return self.number * self.rate
        
        
        
class Wallet:
    def __init__(self, etfList):
        self.etfList=etfList