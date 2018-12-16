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
import csv
import time
import logging
import datetime as dt


'''
This file is set up in three parts: 

* The tws classes (which are what we actually used to place orders and connect to TWS/IB Gateway 

* The 

*


'''


# Setting up the default log location for the api to write to
logging.basicConfig(filename="logs/Log_Main.log", level=logging.INFO)

# This is what we use to connect and interact with IB
'''
This is the basic TWS class. It doesn't have anything extra to it except that I put some examples of how to override the
default wrapper functions to do more specific tasks. In this case, it is writing certain results to csv files. 

'''
class TWS(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    #Note: All of these are wrapper functions to read the tws packets and print their values

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        print("Acct Summary. ReqId:", reqId, "Acct:", account,
              "Tag: ", tag, "Value:", value, "Currency:", currency)

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. Req Id: ", reqId)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency,
              "Position:", position, "Avg cost:", avgCost)

    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")

    def positionMulti(self, reqId: int, account: str, modelCode: str,
                      contract: Contract, pos: float, avgCost: float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)
        print("Position Multi. Request:", reqId, "Account:", account,
              "ModelCode:", modelCode, "Symbol:", contract.symbol, "SecType:",
              contract.secType, "Currency:", contract.currency, ",Position:",
              pos, "AvgCost:", avgCost)

    def positionMultiEnd(self, reqId: int):
        super().positionMultiEnd(reqId)
        print("Position Multi End. Request:", reqId)



''' 
This TWS Class is one that appends account and position info to lists that are built into the class for easy retrieval. 

Examples of how this class is used is in the Example_API_Uses Class. 

'''
class TWSNEW(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        # self.account = 'DU110641'
        self.positions = []
        self.account_info = []

    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)

        self.account_info.append([account, tag, value, currency])

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)

        self.positions.append([account, contract.symbol, contract.secType, position, avgCost])

    def positionMulti(self, reqId: int, account: str, modelCode: str, contract: Contract, pos: float, avgCost: float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)

        self.positions.append([account, contract.symbol, contract.secType, pos, avgCost, contract.conId])


# End of TWS Classes ---------------------------------------------------------------------------------------------------



# The old methods for TWSINFO ------------------------------------------------------------------------------------------
def updateIBInfo():
    #Emptying the old data
    open('csv/positions.csv', 'w').close()
    open('csv/PortfolioInformation.csv', 'w').close()

    try:
        tws = TWSINFO()
        tws.connect('127.0.0.1', 7497, 100)
        tws.startApi()
        tws.reqPositionsMulti(5, 'DU1140641', '')
        # tws.reqAccountSummary(9002, "All", AccountSummaryTags.AllTags)
        tags = ",".join((AccountSummaryTags.AccountType, AccountSummaryTags.BuyingPower, AccountSummaryTags.TotalCashValue))
        tws.reqAccountSummary(9004, 'All', tags=tags)
        tws.run()
    finally:
        tws.disconnect()

def updateIBInfoMulti(client_id):
    #Emptying the old data
    open('csv/positions.csv', 'w').close()
    open('csv/PortfolioInformation.csv', 'w').close()

    try:
        tws = TWSINFO()
        tws.connect('127.0.0.1', 7497, client_id)
        tws.startApi()
        # tws.reqAccountSummary(9002, "All", AccountSummaryTags.AllTags)
        # tags = ",".join((AccountSummaryTags.AccountType, AccountSummaryTags.BuyingPower, AccountSummaryTags.TotalCashValue, AccountSummaryTags.NetLiquidation))
        tag = AccountSummaryTags.NetLiquidation
        tws.reqAccountSummary(9004, 'All', tags=tag)
        tws.reqPositionsMulti(5, 'DU1140641', '')
        tws.run()
    finally:
        tws.disconnect()

def updatePositions(client_id):
    #Emptying the old data
    open('csv/positions.csv', 'w').close()

    try:
        tws = TWSINFO()
        tws.connect('127.0.0.1', 7497, client_id)
        tws.startApi()
        tws.reqPositionsMulti(5, 'DU1140641', '')
        tws.run()

    finally:
        if tws.isConnected():
            tws.disconnect()

def update_net_liquidation(client_id):
    #Emptying the old data
    open('csv/PortfolioInformation.csv', 'w').close()

    try:
        tws = TWSINFO()
        tws.connect('127.0.0.1', 7497, client_id)
        tws.startApi()
        tag = AccountSummaryTags.NetLiquidation
        tws.reqAccountSummary(9004, 'All', tags=tag)
        tws.run()

    finally:
        if tws.isConnected():
            tws.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

# The new methods for TWSNEW -------------------------------------------------------------------------------------------
def get_positions(client_id):
    tws = TWSNEW()
    tws.connect('127.0.0.1', 7497, client_id)
    tws.startApi()
    # tws.reqAccountSummary(9002, "All", AccountSummaryTags.AllTags)
    # tags = ",".join((AccountSummaryTags.AccountType, AccountSummaryTags.BuyingPower, AccountSummaryTags.TotalCashValue, AccountSummaryTags.NetLiquidation))
    tws.reqPositionsMulti(5, 'DU1140641', '')
    tws.run()
    tws.disconnect()

    return tws.positions

def get_portfolio_info(client_id):
    tws = TWSNEW()
    tws.connect('127.0.0.1', 7497, client_id)
    tws.startApi()

    # tags = ",".join((AccountSummaryTags.AccountType, AccountSummaryTags.BuyingPower, AccountSummaryTags.TotalCashValue, AccountSummaryTags.NetLiquidation))
    tag = AccountSummaryTags.NetLiquidation
    tws.reqAccountSummary(9004, 'All', tags=tag)

    tws.run()
    tws.disconnect()

    return tws.account_info

# ----------------------------------------------------------------------------------------------------------------------

# Simple read and write text file to get the next orderID that we need
def getNextOrderId():
    file = open('txt/lastOrder.txt', 'r')
    nextOrder = int(file.read()) + 1
    file.close()
    overwrite = open('txt/lastOrder.txt', 'w')
    overwrite.write(str(nextOrder))
    overwrite.close()
    return nextOrder


# This is an example of how our parameters should look
# symbol = "IBKR"
# sec_type = "STK"
# currency = "USD"
# exchange = "SMART"
def create_contract(stock_symbol, sec_type, currency, exchange):
    contract = Contract()
    contract.symbol = stock_symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract

# This is an example of how our parameters should look
# action = "BUY"
# order_type = "MKT"
# quantity = "100"
def create_base_order(action,order_type, quantity):
    order = Order()
    order.action = action
    order.orderType = order_type
    order.totalQuantity = quantity
    return order

def create_adaptive_order(action, order_type, quantity):
    order = Order()
    order.action = action 
    order.orderType = order_type
    order.totalQuantity = quantity
    order.algoStrategy = "Adaptive"
    order.algoParams = []
    order.algoParams.append(TagValue("adaptivePriority", "Normal"))
    return order

def trailing_stop_order(action, quantity, trailingPercent, trailStopPrice):
    order = Order()
    order.action = action
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.trailingPercent = trailingPercent
    order.trailStopPrice = trailStopPrice
    return order


# -- | Place Trailing Stop Order | --

def TRAIL(action, quantity, trailingPercent, trailStopPrice):
    order = Order()
    order.action = action
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.trailingPercent = trailingPercent
    order.trailStopPrice = trailStopPrice
    return order



def MIT(action, quantity, price):
    order = Order()
    order.Action = action
    order.OrderType = "MIT"
    order.TotalQuantity = quantity
    order.AuxPrice = price
    return order


def STP_LMT(action, quantity, limit_price, stop_price):
    order = Order()
    order.action = action
    order.orderType = "STP LMT"
    order.totalQuantity = quantity
    order.lmtPrice = limit_price
    order.auxPrice = stop_price
    return order


def BracketOrder(parentOrderId: int, action: str, quantity: float, limitPrice: float,
                 takeProfitLimitPrice: float, stopLossPrice: float):
    # This will be our main or "parent" order
    parent = Order()
    parent.orderId = parentOrderId
    parent.action = action

    parent.orderType = "LMT"
    parent.totalQuantity = quantity
    parent.lmtPrice = limitPrice
    # The parent and children orders will need this attribute set to False to prevent accidental executions.
    # The LAST CHILD will have it set to True,
    parent.transmit = False

    takeProfit = Order()
    takeProfit.orderId = parent.orderId + 1
    takeProfit.action = "SELL" if action == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = takeProfitLimitPrice
    takeProfit.parentId = parentOrderId
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.orderId = parent.orderId + 2
    stopLoss.action = "SELL" if action == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    # Stop trigger price
    stopLoss.auxPrice = stopLossPrice
    stopLoss.totalQuantity = quantity
    stopLoss.parentId = parentOrderId
    # In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True
    # to activate all its predecessors
    stopLoss.transmit = True

    bracketOrder = [parent, takeProfit, stopLoss]
    return bracketOrder



def Bracket_With_Time(parentOrderId: int, action: str, quantity: float, limitPrice: float,
                 takeProfitLimitPrice: float, stopLossPrice: float, cancel_time: str, exit_time: str):
    # This will be our main or "parent" order
    parent = Order()
    parent.orderId = parentOrderId
    parent.action = action

    parent.orderType = "LMT"
    parent.totalQuantity = quantity
    parent.lmtPrice = limitPrice
    # The parent and children orders will need this attribute set to False to prevent accidental executions.
    # The LAST CHILD will have it set to True

    # The new stuff I added
    parent.tif = "GTD"
    parent.goodTillDate = cancel_time

    parent.transmit = False

    takeProfit = Order()
    takeProfit.orderId = parent.orderId + 1
    takeProfit.action = "SELL" if action == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = takeProfitLimitPrice
    takeProfit.parentId = parentOrderId
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.orderId = parent.orderId + 2
    stopLoss.action = "SELL" if action == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    # Stop trigger price
    stopLoss.auxPrice = stopLossPrice
    stopLoss.totalQuantity = quantity
    stopLoss.parentId = parentOrderId
    # In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True
    # to activate all its predecessors
    stopLoss.transmit = False

    timeOrder = Order()
    timeOrder.orderId = parent.orderId + 3
    timeOrder.goodAfterTime = exit_time
    timeOrder.action = "SELL" if action == "BUY" else "BUY"
    timeOrder.totalQuantity = quantity
    timeOrder.orderType = "MKT"
    timeOrder.parentId = parentOrderId
    timeOrder.transmit = True

    bracketOrder = [parent, takeProfit, stopLoss, timeOrder]
    return bracketOrder








