from email.utils import localtime
import logging
from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, Activity

from common.bot.elements import Elements
from common.bot.luis_functions import understand
from common.bot import messages as msg
import entities_and_intents as ei


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FlightBot(ActivityHandler):

    def create_elements(self):
        self.elements = Elements()

    def create_conversation(self):
        self.conversation = []

    def log_conversation(self, level=logging.INFO):
        """
        Log self.conversation.
        """
        for turn_context in self.conversation:
            text = turn_context.activity.text
            logger.log(level, text)
            timestamp = turn_context.activity.timestamp
            user = turn_context.activity.from_property.name
            logger.log(level, f'{timestamp} {user}: {text}')


    def _fix_end_date(self, entities):
        """
        If str_date already exist among self.elements,
        converts entities[STR_DATE_ENTITY] to entities[END_DATE_ENTITY].
        """
        if getattr(self.elements, ei.STR_DATE_ENTITY)!='unknown' and ei.STR_DATE_ENTITY in entities:
            end_date = entities.pop(ei.STR_DATE_ENTITY)
            entities[ei.END_DATE_ENTITY] = end_date
        return entities    

    def _update_elements(self, entities: dict) -> None:
        """
        Update self.elements with entities. 
        """
        for key, value in entities.items():
            setattr(self.elements, key, value)


    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext):  
        """
        Welcome user.
        """
        self.create_elements()
        self.create_conversation()
        message = msg.FIRST_MESSAGE + msg.START
        output_turn = TurnContext(self, Activity(text=message, from_property=members_added[0]))
        self.conversation.append(output_turn)
        return await turn_context.send_activity(
            MessageFactory.text(message))


    async def on_message_activity(self, turn_context: TurnContext):
        """
        Return a message according to the intent and entities.
        """
        self.conversation.append(turn_context)
        user_input = turn_context.activity.text
        luis_response = understand(user_input)
        intent, entities = luis_response.intent, luis_response.entities
        fixed_entities = self._fix_end_date(entities)
        self._update_elements(fixed_entities)
                
        if self.elements.is_complete():
            if intent == ei.AGREE_INTENT:
                text = msg.AGREE_INTENT
            elif intent == ei.DISAGREE_INTENT:
                text = msg.DISAGREE_INTENT
                self.log_conversation(level=logging.WARNING)  
                self.elements.reset_values()
            else:    
                text = self.elements.summarize() + msg.ASK_CONFIRMATION

        else:
            if len(entities) > 0:
                next_element_to_get = self.elements.next_unknown_element()
                text = msg.element_to_get_dict[next_element_to_get]
            elif intent == ei.GREETING_INTENT:
                text = msg.GREETING_INTENT
            else:
                text = msg.NONE_INTENT + ' ' + self.conversation[-2].activity.text
        
        output_turn = TurnContext(self, Activity(text=text))
        self.conversation.append(output_turn)
        return await turn_context.send_activity(MessageFactory.text(text))

       