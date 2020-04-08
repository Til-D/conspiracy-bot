# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd


class ActionRandomArticle(Action):

    def name(self) -> Text:
        return "action_random_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = pd.read_csv("./data/Infobot_chat_script_formatted.csv")
        randomArticle = data.sample()
        headline = randomArticle.iloc[0]['headline']
        img = randomArticle.iloc[0]['image']

        dispatcher.utter_message(text=headline, image=img)

        return []
