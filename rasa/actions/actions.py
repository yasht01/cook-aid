# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import datetime
from rasa_sdk.events import FollowupAction, ReminderScheduled
from rasa_sdk import Action

from .connection import rec_db

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

dbc=rec_db()
print(dbc)
ctr=0
class ActionGiveRecipe(Action):

    def name(self) -> Text:
        return "action_give_recipe"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        igd=dbc.ingredients(tracker.get_slot('dish_name'))
        print(igd[0])
        dispatcher.utter_message(text=f"This is my recipe for {igd}")
        
        return []

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("I will remind you in 5 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            entities=entities,
            name="my_reminder",
            kill_on_user_message=False,
        )
        return [reminder]
        
class ActionReactToReminder(Action):
    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(f"Reminded!")
        print('reached!')
        
        global ctr
        ctr+=1
        if ctr<2:
            return [FollowupAction(name="action_set_reminder")]
        else:
            return []