from typing import List
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from bot.elements import Elements
from luis_tools.luis_functions import understand
from entities_and_intents import *

from . import messages as msg

class FlightBot(ActivityHandler):
    """
    A simple echo bot at this stage.
    """
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext):  
        """
        Welcome user.
        """
        return await turn_context.send_activity(
            MessageFactory.text(msg.WELCOME))


    async def on_message_activity(self, turn_context: TurnContext):
        """Display user intent and entities."""
        user_input = turn_context.activity.text
        luis_response = understand(user_input)

        return await turn_context.send_activity(
            MessageFactory.text(f"intent = {luis_response.intent}, entities = {str(luis_response.entities.values())}"))