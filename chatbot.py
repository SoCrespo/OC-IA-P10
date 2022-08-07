from luis_functions import understand
import logging


FIRST_MESSAGE_KEY = 'first_message'
START_KEY = 'start'
GREETING_KEY = 'greeting'
NONE_KEY = 'None'
STR_DATE_KEY = 'str_date'
END_DATE_KEY = 'end_date'
BUDGET_KEY = 'budget'
OR_CITY_KEY = 'or_city'
DST_CITY_KEY = 'dst_city'
SUMMARIZE_KEY = 'summarize'
REPHRASE_KEY = 'rephrase'
LAST_MESSAGE_KEY = 'last_message'

entities = [
        OR_CITY_KEY,
        DST_CITY_KEY,
        STR_DATE_KEY,
        BUDGET_KEY,
        END_DATE_KEY,
    ]

def summary_message(elements):
    return (f"from {elements[OR_CITY_KEY]} "
            f"to {elements[DST_CITY_KEY]}, "
            f"leaving on {elements[STR_DATE_KEY]} "
            f"and returning on {elements[END_DATE_KEY]},"
            f" for a budget of {elements[BUDGET_KEY]}?")

class Dialog:
    def __init__(self, entities=entities):
        self.elements = dict.fromkeys(entities, '')
        self.messages = {
            FIRST_MESSAGE_KEY: "Hi, I'm your flight assistant.",
            START_KEY: "How can I help you?",
            GREETING_KEY: "Thanks, tell me more about your flight!",
            NONE_KEY: "I'm sorry, I didn't understand. Could you rephrase please?",
            STR_DATE_KEY: "When do you want to leave?",
            END_DATE_KEY: "When do you want to come back?",
            DST_CITY_KEY: "Where do you want to fly to?",
            OR_CITY_KEY: "Where do you want to depart from?",
            BUDGET_KEY: "What is your budget?",
            SUMMARIZE_KEY: "Let's sum up: you want to book a flight" ,  
            REPHRASE_KEY: "Ok, let's try again.",
            LAST_MESSAGE_KEY: "Great, let's find your flights!",
            }
        self.intent = None
        self.entities = None

    @property
    def all_elements_are_known(self):
        return '' not in self.elements.values()

    @property
    def summary(self):
        return summary_message(self.elements)

    def next_element_to_ask(self):
        """Return the first key of self.entities with '' value."""
        for element in self.elements:
            if self.elements[element] == '':
                return element
    
    def reset_elements(self):
        """Reset self.elements to empty strings."""
        self.elements = dict.fromkeys(self.elements.keys(), '')

    def fix_end_date(self):
        """
        If str_date already exist among self.elements,
        converts self.entities[STR_DATE_KEY] to self.entities[END_DATE_KEY].
        """
        if self.elements[STR_DATE_KEY] and STR_DATE_KEY in self.entities:
            end_date = self.entities.pop(STR_DATE_KEY)
            self.entities[END_DATE_KEY] = end_date

    def ask_till_all_elements_are_known(self):
        """
        Ask for missing elements until all keys of self.elements
        have a value (different from '').
        """
        topic = START_KEY
        while not self.all_elements_are_known:
            if not topic in self.messages:
                logging.error(f'Unknown topic: {topic}')
                topic = NONE_KEY
                
            message = self.messages[topic]

            text = input(message + '\n')

            if not text:
                message = self.messages[NONE_KEY]
                continue
            luis_response = understand(text)
            self.intent, self.entities = luis_response['intent'], luis_response['entities']
            if self.entities:
                self.fix_end_date()
                self.elements.update(self.entities)
                topic = self.next_element_to_ask()
            else:
                topic = self.intent if self.intent != 'inform' else NONE_KEY

    def customer_confirms(self):
        """For confirmation."""
        text = input(f'{self.messages[SUMMARIZE_KEY]} {self.summary}\n')
        luis_response = understand(text)
        its_ok = luis_response['intent'] == 'confirm'
        logging.info(its_ok)
        return its_ok
   
    
    def main(self):
        """
        Main dialog loop.
        """
        first_message=True
        while True:
            if first_message:
                print(self.messages[FIRST_MESSAGE_KEY], end=' ')

            self.ask_till_all_elements_are_known()
            if self.customer_confirms():
                print(self.messages[LAST_MESSAGE_KEY])
                break
            else:
                print(self.messages[REPHRASE_KEY], end=' ')
                self.reset_elements()
                first_message = False


if __name__ == '__main__':
    dialog = Dialog()
    dialog.main()

## TODO:
# refacto : créer dataclass pour les elements (et pour les messages)
# entraîner LUIS pour l'intention "désaccord"
# debug : gérer le cas des intents non reconnus (confirm doit être traité)
# logger rephrase et confirm (Azure Insights)