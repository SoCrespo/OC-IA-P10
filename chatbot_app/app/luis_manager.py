import logging
import requests


logging.basicConfig(level=logging.INFO)

def log_and_raise_error(response, message_info, message_error, threshold=300):
    """
    Log messages according to response.
    """
    if response.status_code >= threshold:
        full_message = f"{message_error} {response.json()['error']}"
        logging.error(full_message)
        raise Exception(full_message)
    else:
        logging.info(message_info)


class LuisManager:
    def __init__(self, 
                subscription_id,
                app_id, 
                version_id,
                authoring_key, 
                authoring_endpoint,
                prediction_key,
                prediction_endpoint,
                slot_name): 
                
        """
        Manage interactions with existing Luis model:
        - create intent
        - create entity
        - upload samples
        - train model
        - upload test data
        - get test status
        - publish model.
        - get prediction.
        """
        self.subscription_id=subscription_id
        self.app_id = app_id
        self.version_id = version_id
        self.authoring_key = authoring_key
        self.authoring_endpoint = authoring_endpoint
        self.prediction_key = prediction_key
        self.prediction_endpoint = prediction_endpoint
        self.slot_name = slot_name

        self.request_authoring_url = f"{self.authoring_endpoint}luis/authoring/v3.0/apps/{self.app_id}/versions/{self.version_id}/"
        self.request_publish_url = f'{self.authoring_endpoint}luis/authoring/v3.0-preview/apps/{self.app_id}/publish'
        self.request_batch_test_url = f'{self.prediction_endpoint}luis/v3.0-preview/apps/{self.app_id}/slots/{self.slot_name}/evaluations/'
        self.request_prediction_url = f'{self.prediction_endpoint}luis/prediction/v3.0/apps/{self.app_id}/slots/{self.slot_name}/'

        self.authoring_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': self.authoring_key
        }

        self.prediction_headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': self.prediction_key
        }
  

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
        log_and_raise_error(
            response, 
            f"Intent {intent_name} created.", 
            f"Intent {intent_name} not created")
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
        log_and_raise_error(
            response,
            f"Entity {entity_name} created.",
            f"Entity {entity_name} not created")
        return response

        
    def upload_samples(self, samples_list):
        """
        Add labeled samples (list of dicts) to LUIS.
        Return a requests.Response object.

        Each labeled sample is sent as a separate request.
        Train data is a list of dicts with following format:
        {'text': str  # an utterance
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
        log_and_raise_error(
            response,
            f"Samples uploaded.",
            f"Samples not uploaded")
        return response


    def train_model(self):
        """
        Train app on uploaded utterances.
        Return a requests.Response object.
        """
        logging.info('Starting model training...')
        url = self.request_authoring_url + "train"
        response = requests.post(url, headers=self.authoring_headers, data={})
        log_and_raise_error(
            response,
            "Training launched.",
            "Error at training lauching")
        return response

        
    def get_training_status(self):
        """
        Get training status from LUIS.
        Return a requests.Response object.
        """
        url = self.request_authoring_url + "train"
        response = requests.get(url, headers=self.authoring_headers)
        log_and_raise_error(
            response,
            "Model trained.",
            "Error at training")
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
        url = self.request_batch_test_url
        data = {"LabeledTestSetUtterances": test_data}
        response = requests.post(url, headers=self.prediction_headers, json=data)
        log_and_raise_error(
            response,
            "Test data uploaded.",
            "Error at test data upload")
        return response


    def get_test_status(self, operation_id):
        """
        Get test status from LUIS.
        Return a requests.Response object.
        """
        url = self.request_batch_test_url + f"{operation_id}/status"
        response = requests.get(url, headers=self.prediction_headers)
        log_and_raise_error(
            response,
            "Test status received.",
            "Error at test status")
        return response


    def get_test_result(self, operation_id):
        """
        Get test result from LUIS.
        Return a requests Reponse object.
        """        
        url = self.request_batch_test_url + f"{operation_id}/result"
        response = requests.get(url, headers=self.prediction_headers)
        log_and_raise_error(
            response,
            "Test result received.",
            "Error at test result")
        return response


    def publish_model(self):
        """
        Publish model to production
        to the published endpoint.
        Return a requests.Response object.
        """
        data = {"versionId": self.version_id,
                "isStaging": False, 
                "directVersionPublish": False,
                }
        response = requests.post(
            url=self.request_publish_url, 
            headers=self.authoring_headers,
            json=data)
        log_and_raise_error(
            response,
            "Model published.",
            "Error at model publishing")
        return response


    def get_prediction_response(self, sentence):
        """
        Get prediction from LUIS.
        Return a requests.Response object.
        """
        url = self.request_prediction_url + "predict"
        data = {"query": sentence}
        response = requests.post(url, headers=self.prediction_headers, json=data)
        log_and_raise_error(
            response,
            "Prediction received.",
            "Error at prediction")
        return response
