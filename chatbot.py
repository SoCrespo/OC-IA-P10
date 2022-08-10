import logging
from uuid import uuid4
from luis_functions import understand

logging.basicConfig(
    filename="conversations.log", 
    datefmt="%d/%m/%y %H:%M:%S",
    format="%(asctime)s: %(levelname)s: %(message)s",
    level=logging.INFO)

FIRST_MESSAGE = 'first_message'
START = 'start'
SUMMARIZE = 'summarize'
NONE = 'None'

STR_DATE_ENTITY = 'str_date'
END_DATE_ENTITY = 'end_date'
BUDGET_ENTITY = 'budget'
OR_CITY_ENTITY = 'or_city'
DST_CITY_ENTITY = 'dst_city'

AGREE_INTENT = 'agree'
DISAGREE_INTENT = 'disagree'
INFORM_INTENT = 'inform'
GREETING_INTENT = 'greeting'
NONE_INTENT = 'None'

entities = [
        OR_CITY_ENTITY,
        DST_CITY_ENTITY,
        STR_DATE_ENTITY,
        END_DATE_ENTITY,
        BUDGET_ENTITY,
    ]

def summary_message(elements):
    return ("Let's sum up: you want to book a flight " 
            f"from {elements[OR_CITY_ENTITY]} "
            f"to {elements[DST_CITY_ENTITY]}, "
            f"leaving on {elements[STR_DATE_ENTITY]} "
            f"and returning on {elements[END_DATE_ENTITY]},"
            f" for a budget of {elements[BUDGET_ENTITY]}?")

class Dialog:
    def __init__(self, entities=entities):
        self.uuid = uuid4()
        self.elements = self.reset_elements()
        self.messages = {
            FIRST_MESSAGE: "Hi, I'm your flight assistant.",
            START: "How can I help you?",
            NONE: "I'm sorry, I didn't understand. Could you rephrase please?",
            STR_DATE_ENTITY: "When do you want to leave?",
            END_DATE_ENTITY: "When do you want to come back?",
            DST_CITY_ENTITY: "Where do you want to fly to?",
            OR_CITY_ENTITY: "Where do you want to depart from?",
            BUDGET_ENTITY: "What is your budget?", 
            GREETING_INTENT: "I'm at your service!",
            AGREE_INTENT: "Great, let's find your flights!",
            DISAGREE_INTENT: "I'm sorry, I'm trying to do my best. Thanks for your patience!",
            }


    @property
    def all_elements_are_known(self):
        return 'unknown' not in self.elements.values()

    @property
    def summary(self):
        """
        Return updated summary of the flight with actual values.
        """
        return summary_message(self.elements)

    def next_element_to_ask(self):
        """
        Return the first key of entities with 'unknown' value.
        """
        for element in self.elements:
            if self.elements[element] == 'unknown':
                return element
    
    def reset_elements(self):
        """
        Return dict with entities as keys and 'unknown' as values.
        """
        return dict.fromkeys(entities, 'unknown')

    def _fix_end_date(self, entities):
        """
        If str_date already exist among self.elements,
        converts entities[STR_DATE_ENTITY] to entities[END_DATE_ENTITY].
        """
        if self.elements[STR_DATE_ENTITY]!='unknown' and STR_DATE_ENTITY in entities:
            end_date = entities.pop(STR_DATE_ENTITY)
            entities[END_DATE_ENTITY] = end_date
        return entities

    def ask_till_all_elements_are_known(self):
        """
        Ask for missing elements until all keys of self.elements
        have a value (different from 'unknown').
        """
        topic = START
        while not self.all_elements_are_known:
            if not topic in self.messages:
                logging.error(f'Unknown topic: {topic}')
                topic = NONE
            logging.info(f"{self.uuid}: elements = {self.elements}")    
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
                entities = self._fix_end_date(entities)
                self.elements.update(entities)
                topic = self.next_element_to_ask()
            else:
                topic = intent if intent != 'inform' else NONE

    def ask_for_confirmation(self):
        """
        Ask for confirmation of all gathered data about the flight.
        Return the text typed by customer.
        """
        message = self.summary
        print(message)
        logging.info(f"{self.uuid} BOT: {message}")
        return input('\n')
   
    
    def main(self):
        """
        Main dialog loop.
        """
        first_message=True
        while True:
            if first_message:
                print(self.messages[FIRST_MESSAGE], end=' ')


            self.ask_till_all_elements_are_known()
            confirmation = self.ask_for_confirmation()
            logging.info(f"{self.uuid}, USER: {confirmation}")

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
                self.elements = self.reset_elements()
                first_message = False

            else:
                message = self.messages[NONE]
                logging.info(f"{self.uuid} intent = {final_intent}")
                logging.info(f"{self.uuid} BOT: {message}")


if __name__ == '__main__':
    
    dialog = Dialog()
    dialog.main()

