# coding =utf-8

###############################################################################################################################
# This code is necessary to import tested functions
###############################################################################################################################                                                                                                        #
import sys
from pathlib import Path
p = Path(__file__)
chatbot_app_path = p.parent.parent
app_path = chatbot_app_path/'app'
sys.path.extend([chatbot_app_path.as_posix(), app_path.as_posix()])
###############################################################################################################################

import pytest
from dotenv import dotenv_values
from types import SimpleNamespace

config = SimpleNamespace(**dotenv_values())

from luis_tools.luis_manager import LuisManager
lm = LuisManager(
    config.subscription_id,
    config.app_id, 
    config.version_id, 
    config.authoring_key, 
    config.authoring_endpoint, 
    config.prediction_key,
    config.prediction_endpoint,
    config.slot_name,
)

def test_lm_attributes_not_empty():
    assert lm.subscription_id != ''
    assert lm.app_id != ''
    assert lm.version_id != ''
    assert lm.authoring_key != ''
    assert lm.authoring_endpoint != ''
    assert lm.prediction_key != ''
    assert lm.prediction_endpoint != ''
    assert lm.slot_name != ''

def test_lm_urls_are_valid():
    for url in [
            lm.authoring_endpoint, 
            lm.prediction_endpoint,
            lm.request_authoring_url,
            lm.request_prediction_url,
            lm.request_batch_test_url,
            lm.request_publish_url]:

        assert url.startswith('https://')
        assert len(url) > 10
        if url != lm.request_publish_url:
            assert url.endswith('/')
    





