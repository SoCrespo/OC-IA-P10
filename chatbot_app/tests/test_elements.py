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

from dataclasses import asdict
from app.elements import Elements

elements = Elements()

def test_elements_attributes_have_correct_names():
    assert asdict(elements) == dict.fromkeys(['or_city','dst_city', 'str_date', 'end_date', 'budget'], 'unknown')
