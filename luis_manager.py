import logging
import requests


logging.basicConfig(level=logging.INFO)
class LuisManager:
    def __init__(self, 
                subscription_id,
                app_id, 
                version_id,
                authoring_key, 
                authoring_endpoint,
                prediction_key,
                prediction_endpoint): 
                
        """
        Manage interactions with existing Luis model:
        - create intent
        - create entity
        - upload samples
        - train model
        - upload test data
        - get test status
        - publish model.
        """
        self.subscription_id=subscription_id
        self.app_id = app_id
        self.version_id = version_id
        self.authoring_key = authoring_key
        self.authoring_endpoint = authoring_endpoint
        self.prediction_key = prediction_key
        self.prediction_endpoint = prediction_endpoint

        endpoint_tail = f"v3.0-preview/apps/{self.app_id}/versions/{self.version_id}/"
        self.request_authoring_url = f"{self.authoring_endpoint}luis/authoring/{endpoint_tail}"
        self.request_prediction_url = f"{self.prediction_endpoint}luis/{endpoint_tail}"

        self.authoring_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': self.authoring_key
        }

        self.prediction_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': self.prediction_key
        }

    def _post(self, url_end, data, ):
        """
        Send data to self.request_authoring_url/url_end.
        Return a requests.Response object.
        """
        url = self.request_authoring_url + url_end
        response = requests.post(url, headers=self.authoring_headers, json=data)
        return response
   
    def _get(self, url_end):
        """
        Get data from self.request_authoring_url/url_end.
        Return a requests.Response object.
        """
        url = self.request_authoring_url + url_end
        response = requests.get(url, headers=self.authoring_headers)
        return response


    def create_intent(self, intent_name):
        """
        Add an intent to the app.
        Return a requests.Response object.        
        """
        logging.info(f"Creating intent {intent_name}...")
        url_end = 'intents'
        url = self.request_authoring_url + url_end
        data = {'name': intent_name}
        response = requests.post(url, headers=self.authoring_headers, json=data)
        if response.status_code < 400:
            logging.info(f"Intent {intent_name} created.")
        else:
            logging.warning(f"Intent {intent_name} not created: {response.json()['error']}")
        return response
        

    def create_entity(self, entity_name):
        """
        Add an entity to the app.
        Return a requests.Response object.
        """
        logging.info(f"Creating entity {entity_name}...")
        url = self.request_authoring_url + 'entities'
        data = {'name': entity_name}
        response = requests.post(url, headers=self.authoring_headers, json=data)
        if response.status_code < 400:
            logging.info(f"Entity {entity_name} created.")
        else:
            logging.warning(f"Entity {entity_name} not created: {response.json()['error']}")
        return response

        
    def upload_samples(self, samples_list):
        """
        Add labeled samples (list of dicts) to LUIS.
        Return a requests.Response object.

        Each labeled sample is sent as a separate request.
        Train data is a list of dicts with following format:
        {'text': str, 
        'intentName': str, 
        'entityLabels': [
                        {
                        'entityName': str, 
                        'startCharIndex': int, 
                        'endCharIndex': int
                        },
                        ...
                        ]
            }
        """
        logging.info('Starting samples upload...')
        url = self.request_authoring_url + "examples"
        response = requests.post(url, headers=self.authoring_headers, json=samples_list)
        if response.status_code < 400:
            logging.info(f"samples loaded.")
        else:
            logging.warning(f"samples not loaded: {response.json()['error']}")
        return response


    def train_model(self):
        """
        Train app on uploaded utterances.
        Return a requests.Response object.
        """
        logging.info('Starting model training...')
        url = self.request_authoring_url + "train"
        response = requests.post(url, headers=self.authoring_headers, data={})
        if response.status_code < 400:
            logging.info(f"Training launched.")
        else:
            logging.warning(f"Error at training lauching: {response.json()['error']}")
        return response

        
    def get_training_status(self):
        """
        Get training status from LUIS.
        Return a requests.Response object.
        """
        url = self.request_authoring_url + "train"
        response = requests.get(url, headers=self.authoring_headers)
        if response.status_code < 400:
            logging.info(f"Model trained.")
        else:
            logging.warning(f"Problem: {response.json()['error']}")
        return response    


    def upload_test_data(self, test_data):
        """
        Send test data to LUIS.
        Return a requests.Response object.

        Data is a list of dicts with following format:
        {'text': str,
        'intent': str,
        'entities': [
                        {
                        'entity': str, 
                        'startPos': int, 
                        'endPos': int
                        },
                ...]
        }
        """
        url = self.request_prediction_url + "evaluations"
        data = {"LabeledTestSetUtterances": test_data}
        response = requests.post(url, headers=self.prediction_headers, json=data)
        if response.status_code < 400:
            logging.info(f"Test data uploaded.")
        else:
            logging.warning(f"Problem: {response.json()['error']}")
        return response


    def get_test_status(self, operation_id):
        """
        Get test status from LUIS.
        Return a requests.Response object.
        """
        url = self.request_prediction_url + f"evaluations/{operation_id}/status"
        response = requests.get(url, headers=self.prediction_headers)
        return response


    def get_test_result(self, operation_id):
        """
        Get test result from LUIS.
        Return a requests Reponse object.
        """        
        url = self.request_prediction_url + f"evaluations/{operation_id}/result"
        response = requests.get(url, headers=self.prediction_headers)
        return response

    def publish_model(self):
        """
        Publish model to production
        to the published endpoint.
        Return a requests.Response object.
        """
        raise NotImplementedError