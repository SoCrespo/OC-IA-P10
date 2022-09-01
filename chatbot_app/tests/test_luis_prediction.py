# coding =utf-8
###############################################################################################################################
# This code is necessary to import tested functions and their params
###############################################################################################################################                                                                                                        #
import sys
from pathlib import Path
p = Path(__file__)
chatbot_app_path = p.parent.parent
app_path = chatbot_app_path/'app'
sys.path.extend([chatbot_app_path.as_posix(), app_path.as_posix()])
###############################################################################################################################

import pytest
from luis_tools.luis_prediction import LuisPrediction

class MockResponse:
    def __init__(self, json: dict):
        self._json = json

    def json(self):
        return self._json

@pytest.fixture
def prediction():
    return MockResponse(
        {
            'query': 'I want to book a flight to London', 
            'prediction': {
                'topIntent': 'inform', 
                'intents': {'inform': {'score': 0.31024516}}, 
                'entities': {'dst_city': ['London']}
                          }
        }
                        )

@pytest.fixture
def empty_prediction():
    return MockResponse(
        {
            'query': 'xxxxx', 
            'prediction': {
                'topIntent': 'None', 
                'intents': {'None': {'score': 0.81479394}}, 
                'entities': {}}}
                        )

def test_luis_prediction_has_no_intent_if_empty(empty_prediction):
    result = LuisPrediction(empty_prediction)
    assert result.intent == 'None'

def test_luis_prediction_has_no_entities_if_empty(empty_prediction):
    result = LuisPrediction(empty_prediction)
    assert result.entities == {}

def test_luis_prediction_has_text(prediction):
    result = LuisPrediction(prediction)
    assert result.text == 'I want to book a flight to London'

def test_luis_prediction_has_intent(prediction):
    result = LuisPrediction(prediction)
    assert result.intent == 'inform'    

def test_luis_prediction_has_entities(prediction):
    result = LuisPrediction(prediction)
    assert result.entities == {'dst_city': 'London'}
