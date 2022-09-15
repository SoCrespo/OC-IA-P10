
from datetime import datetime
import logging
from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, Activity
from opencensus.ext.azure.log_exporter import AzureLogHandler

from common.bot.elements import Elements
from common.bot.luis_functions import understand
from common.bot import messages as msg
import entities_and_intents as ei

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler()) # No param needed if APPLICATIIONINSIGHTS_CONNECTION_STRING is set

class FlightBot(ActivityHandler):

    def create_elements(self):
        self.elements = Elements()

    def create_conversation(self):
        self.conversation = []


    def log_conversation(self, level=logging.WARNING):
        """
        Log self.conversation.
        """
        conversation_elements = []
        for activity in self.conversation:
            text = activity.text
            timestamp = activity.timestamp.strftime("%d/%m/%Y, %H:%M:%S")
            user = activity.from_property.name
            line = f"{timestamp}  | {user}: {text}"
            conversation_elements.append(line)
        msg = "The following conversation lead to 'DISAGREE' intent:\n\n" + "\n".join(conversation_elements)
        logger.log(level=level, msg=msg)


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
        welcome_activity = Activity(text=message, from_property=ChannelAccount(name="Bot"), timestamp=datetime.now())
        self.conversation.append(welcome_activity)
        return await turn_context.send_activity(MessageFactory.text(message))


    async def on_message_activity(self, turn_context: TurnContext):
        """
        Return a message according to the intent and entities detected in message by Luis.
        """

        text = turn_context.activity.text

        user_activity = Activity(
            text=text, 
            from_property=ChannelAccount(name="User"), 
            timestamp=datetime.now()
            )
        self.conversation.append(user_activity)

        luis_response = understand(text)
        intent, entities = luis_response.intent, luis_response.entities
        fixed_entities = self._fix_end_date(entities)
        self._update_elements(fixed_entities)
                
        text = msg.NONE_INTENT

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

        
        bot_activity = Activity(
            text=text, 
            from_property=ChannelAccount(name="Bot"), 
            timestamp=datetime.now())
        self.conversation.append(bot_activity)

        return await turn_context.send_activity(MessageFactory.text(text))

       