from typing import List
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from common.bot.elements import Elements
from common.bot.luis_functions import understand
import entities_and_intents as ei
from . import messages as msg


class FlightBot(ActivityHandler):
    """
    A simple echo bot at this stage.
    """
    def create_elements(self):
        self.elements = Elements()

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
        return await turn_context.send_activity(
            MessageFactory.text(msg.WELCOME))


    async def on_message_activity(self, turn_context: TurnContext):
        """Display user intent and entities."""
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
                text = msg.NONE_INTENT

        return await turn_context.send_activity(MessageFactory.text(text))