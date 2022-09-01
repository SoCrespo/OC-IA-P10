# encoding = utf-8
from dotenv import dotenv_values

from .luis_manager import LuisManager
from .luis_prediction import LuisPrediction

luis_params = {key: value for key, value in dotenv_values().items() if key.startswith('luis_')}
lm = LuisManager(**luis_params)

def understand(text, prediction_func=lm.get_prediction_response) -> LuisPrediction:
    """
    Return LuisPrediction for a given text.
    """
   
    result = prediction_func(text)
    prediction = LuisPrediction(result)
    return prediction
