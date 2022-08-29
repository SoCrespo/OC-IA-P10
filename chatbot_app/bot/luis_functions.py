# encoding = utf-8
from dotenv import dotenv_values

from .luis_manager import LuisManager
from .luis_prediction import LuisPrediction

lm = LuisManager(**dotenv_values())

print(lm)

def understand(text, prediction_func=lm.get_prediction_response) -> dict:
    """
    Return LUIS intent and entities for a given text.
    """
   
    result = prediction_func(text)
    prediction = LuisPrediction(result)
    return {'intent': prediction.intent, 'entities': prediction.entities}

        