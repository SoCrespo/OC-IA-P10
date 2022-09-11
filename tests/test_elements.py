print(__name__)
import pytest
import sys
import logging

from .bot.elements import Elements

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
    assert set(empty_elements.elements.values()) == {'unknown'}

def test_elements_is_complete_true_if_complete(complete_elements):
    assert complete_elements.is_complete()

def test_elements_is_complete_false_if_not_complete(empty_elements):
    assert not empty_elements.is_complete()

def test_elements_attributes_have_correct_names_and_values_after_reset(complete_elements):
    complete_elements.reset_values()
    assert complete_elements.__dict__ == dict.fromkeys(['or_city','dst_city', 'str_date', 'end_date', 'budget'], 'unknown')

def test_next_unknown_element_returns_none(complete_elements):
    assert complete_elements.next_unknown_element() is None

def test_next_unknown_element_returns_first_unknown_element(empty_elements):
    assert empty_elements.next_unknown_element() == 'or_city'

def test_summarize_returns_correct_string(complete_elements):
    assert complete_elements.summarize() == (
        "You want to fly from Madrid to Barcelona, "
        "departing on 01/01/2019 and coming back on 01/01/2019, "
        "with a budget of 1000."
        )

def test_summarize_returns_correct_string_if_not_complete(empty_elements):
    assert empty_elements.summarize() == "I don't have enough information to summarize your request."