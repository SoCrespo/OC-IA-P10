from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import json, time, uuid
import params

def quickstart():
        
    authoringKey = params.authoringKey
    authoringEndpoint = params.authoringEndpoint
    predictionKey = params.predictionKey
    predictionEndpoint = params.predictionEndpoint
    
    # We use a UUID to avoid name collisions.
    appName = "Contoso Pizza Company " + str(uuid.uuid4())
    versionId = "0.1"
    intentName = "OrderPizzaIntent"

    client = LUISAuthoringClient(authoringEndpoint, 
                            CognitiveServicesCredentials(authoringKey))

    # define app basics
# define app basics
    appDefinition = ApplicationCreateObject(name=appName, 
                                initial_version_id=versionId, 
                                culture='en-us')

    # create app
    app_id = client.apps.add(appDefinition)

    # get app id - necessary for all other changes
    print(f"Created LUIS app with ID {app_id}")

    client.model.add_intent(app_id, versionId, intentName)
                        
quickstart()
