import logging
from uuid import uuid4
from elements import Elements
from luis_functions import understand
from chatbot_app.app.entities_and_intents import *

logging.basicConfig(
    filename="./conversations.log", 
    datefmt="%d/%m/%y %H:%M:%S",
    format="%(asctime)s: %(levelname)s: %(message)s",
    level=logging.INFO)

FIRST_MESSAGE = 'first_message'
START = 'start'
SUMMARIZE = 'summarize'
NONE = 'None'

def summary(elements):
    return ("Let's sum up: you want to book a flight " 
            f"from {getattr(elements, OR_CITY_ENTITY)} "
            f"to {getattr(elements, DST_CITY_ENTITY)}, "
            f"leaving on {getattr(elements, STR_DATE_ENTITY)} "
            f"and returning on {getattr(elements, END_DATE_ENTITY)},"
            f" for a budget of {getattr(elements, BUDGET_ENTITY)}?")

class Dialog:
    def __init__(self):
        self.uuid = uuid4()
        self.messages = {
            FIRST_MESSAGE: "Hi, I'm your flight assistant.",
            START: "How can I help you?",
            NONE: "I'm sorry, I didn't understand. Could you rephrase please?",
            STR_DATE_ENTITY: "What is your departure date?",
            END_DATE_ENTITY: "What is your return date?",
            DST_CITY_ENTITY: "Where do you want to fly to?",
            OR_CITY_ENTITY: "Where do you want to depart from?",
            BUDGET_ENTITY: "What is your budget?", 
            GREETING_INTENT: "I'm at your service!",
            AGREE_INTENT: "Great, let's find your flights!",
            DISAGREE_INTENT: "Sorry, I'm trying to do my best. Thanks for your patience!",
            }

    def _fix_end_date(self, elements, entities):
        """
        If str_date already exist among elements,
        converts entities[STR_DATE_ENTITY] to entities[END_DATE_ENTITY].
        """
        if getattr(elements, STR_DATE_ENTITY)!='unknown' and STR_DATE_ENTITY in entities:
            end_date = entities.pop(STR_DATE_ENTITY)
            entities[END_DATE_ENTITY] = end_date
        return entities

    def _update_elements(self, elements: Elements, entities: dict) -> Elements:
        """
        Return elements updated with entities. 
        """
        for key, value in entities.items():
            setattr(elements, key, value)
        return elements


    def ask_till_all_elements_are_known(self, elements):
        """
        Ask for missing elements until all keys of elements
        have a value (different from 'unknown').
        """
        topic = START
        while not elements.is_complete():
            if not topic in self.messages:
                logging.error(f'Unknown topic: {topic}')
                topic = NONE
            logging.info(f"{self.uuid}: elements = {elements.elements}")    
            message = self.messages[topic]
            logging.info(f"{self.uuid} BOT: {message}")

            text = input(message + '\n')
            if not text:
                topic = NONE
                continue

            logging.info(f"{self.uuid} USER: {text}")
            luis_response = understand(text)
            intent, entities = luis_response['intent'], luis_response['entities']
            if entities:
                entities = self._fix_end_date(elements, entities)
                elements = self._update_elements(elements, entities)
                topic = elements.next_unknown_element()
            else:
                topic = intent if intent != 'inform' else NONE
        return elements

    def ask_for_confirmation(self, elements):
        """
        Ask for confirmation of all gathered data about the flight.
        Return the text typed by customer.
        """
        message = summary(elements)
        print(message)
        logging.info(f"{self.uuid} BOT: {message}")
        return input()
   
    
    def main(self,elements):
        """
        Main dialog loop.
        """
        first_message=True
        while True:
            if first_message:
                print(self.messages[FIRST_MESSAGE], end=' ')
                logging.info(f"{self.uuid} BOT: {self.messages[FIRST_MESSAGE]}")

            elements = self.ask_till_all_elements_are_known(elements)
            confirmation = self.ask_for_confirmation(elements)
            logging.info(f"{self.uuid} USER: {confirmation}")

            final_intent = understand(confirmation)['intent']

            if final_intent == 'agree':
                message = self.messages[AGREE_INTENT]
                logging.info(f"{self.uuid} intent = {final_intent} *** SUCCESS***")
                print(message)
                logging.info(f"{self.uuid} BOT: {message}")
                break

            elif final_intent == 'disagree':
                message = self.messages[DISAGREE_INTENT]
                logging.warning(f"{self.uuid} intent = {final_intent} *** FAIL***")
                print(message)
                logging.info(f"{self.uuid} BOT: {message}")
                elements.reset_values()
                first_message = False

            else:
                message = self.messages[NONE]
                logging.info(f"{self.uuid} intent = {final_intent}")
                logging.info(f"{self.uuid} BOT: {message}")


if __name__ == '__main__':
    elements = Elements()
    dialog = Dialog()
    dialog.main(elements)

