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
from app.elements import Elements

@pytest.fixture
def empty_elements():
    return Elements()

@pytest.fixture
def complete_elements():
    complete_elements = Elements()
    complete_elements.or_city = 'Madrid'
    complete_elements.dst_city = 'Barcelona'
    complete_elements.str_date = '01/01/2019'
    complete_elements.end_date = '01/01/2019'
    complete_elements.budget = '1000'
    return complete_elements

def test_elements_attributes_have_correct_names_and_values(empty_elements):
    assert set(empty_elements.elements) == {'unknown'}

def test_elements_is_complete_true_if_complete(complete_elements):
    assert complete_elements.is_complete()

def test_elements_is_complete_false_if_not_complete(empty_elements):
    assert not empty_elements.is_complete()

def test_elements_attributes_have_correct_names_and_values_after_reset(complete_elements):
    complete_elements.reset_values()
    assert complete_elements.__dict__ == dict.fromkeys(['or_city','dst_city', 'str_date', 'end_date', 'budget'], 'unknown')
