# Interactive Brokers API Guide:

This repository is just to show some examples of how to use the Interactive Brokers API for some general cases. 

## Before You Get Started: 

1. Install the Interactive Brokers API at http://interactivebrokers.github.io/ 
2. Enable API access in the Trader Workstation (TWS) application 

## General Notes:

The code I provided is split up between the actual TWS class in IB_API.py, the the order objects based on their types in
IB_Orders.py, and some examples of how to use them at Example_API_Uses.py. 

The functions in the TWS class in IB_API.py are just wrapper functions overriding the default ibapi package functions
which sends everything to a log file by default. You find all of the wrapper functions in the file wrapper.py in the actual Interactive Brokers package. 

Interactive Brokers has thorough documentation of their API at 
https://interactivebrokers.github.io/tws-api/index.html that is well written and easy to navigate. 
<br><br>



