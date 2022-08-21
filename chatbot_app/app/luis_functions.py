# encoding = utf-8
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import dotenv_values
from types import SimpleNamespace
config = SimpleNamespace(**dotenv_values())

runtime_credentials = CognitiveServicesCredentials(
    config.prediction_key)

clientRuntime = LUISRuntimeClient(
    endpoint=config.prediction_endpoint, 
    credentials=runtime_credentials)


def understand(text, prediction_func=clientRuntime.prediction.get_slot_prediction):
    """
    Return LUIS intent and entities for a given text.
    """
    request = {"query": text}
    result = prediction_func(
            config.app_id, config.slot_name, request)
    intent = result.prediction.top_intent
    entities = result.prediction.entities
    for key, value in entities.items():
        try:
            entities[key] = value[0]
        except KeyError:
            entities[key] = ''  
    return {'intent': intent, 'entities': result.prediction.entities}

if __name__ == '__main__':
    print(understand("I want to fly to Madrid from Paris on the 25th of June"))
        