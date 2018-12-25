# Interactive Brokers API Guide:

This repository is for demonstrating how to use the Interactive Brokers API. When getting started with the API, 
there are not a whole lot of models or examples online that show you how to get the api setup in the beginning and that 
is why I created this project. It covers the basics of how to use the API and where to go from here if you would like
to continue learning about the more advanced parts of it. 

## Before You Get Started: 

* Make sure to install the Interactive Brokers API at http://interactivebrokers.github.io/
    * Make sure read the instructions for installing it as a package in the file contents because it is not as simple
    as a pip install 
    
NOTE: This code is using the official Interactive Brokers API (version 9.73) with their python implementation and may
differ from their other languages or third party packages. 

## How to use the API:

Check the example uses file to see some examples of how you can use the API. 

## General Notes:

Interactive Brokers has thorough documentation of their API at 
https://interactivebrokers.github.io/tws-api/index.html that is well written and easy to navigate. 
<br><br>
Most of the functions in the TWS class are just wrapper functions overriding the default ibapi package functions
which sends everything to a log file by default. This can be sufficient for most operations but can be easily 
personalized if they need to be. An example of this is how the reqPositions function in the IB_API.py TWS class is 
implemented so that it saves the data positions held to a list that can be easily retrieved instead of straight to the log 
file. 

## Summary of how the API Works:

The API is split into 3 main parts: the client, the connection, and the wrapper. The best way to understand it is to just
start reading their code but I summarized the main parts so that you can have a general idea of what is  happening in 
their code. 

* The Client (client.py):

* The Connection (connection.py):

* The Wrapper (Wrapper.py): 





