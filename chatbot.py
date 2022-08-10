import logging
from uuid import uuid4
from luis_functions import understand

logging.basicConfig(
    filename="conversations.log", 
    datefmt="%d/%m/%y %H:%M:%S",
    format="%(asctime)s: %(levelname)s: %(message)s",
    level=logging.INFO)

FIRST_MESSAGE_KEY = 'first_message'
START_KEY = 'start'
NONE_KEY = 'None'
STR_DATE_KEY = 'str_date'
END_DATE_KEY = 'end_date'
BUDGET_KEY = 'budget'
OR_CITY_KEY = 'or_city'
DST_CITY_KEY = 'dst_city'
SUMMARIZE_KEY = 'summarize'
LAST_MESSAGE_KEY = 'last_message'

AGREE_INTENT = 'agree'
DISAGREE_INTENT = 'disagree'
INFORM_INTENT = 'inform'
GREETING_INTENT = 'greeting'
NONE_INTENT = 'None'

entities = [
        OR_CITY_KEY,
        DST_CITY_KEY,
        STR_DATE_KEY,
        END_DATE_KEY,
        BUDGET_KEY,
    ]

def summary_message(elements):
    return ("Let's sum up: you want to book a flight " 
            f"from {elements[OR_CITY_KEY]} "
            f"to {elements[DST_CITY_KEY]}, "
            f"leaving on {elements[STR_DATE_KEY]} "
            f"and returning on {elements[END_DATE_KEY]},"
            f" for a budget of {elements[BUDGET_KEY]}?")

class Dialog:
    def __init__(self, entities=entities):
        self.uuid = uuid4()
        self.elements = self.reset_elements()
        self.messages = {
            FIRST_MESSAGE_KEY: "Hi, I'm your flight assistant.",
            START_KEY: "How can I help you?",
            NONE_KEY: "I'm sorry, I didn't understand. Could you rephrase please?",
            STR_DATE_KEY: "When do you want to leave?",
            END_DATE_KEY: "When do you want to come back?",
            DST_CITY_KEY: "Where do you want to fly to?",
            OR_CITY_KEY: "Where do you want to depart from?",
            BUDGET_KEY: "What is your budget?", 

            LAST_MESSAGE_KEY: "Great, let's find your flights!",
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
        converts entities[STR_DATE_KEY] to entities[END_DATE_KEY].
        """
        if self.elements[STR_DATE_KEY]!='unknown' and STR_DATE_KEY in entities:
            end_date = entities.pop(STR_DATE_KEY)
            entities[END_DATE_KEY] = end_date
        return entities

    def ask_till_all_elements_are_known(self):
        """
        Ask for missing elements until all keys of self.elements
        have a value (different from 'unknown').
        """
        topic = START_KEY
        while not self.all_elements_are_known:
            if not topic in self.messages:
                logging.error(f'Unknown topic: {topic}')
                topic = NONE_KEY
            logging.info(f"{self.uuid}: elements = {self.elements}")    
            message = self.messages[topic]
            logging.info(f"{self.uuid} BOT: {message}")

            text = input(message + '\n')
            if not text:
                topic = NONE_KEY
                continue

            logging.info(f"{self.uuid} USER: {text}")
            luis_response = understand(text)
            intent, entities = luis_response['intent'], luis_response['entities']
            if entities:
                entities = self._fix_end_date(entities)
                self.elements.update(entities)
                topic = self.next_element_to_ask()
            else:
                topic = intent if intent != 'inform' else NONE_KEY

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
                print(self.messages[FIRST_MESSAGE_KEY], end=' ')


            self.ask_till_all_elements_are_known()
            confirmation = self.ask_for_confirmation()
            logging.info(f"{self.uuid}, USER: {confirmation}")

            final_intent = understand(confirmation)['intent']

            if final_intent == 'agree':
                message = self.messages[LAST_MESSAGE_KEY]
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
                message = self.messages[NONE_KEY]
                logging.info(f"{self.uuid} intent = {final_intent}")
                logging.info(f"{self.uuid} BOT: {message}")


if __name__ == '__main__':
    
    dialog = Dialog()
    dialog.main()

