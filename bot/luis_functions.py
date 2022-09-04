# encoding = utf-8
from dotenv import load_dotenv
import os

from luis_tools.luis_manager import LuisManager
from luis_tools.luis_prediction import LuisPrediction

load_dotenv()
luis_params = {key: value for key, value in os.environ.items() if key.startswith("luis_")}
lm = LuisManager(**luis_params)

def understand(text, prediction_func=lm.get_prediction_response) -> LuisPrediction:
    """
    Return LuisPrediction for a given text.
    """
   
    result = prediction_func(text)
    prediction = LuisPrediction(result)
    return prediction
