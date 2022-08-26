import requests

class LuisPrediction:
    """
    Hold the prediction result from LUIS.
    :text: The text that was analysed.
    :intent: The intent that was predicted.
    :entities: The entities that were predicted.
    """
    def __init__(self, prediction: requests.Response):
        self.text = prediction.json()['query']
        self.intent = prediction.json()['prediction']['topIntent']
        self.entities = prediction.json()['prediction']['entities']
