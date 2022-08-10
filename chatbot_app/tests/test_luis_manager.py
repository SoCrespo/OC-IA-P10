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
from app.luis_manager import LuisManager
from app import params

lm = LuisManager(
    params.subscription_id,
    params.app_id, 
    params.version_id, 
    params.authoring_key, 
    params.authoring_endpoint, 
    params.prediction_key,
    params.prediction_endpoint,
    params.slot_name,
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
    





