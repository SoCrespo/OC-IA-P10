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


from app.luis_functions import understand


from dataclasses import dataclass, field

@dataclass
class Prediction:    
    top_intent: str = ''
    entities: dict = field(default_factory=dict)

@dataclass
class MockResponse:
    prediction: Prediction()

def create_mock_prediction_function(expected_response):
    def mock_prediction_func(app_id, slot_name, request):
        return expected_response
    return mock_prediction_func

dict_without_entities = {
        'top_intent': 'None', 
        'entities': {}, 
    }
dict_with_entities = {
        'top_intent': 'INFORM', 
        'entities': {
                'dst_city': ['Madrid'], 
                'or_city': ['Paris'], 
                'str_date': ['25th']
                }, 
    }

func_returning_without_entities = create_mock_prediction_function(MockResponse(Prediction(**dict_without_entities)))
func_returning_with_entities = create_mock_prediction_function(MockResponse(Prediction(**dict_with_entities)))    

def test_understand_return_expect_values_with_entities():
    result = understand('', func_returning_with_entities)
    assert result['intent'] == 'INFORM'
    assert result['entities'] == {
                'dst_city': 'Madrid', 
                'or_city': 'Paris', 
                'str_date': '25th'
                }

def test_understand_return_expect_values_without_entities():
    result = understand('', func_returning_without_entities)
    assert result['intent'] == 'None'
    assert result['entities'] == {}
 
