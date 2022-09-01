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
        self.entities = self.extract_entities(prediction.json()['prediction']['entities'])

    def extract_entities(self, entities):
        """
        Extract entities from prediction.
        :entities: A dict with form {key1: [val1], key2: [val2], ...}

        :return: A dict with form {key1: val1, key2: val2, ...}
        """
        extracted_entities = {key: value[0] for key, value in entities.items()}
        return extracted_entities