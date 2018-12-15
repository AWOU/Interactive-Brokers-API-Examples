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

import collections
import csv
import time

import logging
import datetime as dt


logging.basicConfig(filename="logs/Log_Main.log", level=logging.INFO)


# This is what we use to connect and interact with IB
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


class TWSINFO(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    # Note: All of these are wrapper functions to read the tws packets and print their values

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        # # 2104 and 2106 are technically not errors but just status updates
        # if errorCode == 2104 or errorCode == 2106:
        #     return

        # # TODO: Test this, it is very important that this is working when we go live
        # if errorCode == 1100:  # If the connection has been lost
        #     count = 0
        #     while self.isConnected() is False and count < 50: # Retrying 100 more times to connect to IB
        #         print("Connection has been lost, trying again ")
        #         time.sleep(10)
        #         # TODO Check this 3rd parameter as it could cause us problems if it is not in sync with the running app
        #         self.connect("127.0.0.1", 7497, 100)
        #         count += 1
        #     return

        """This event is called when there is an error with the
        communication or when TWS wants to send a message to the client."""
        logging.error("ERROR %s %s %s", reqId, errorCode, errorString)


    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)


        data = open('csv/portfolioInformation.csv', 'a', newline='')
        with (data):
            writer = csv.writer(data)
            writer.writerow([account, tag, value, currency])
        #print('Account info written to portfolioInformation.csv')
        data.close()

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. Req Id: ", reqId)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)


        data = open('csv/positions.csv', 'a', newline='')
        with (data):
            writer = csv.writer(data)
            writer.writerow([account, contract.symbol, contract.secType, position, avgCost])
        print('positions written to positions.csv')
        data.close()

    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")

    def positionMulti(self, reqId: int, account: str, modelCode: str, contract: Contract, pos: float, avgCost: float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)

        data = open('csv/positions.csv', 'a', newline='')
        with (data):
            writer = csv.writer(data)
            writer.writerow([account, contract.symbol, contract.secType, pos, avgCost, contract.conId])
        # print('positions Multi written to positions.csv')
        data.close()

    def positionMultiEnd(self, reqId: int):
        super().positionMultiEnd(reqId)
        #print("Position Multi End. Request:", reqId)

    def marketDataType(self, reqId:TickerId, marketDataType:int):
        """TWS sends a marketDataType(type) callback to the API, where
        type is set to Frozen or RealTime, to announce that market data has been
        switched between frozen and real-time. This notification occurs only
        when market data switches between real-time and frozen. The
        marketDataType( ) callback accepts a reqId parameter and is sent per
        every subscription because different contracts can generally trade on a
        different schedule."""

        super().marketDataType(reqId, marketDataType)
        print('ReqID: ', reqId, 'MarketDataTpye: ', marketDataType)


    def tickPrice(self, reqId:TickerId , tickType:TickType, price:float,
                  attrib:TickAttrib):
        """Market data tick price callback. Handles all price related ticks."""

        super().tickPrice(reqId, tickType, price)
        print('ID:', reqId, 'TickType: ', tickType, 'Price: ', price)


    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        """Market data tick size callback. Handles all size-related ticks."""

        super().tickSize(reqId, tickType, size)
        print('ReqID: ', reqId, 'TickType: ', tickType, 'Size: ', size)


    def tickSnapshotEnd(self, reqId:int):
        """When requesting market data snapshots, this market will indicate the
        snapshot reception is finished. """

        super().tickSnapshotEnd(reqId)
        print('Snapshot with ID ', reqId, ' ended')


    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):

        super().tickGeneric(reqId,tickType, value)
        print('ID: ', reqId, 'tickTpye: ', tickType, 'Valeu: ', value)


    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        super().tickString(reqId, tickType, value)
        print('ID: ', reqId, 'TickType: ', tickType, 'Value: ', value)


    def tickEFP(self, reqId:TickerId, tickType:TickType, basisPoints:float,
                formattedBasisPoints:str, totalDividends:float,
                holdDays:int, futureLastTradeDate:str, dividendImpact:float,
                dividendsToLastTradeDate:float):
        """ market data call back for Exchange for Physical
        tickerId -      The request's identifier.
        tickType -      The type of tick being received.
        basisPoints -   Annualized basis points, which is representative of
            the financing rate that can be directly compared to broker rates.
        formattedBasisPoints -  Annualized basis points as a formatted string
            that depicts them in percentage form.
        impliedFuture - The implied Futures price.
        holdDays -  The number of hold days until the lastTradeDate of the EFP.
        futureLastTradeDate -   The expiration date of the single stock future.
        dividendImpact - The dividend impact upon the annualized basis points
            interest rate.
        dividendsToLastTradeDate - The dividends expected until the expiration
            of the single stock future."""

        super().tickEFP(reqId, tickType, basisPoints, formattedBasisPoints, totalDividends, holdDays,
                        futureLastTradeDate, dividendImpact, dividendsToLastTradeDate)
        # TODO: Print these


    def orderStatus(self, orderId:OrderId , status:str, filled:float,
                    remaining:float, avgFillPrice:float, permId:int,
                    parentId:int, lastFillPrice:float, clientId:int,
                    whyHeld:str, mktCapPrice: float):
        """This event is called whenever the status of an order changes. It is
        also fired after reconnecting to TWS if the client has any open orders.

        orderId: OrderId - The order ID that was specified previously in the
            call to placeOrder()
        status:str - The order status. Possible values include:
            PendingSubmit - indicates that you have transmitted the order, but have not  yet received confirmation that it has been accepted by the order destination. NOTE: This order status is not sent by TWS and should be explicitly set by the API developer when an order is submitted.
            PendingCancel - indicates that you have sent a request to cancel the order but have not yet received cancel confirmation from the order destination. At this point, your order is not confirmed canceled. You may still receive an execution while your cancellation request is pending. NOTE: This order status is not sent by TWS and should be explicitly set by the API developer when an order is canceled.
            PreSubmitted - indicates that a simulated order type has been accepted by the IB system and that this order has yet to be elected. The order is held in the IB system until the election criteria are met. At that time the order is transmitted to the order destination as specified.
            Submitted - indicates that your order has been accepted at the order destination and is working.
            Cancelled - indicates that the balance of your order has been confirmed canceled by the IB system. This could occur unexpectedly when IB or the destination has rejected your order.
            Filled - indicates that the order has been completely filled.
            Inactive - indicates that the order has been accepted by the system (simulated orders) or an exchange (native orders) but that currently the order is inactive due to system, exchange or other issues.
        filled:int - Specifies the number of shares that have been executed.
            For more information about partial fills, see Order Status for Partial Fills.
        remaining:int -   Specifies the number of shares still outstanding.
        avgFillPrice:float - The average price of the shares that have been executed. This parameter is valid only if the filled parameter value is greater than zero. Otherwise, the price parameter will be zero.
        permId:int -  The TWS id used to identify orders. Remains the same over TWS sessions.
        parentId:int - The order ID of the parent order, used for bracket and auto trailing stop orders.
        lastFilledPrice:float - The last price of the shares that have been executed. This parameter is valid only if the filled parameter value is greater than zero. Otherwise, the price parameter will be zero.
        clientId:int - The ID of the client (or TWS) that placed the order. Note that TWS orders have a fixed clientId and orderId of 0 that distinguishes them from API orders.
        whyHeld:str - This field is used to identify an order held when TWS is trying to locate shares for a short sell. The value used to indicate this is 'locate'.

        """

        super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId
                            , whyHeld, mktCapPrice)
        # print('OrderID:', orderId, 'Status:', status, 'Filled:', filled, 'Remaining:', remaining, 'avgFillPrice:',
        #       avgFillPrice, 'permId:', permId, 'parentId:', parentId, 'lastFillPrice,', lastFillPrice, 'clientId',
        #       clientId, 'whyheld:', whyHeld, 'mktCapPrice:', mktCapPrice)
        #
        # # TODO: Check the format on these
        # data = open('csv/openOrderData.csv', 'a', newline='')
        # with (data):
        #     writer = csv.writer(data)
        #     writer.writerow([orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice,
        #                      clientId, whyHeld, mktCapPrice])
        # print('order status written to openOrderData.csv')
        # data.close()

    def openOrder(self, orderId:OrderId, contract:Contract, order:Order,
                  orderState:OrderState):
        """This function is called to feed in open orders.

        orderID: OrderId - The order ID assigned by TWS. Use to cancel or
            update TWS order.
        contract: Contract - The Contract class attributes describe the contract.
        order: Order - The Order class gives the details of the open order.
        orderState: OrderState - The orderState class includes attributes Used
            for both pre and post trade margin and commission data."""
        super().openOrder(orderId, contract, order, orderState)
        #print('OrderId: ', orderId, 'Contract: ', contract, 'Order: ', order, 'OrderState: ', orderState.status)

        # # TODO: Check the format on these
        # data = open('csv/openOrderData.csv', 'a', newline='')
        # with (data):
        #     writer = csv.writer(data)
        #     writer.writerow([orderId, contract, order, orderState])
        # print('open order info written to openOrderData.csv')
        # data.close()

    def openOrderEnd(self):
        """This is called at the end of a given request for open orders."""
        super().openOrderEnd()
        #print('Open order end')

    def updateAccountValue(self, key:str, val:str, currency:str, accountName:str):
        """ This function is called only when ReqAccountUpdates on
        EEClientSocket object has been called. """

        super().updateAccountValue(key, val, currency, accountName)
        print('Key: ', key, 'Value: ', val, 'Currency: ', currency, 'Acct Name: ', accountName)

    def updatePortfolio(self, contract:Contract, position:float,marketPrice:float, marketValue:float,
                        averageCost:float, unrealizedPNL:float, realizedPNL:float, accountName:str):
        """This function is called only when reqAccountUpdates on
        EEClientSocket object has been called."""

        super().updatePortfolio(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL,
                                accountName)
        print('Contract: ', contract, 'Position: ', position, 'marketPrice: ', marketPrice, 'MarketValue: ',
              marketValue, 'Average Cost: ', averageCost, 'unrealizedPNL: ', unrealizedPNL, 'realizedPNL: ',
              realizedPNL, 'Account name: ', accountName)

    def updateAccountTime(self, timeStamp: str):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("Account download finished:", accountName)


    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        print("Daily PnL. Req Id: ", reqId, ", daily PnL: ", dailyPnL,
              ", unrealizedPnL: ", unrealizedPnL, ", realizedPnL: ", realizedPnL)

    def pnlSingle(self, reqId: int, pos: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float, value: float):
        super().pnlSingle(reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value)
        print("Daily PnL Single. Req Id: ", reqId, ", pos: ", pos,
              ", daily PnL: ", dailyPnL, ", unrealizedPnL: ", unrealizedPnL,
              ", realizedPnL: ", realizedPnL, ", value: ", value)

        data = open('csv/PnLSingleInfo.csv', 'a', newline='')
        with data:
            writer = csv.writer(data)
            writer.writerow([reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value])
        print('PnLSingleInfo written to PnLSingleInfo.csv')
        data.close()

    def symbolSamples(self, reqId: int, contractDescriptions: ListOfContractDescription):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)
        for contractDescription in contractDescriptions:
            derivSecTypes = ""
        for derivSecType in contractDescription.derivativeSecTypes:
            derivSecTypes += derivSecType
            derivSecTypes += " "
        print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, ""currency:%s, derivativeSecTypes:%s" % (
            contractDescription.contract.conId, contractDescription.contract.symbol,
            contractDescription.contract.secType, contractDescription.contract.primaryExchange,
            contractDescription.contract.currency, derivSecTypes))


# The new and most efficient tws class
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

    return(order)



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








