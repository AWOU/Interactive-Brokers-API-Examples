# Interactive Brokers API Guide:

This repository is for demonstrating how to use the Interactive Brokers API. When getting started with the API, 
there are not very many examples online that show you how to get setup in the beginning and that is why I created 
this repository. 

## Before You Get Started: 

Make sure to install the Interactive Brokers API at http://interactivebrokers.github.io/ and read their instructions for 
installing it because it is a manual pip install. 

NOTE: This code is using the official Interactive Brokers API (version 9.73) for python. 

## General Notes:

The code I provided is split up between the actual TWS class in IB_API.py, the the order objects based on their types in
IB_Orders.py, and some examples of how to use them at Example_API_Uses.py. 

Interactive Brokers has thorough documentation of their API at 
https://interactivebrokers.github.io/tws-api/index.html that is well written and easy to navigate. 
<br><br>
The functions in the TWS class in IB_API.py are just wrapper functions overriding the default ibapi package functions
which sends everything to a log file by default.



