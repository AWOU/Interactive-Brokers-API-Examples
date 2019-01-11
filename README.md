# Interactive Brokers API Guide:

This repository is for demonstrating how to use the Interactive Brokers API. When getting started with the API, 
there are not a whole lot of models or examples online that show you how to get the api setup in the beginning and that 
is why I created this repository. 

## Before You Get Started: 

* Make sure to install the Interactive Brokers API at http://interactivebrokers.github.io/
    * Make sure read the instructions for installing it as a package in the file contents because it is not as simple
    as a pip install 

NOTE: This code is using the official Interactive Brokers API (version 9.73) for python. 

## How to use the API:

Check the example uses file to see some examples of how you can use the API. 

## General Notes:

Interactive Brokers has thorough documentation of their API at 
https://interactivebrokers.github.io/tws-api/index.html that is well written and easy to navigate. 
<br><br>
Most of the functions in the TWS class are just wrapper functions overriding the default ibapi package functions
which sends everything to a log file by default. This can be sufficient for most operations but can be easily 
personalized if they need to be. An example of this is how the reqPositions function in the IB_API.py TWS class is 
implemented so that it saves the data about the positions held to a list that can be easily retrieved instead of straight to the log 
file. 



