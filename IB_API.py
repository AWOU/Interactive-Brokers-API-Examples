from ibapi.contract import *
from ibapi.order import *
from ibapi.tag_value import TagValue
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.account_summary_tags import *
from ibapi.common import *
from ibapi.contract import Contract
from ibapi.order import Order
import ibapi.ticktype as TickType
import ibapi.order_state as OrderState
import logging

#logging.basicConfig(filename="logs/IBAPI.log", level=logging.INFO)

# The new and most efficient tws class
class TWS(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        # self.account = 'DU110641'
        self.positions = []
        self.account_info = []

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency) # Since this function is here to override the
        # original accountSummary function, we call super() first with the same values for it and then add what we really
        # want it to do under this

        # Just adding it to a list that we can retrieve from the class
        self.account_info.append([account, tag, value, currency])

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)

        self.positions.append([str(account), str(contract.symbol), str(contract.secType), float(position), float(avgCost)])

    def positionMulti(self, reqId: int, account: str, modelCode: str, contract: Contract, pos: float, avgCost: float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)

        self.positions.append([account, contract.symbol, contract.secType, float(pos), float(avgCost), contract.conId])

# End of TWS Classes ---------------------------------------------------------------------------------------------------

# Simple read and write text file to get the next orderID that we need
def getNextOrderId():
    file = open('txt/LastOrder.txt', 'r')
    nextOrder = int(file.read()) + 1
    file.close()
    overwrite = open('txt/LastOrder.txt', 'w')
    overwrite.write(str(nextOrder))
    overwrite.close()
    return nextOrder

