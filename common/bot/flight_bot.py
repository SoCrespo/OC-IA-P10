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

        text = f"{self.elements.__dict__.items()}"
        return await turn_context.send_activity(MessageFactory.text(text))