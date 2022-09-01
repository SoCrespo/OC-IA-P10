from botbuilder.core import ActivityHandler, MessageFactory, TurnContext

class FlightBot(ActivityHandler):
    """
    A simple echo bot at this stage.
    """
    async def on_message_activity(self, turn_context: TurnContext):
        return await turn_context.send_activity(
            MessageFactory.text(f"You said: {turn_context.activity.text}")
        )