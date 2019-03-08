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

def bracket_order(parentOrderId: int, action: str, quantity: float, limitPrice: float,
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

