from chatbot_app.luis_tools.luis_functions import understand
from chatbot_app.luis_tools.luis_prediction import LuisPrediction
from chatbot_app import entities_and_intents as ei

def test_understand_returns_prediction_type():
    result = understand('I want to book a flight from Berlin to London')
    assert isinstance(result, LuisPrediction)

def test_understand_returns_intent():
    result = understand('I want to book a flight from Berlin to London')
    assert result.intent in ei.intents

def test_understand_returns_entities():
    result = understand('I want to book a flight from Berlin to London')
    assert all([keys in ei.entities for keys in result.entities.keys()])

def test_understand_returns_strings_for_entities():
    result = understand('I want to book a flight from Berlin to London')
    assert all([isinstance(values, str) for values in result.entities.values()])

