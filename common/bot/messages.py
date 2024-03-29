
FIRST_MESSAGE = "Hi! I'm your flight reservation assistant."
START = " How can I help you?"
NONE_INTENT = "Sorry, I didn't understand. "
GREETING_INTENT = "I'm at your service!"
AGREE_INTENT = "Great, let's find your flights!"
DISAGREE_INTENT = "Sorry, I'm trying to do my best. Thanks for your patience! How can I help you?"
STR_DATE_ENTITY = "What is your departure date?"
END_DATE_ENTITY = "What is your return date?"
DST_CITY_ENTITY = "Where do you want to fly to?"
OR_CITY_ENTITY = "Where do you want to depart from?"
BUDGET_ENTITY = "What is your budget?"
ASK_CONFIRMATION = " Is this correct?"

element_to_get_dict = {
    'or_city': OR_CITY_ENTITY,
    'dst_city': DST_CITY_ENTITY,
    'str_date': STR_DATE_ENTITY,
    'end_date': END_DATE_ENTITY,
    'budget': BUDGET_ENTITY,
}