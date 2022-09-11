# coding =utf-8


from dotenv import dotenv_values
from types import SimpleNamespace

luis_params = {key: value for key, value in dotenv_values().items() if key.startswith('luis_')}
config = SimpleNamespace(**luis_params)

from ..luis_tools.luis_manager import LuisManager
lm = LuisManager(
    config.luis_subscription_id,
    config.luis_app_id, 
    config.luis_version_id, 
    config.luis_authoring_key, 
    config.luis_authoring_endpoint, 
    config.luis_prediction_key,
    config.luis_prediction_endpoint,
    config.luis_slot_name,
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
    





