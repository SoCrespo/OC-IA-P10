# encoding = utf-8
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
import params

runtimeCredentials = CognitiveServicesCredentials(
    params.predictionKey)

clientRuntime = LUISRuntimeClient(
    endpoint=params.predictionEndpoint, 
    credentials=runtimeCredentials)


def understand(text):
    """Return LUIS intent and entities for a given text."""
    request = {"query": text}
    result = clientRuntime.prediction.get_slot_prediction(
        params.appId, params.slotName, request)
    intent = result.prediction.top_intent
    entities = result.prediction.entities
    for key, value in entities.items():
        try:
            entities[key] = value[0]
        except KeyError:
            entities[key] = ''  
    return {'intent': intent, 'entities': result.prediction.entities}

if __name__ == '__main__':
    print(understand("I want to book a flight from New York to Paris on the 15th of July"))
        