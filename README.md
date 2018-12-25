# Interactive Brokers API Guide:

This repository is for demonstrating how to use the Interactive Brokers API. When getting started with the API, 
there are not a whole lot of models or examples online that show you how to get the api setup in the beginning and that 
is why I created this project. It covers the basics of how to use the API and where to go from here if you would like
to continue learning about the more advanced parts of it. 

## Before you get started: 

* Make sure to install the Interactive Brokers API at http://interactivebrokers.github.io/
    * Make sure read the instructions for installing it as a package in the file contents because it is not as simple
    as a pip install 
    
NOTE: This code is using the official Interactive Brokers API (version 9.73) with their python implementation and may
differ from their other languages or third party packages. 

## How the API works:

The API is split into 3 main parts, the client, the connection, and the wrapper. The best way to understand it is to just
start reading their code but I will start to summarize the main parts so that you can have an idea of what the main
parts are doing before you start jumping into it as there are also many supporting files as well that will not be helpful 
until you understand what the main parts are doing. 

* The Client (client.py):

* The Connection (connection.py):

* The Wrapper (Wrapper.py): 


## How to use the API:

Check the example uses file to see some examples of how you can use the API. 

## General Notes:

Most of the functions in the TWS classes are just wrapper functions overriding the default ibapi package functions
which sends everything to a log file. This can be sufficient for most operations can often benefit from personalized
functions. An example of this is how reqPositions is implemented so that it writes the positions held to a file or list 
instead of straight to the log file. 

##  Structure of the TWS classes (from the IB_API.py file): 

There are three main TWS classes and they are all very similar despite a few differences. 








