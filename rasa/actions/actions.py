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
from rasa_sdk.events import FollowupAction, ReminderScheduled, SlotSet
from rasa_sdk import Action

from .connection import rec_db

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

with open('/home/donut/cook-aid/rasa/actions/listOfFood.txt','r') as f:
    food_arr=f.readlines()
    food_arr=[word.lower() for word in arr]
def editDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
def checkDishName(dish_name):
    for i in food_arr:
        if editDistance(i.lower(),dish_name)<=2:
            return i.lower()
    return ""

dbc=rec_db()
steps=dbc.steps('pizza')
no_of_steps=len(steps)
stepCtr=0
class ActionGiveRecipe(Action):

    def name(self) -> Text:
        return "action_give_recipe"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish_name = tracker.get_slot('dish_name')
        if dish_name:
            igd_time=dbc.ingredients(dish_name)
            ingd_step = ""
            for igd in igd_time[0]:
                ingd_step += f"{igd['igd_qty']} {igd['igd_name']}, "
            dispatcher.utter_message(text=f"To cook {dish_name} you will need:")
            dispatcher.utter_message(text=ingd_step)
            dispatcher.utter_message(text=f" Total time required is {igd_time[1]}")

        dispatcher.utter_message(text=f"This is my recipe for {igd}")
        
        return []

class ActionCheckRecipe(Action):

    def name(self) -> Text: 
        return "action_check_recipe"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish_name = tracker.get_slot('dish_name')
        dish_name = checkDishName(dish_name)
        exists=dbc.check_exists(dish_name)
        if exists:
            dispatcher.utter_message(text=f"I can help you make {dish_name}")
            SlotSet("exists","yes")
        else:
            dispatcher.utter_message(text=f"Sorry,I can't help you make {dish_name}")
            SlotSet("exists",None)
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
        dispatcher.utter_message(f" You will need the following ingredients for this step:")
        ingd_step = ""
        for igd in steps[stepCtr]['ingredients']:
            ingd_step += f"{igd['igd_qty']} {igd['igd_name']}, "
        dispatcher.utter_message(f"{ingd_step}")
        
        dispatcher.utter_message(f"{steps[stepCtr]['instruct']}")

        date = datetime.datetime.now() + datetime.timedelta(seconds=int(steps[stepCtr]['time']))
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

        global stepCtr
        stepCtr+=1
        if stepCtr<no_of_steps:
            return [FollowupAction(name="action_set_reminder")]
        else:
            return []