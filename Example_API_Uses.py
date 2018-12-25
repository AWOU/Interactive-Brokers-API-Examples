import IB_API
import IB_Orders

# Simple Example: connecting to TWS and placing an order
tws = IB_API.TWS()
tws.connect('127.0.0.1', 100, 7497)
tws.startApi()

contract = IB_Orders.create_contract("IBKR", "STK", "USD", "SMART")
order = IB_Orders.create_base_order("BUY", "MKT", 100)

tws.placeOrder(IB_API.getNextOrderId(), contract, order)

# Note: The run method has to be called after everything is set up before
tws.run()

tws.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

# Simple Example 2: creating and placing a limit order
tws = IB_API.TWS()
tws.connect('127.0.0.1', 100, 7497)
tws.startApi()

contract = IB_Orders.create_contract("IBKR", "STK", "USD", "SMART")
order = IB_Orders.create_base_order("BUY", "LMT", 100)
# Note: To see more about order types and creating custom orders go to the Interactive Brokers API documentation at
# https://interactivebrokers.github.io/tws-api/introduction.html
order.auxPrice = 200.10

tws.placeOrder(IB_API.getNextOrderId(), contract, order)

tws.run()

tws.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

# Example of how to check the positions that are being held
tws = IB_API.TWS()
tws.connect('127.0.0.1', 100, 7497)
tws.startApi()

tws.reqPositions(100)
tws.disconnect()

positions = tws.positions

if len(positions) == 0:
    print("No positions held")
else:
    for pos in positions:
        print(pos)
# ----------------------------------------------------------------------------------------------------------------------
