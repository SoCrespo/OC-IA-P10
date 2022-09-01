from typing import List
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

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
        """Echoes user input back to them."""
        return await turn_context.send_activity(
            MessageFactory.text(f"You said: {turn_context.activity.text}")
        )