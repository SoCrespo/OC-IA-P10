# OC-IA-P10

This repository contains the code for the 10th project of the OpenClassrooms AI Engieneer path.

## Project description

The aim of this project is to build a chatbot that can collect following information about a flight a user would like to book:
- departure city
- arrival city
- departure date
- return date
- budget.

The chatbot must then summarize the information and ask the user to confirm them. If the bot did not interpret the user's input correctly, it must ask the user to re-enter the information and log the incident on Azure Insights.

## Structure


- `app.py` : main file that launches the chatbot as a server.  

-  `common/`:
    - `common/luis_tools/` : code to interact with the LUIS API:  
        - `luis_manager.py` : class `LuisManager` interacting with LUIS API
        - `luis_prediction.py` : class `Prediction` holding predictions returned by the LUIS API as an object.  


    - `common/bot/` : bot code:
        - `elements.py` : class Elements holding information collected by the bot
        - `entities_and_intents.py` : entities (departure city, destination...) and intents (agree, disagree, inform...) used by the bot
        - `flight_bot.py` : the bot itself. Class FlightBot managing the conversation with the user
        - `luis_functions` : function interacting with the LUIS API (interface with LuisManager)
        - `messages.py` : text of messages sent by the bot

- `tests/` : unit tests for the bot code. These tests are here to demonstrate how to insert tests into a CI/CD pipeline. They are not meant to be exhaustive. 



## Installation

This bot is to be deployed on an Azure Web App in a CI/CD pipeline. The appropriate environment variables must be set in the Azure portal.

## Usage

The bot can be accessed at the following URL: https://oc-ia-p10.azurewebsites.net/, using the Bot Framework Emulator. ID and password are available in the Azure portal.