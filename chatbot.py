from luis_functions import understand

entities = [
        "or_city",
        "dst_city",
        "str_date",
        "end_date",
        "budget",
    ]


class Dialog:
    def __init__(self, entities=entities):
        self.elements = dict.fromkeys(entities, '')
        self.messages = {
            "first_message": "Hi, I'm your flight assistant.",
            "start": "How can I help you?",
            "greeting": "Thanks, tell me more about your flight!",
            "none": "I'm sorry, I didn't understand. Could you rephrase please?",
            "str_date": "When do you want to leave?",
            "end_date": "When do you want to come back?",
            "dst_city": "Where do you want to fly to?",
            "or_city": "Where do you want to depart from?",
            "budget": "What is your budget?",
            "summarize": "Let's sum up: you want to book a flight" ,  
            "rephrase": "Ok, let's try again.",
            "last_message": "Great, let's find your flights!",
            }
        self.intent = None
        self.entities = None

    @property
    def all_elements_are_known(self):
        return '' not in self.elements.values()

    @property
    def summary(self):
        return (f"from {self.elements['or_city']} "
                f"to {self.elements['dst_city']}, "
                f"leaving on {self.elements['str_date']} "
                f"and returning on {self.elements['end_date']},"
                f" for a budget of {self.elements['budget']}?")

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
        converts self.entities['str_date'] to self.entities['end_date'].
        """
        if self.elements['str_date'] and 'str_date' in self.entities:
            end_date = self.entities.pop('str_date')
            self.entities['end_date'] = end_date

    def ask_till_all_elements_are_known(self):
        """
        Ask for missing elements until all keys of self.elements
        have a value (different from '').
        """
        topic = "start"
        while not self.all_elements_are_known:
            message = self.messages[topic]
            text = input(message + '\n')

            if not text:
                message = self.messages["none"]
                continue
            luis_response = understand(text)
            self.intent, self.entities = luis_response['intent'], luis_response['entities']
            if self.entities:
                self.fix_end_date()
                self.elements.update(self.entities)
                topic = self.next_element_to_ask()
            else:
                topic = self.intent if self.intent != 'inform' else 'none'

    def customer_confirms(self):
        """ for confirmation."""
        text = input(f'{self.messages["summarize"]} {self.summary}\n')
        luis_response = understand(text)
        return luis_response['intent'] == 'confirm'
   
    
    def main(self, first_message=True):
        """
        Main dialog loop.
        """
        if first_message:
            print(self.messages["first_message"], end=' ')

        self.ask_till_all_elements_are_known()
        if self.customer_confirms():
            print(self.messages["last_message"])
        else:
            print(self.messages["rephrase"], end=' ')
            self.reset_elements()
            self.main(first_message=False)


if __name__ == '__main__':
    dialog = Dialog()
    dialog.main()