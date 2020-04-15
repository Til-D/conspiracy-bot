# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
from os import path
from datetime import datetime

import csv
import random
import json

ARTICLES = '[{"id": "d1", "headline": "Defeated Activist Greta Whines Climate Strikes Have \\u2018Achieved Nothing,\\u2019 Claims People Are \\u2018Dying Today\\u2019", "summary": "In December, far-left activist Greta Thunberg struck a somber, defeatist tone while speaking to fellow climate activists gathered at the United Nations climate talks in Madrid, Spain. Thunberg claimed that people are currently \\u201csuffering and dying\\u201d due to effects of supposed man-made climate change. Since 2017, Thunberg has been pushed by politicos on the far-left and their allies in the media to lead the climate change agenda, which conveniently promotes socialist policies as solutions.", "link": "https://www.dailywire.com/news/defeated-greta-whines-climate-strikes-have-achieved-nothing-claims-people-are-dying-today", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Greta_Thunberg_au_parlement_europ%C3%A9en_%2833744056508%29%2C_recadr%C3%A9.png/330px-Greta_Thunberg_au_parlement_europ%C3%A9en_%2833744056508%29%2C_recadr%C3%A9.png"}, {"id": "d2", "headline": "Sadiq Khan to Blow \\u00a350m on \\u2018Green New Deal\\u2019 Instead of Police as London Gripped by Crime Wave", "summary": "London assembly member David Kurten grilled London mayor Sadiq Khan on his decision to plough tens of millions of pounds into a \\u201cGreen New Deal\\u201d while violent crime spirals in London. Kurten said that money could have \\u201cpaid for up to 800 extra police officers\\u201d to keep streets safe. In September of 2019, a 16-strong knife gang had targetted a group of young athletes in London\\u2019s Finsbury Park, robbing and threatening to kill the three white people in the group but telling the black people with them \\u201cYou\\u2019re good.\\u201d", "link": "https://www.breitbart.com/europe/2020/02/25/sadiq-khan-blow-50m-green-new-deal-instead-police/", "image": "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"}, {"id": "d3", "headline": "Pete Buttigieg Falsely Claims That Climate Change Doomsday Deadline Is \\u20182020\\u2019", "summary": "Claim: Pete Buttigieg said during Wednesday\\u2019s debate in Las Vegas, Nevada, that the climate change doomsday deadline is now and asserted that \\u201cwe will never meet any of the other scientific or policy deadlines that we need to\\u201d if the country does not elect someone who will take action. Verdict: False. Climate change alarmists have been reconfiguring the so-called \\u201cdoomsday\\u201d clock for years and have 50 years\\u2019 worth of failed predictions\\u2014 predictions that faltered as the country continued to progress and reach its policy goals.", "link": "https://www.breitbart.com/politics/2020/02/20/pete-buttigieg-says-climate-change-doomsday-deadline-2020/", "image": "https://i.guim.co.uk/img/media/b0da101ca411f696646587ea968f60e638a9a387/0_36_2292_1375/master/2292.jpg?width=620&quality=45&auto=format&fit=max&dpr=2&s=081c711e6858e3c1bcadf94e5a153ea0"}, {"id": "d4", "headline": "NASA and NOAA\\u2019S latest climate warning is a result of purposefully flawed data.", "summary": "NASA and NOAA announced that 2019 was the second warmest year since modern record keeping began in 1880. But as has been hammered home repeatedly over the years by meteorologist Anthony Watts  (who is also a Senior Fellow with The Heartland Institute), rather than cite data from their best sources, NASA and NOAA chose to use severely compromised data from temperature readings adjusted\\u2014in a process called \\u201chomogenization\\u201d\\u2014they and others gathered from biased monitoring stations. Numerous reports have shown data manipulation is not limited to the United States, but is common across the globe.", "link": "https://www.heartland.org/news-opinion/news/nasa-and-noaas-latest-climate-warning-is-a-result-of-purposefully-flawed-data", "image": "https://climate.nasa.gov/system/content_pages/main_images/1321_cc-vs-gw-vs-wx-768px.jpg"}, {"id": "a1", "headline": "Greta Thunberg nominated for a Nobel Peace Prize for her efforts to prevent Climate Change", "summary": "Two lawmakers in Sweden have nominated Swedish teenage climate activist Greta Thunberg for the 2020 Nobel Peace Prize. Jens Holm and Hakan Svenneling, who are both members of the Sweden\\u2019s Left Party, said Monday that Greta \\u201chas worked hard to make politicians open their eyes to the climate crisis\\u201d and \\u201caction for reducing our emissions and complying with the Paris agreement is therefore also an act of making peace.\\u201d", "link": "https://www.washingtonpost.com/lifestyle/kidspost/greta-thunberg-nominated-for-nobel-peace-prize/2020/02/03/d296c146-46a7-11ea-ab15-b5df3261b710_story.html?itid=lk_inline_manual_1", "image": "https://specials-images.forbesimg.com/imageserve/1193255203/960x0.jpg?fit=scale"}, {"id": "a2", "headline": "Study: global banks \'failing miserably\' on climate crisis by funnelling trillions into fossil fuels", "summary": "The world\\u2019s largest investment banks have funnelled more than \\u00a32.2tn ($2.66tn) into fossil fuels since the Paris agreement, new figures show, prompting warnings they are failing to respond to the climate crisis. Analysis of the 35 leading global investment banks, by an alliance of US-based environmental groups, said that financing for the companies most aggressively expanding in new fossil fuel extraction since the Paris agreement has surged by nearly 40% in the last year.", "link": "https://www.theguardian.com/environment/2020/mar/18/global-banks-climate-crisis-finance-fossil-fuels", "image": "https://www.thebalance.com/thmb/EkAve7viun3r_zUE-4Wk1aK0j_E=/300x200/filters:saturation(0.2):brightness(10):contrast(5):no_upscale():format(webp)/Investing-in-Bank-Stocks-56a093433df78cafdaa2d88a.jpg"}, {"id": "a3", "headline": "Fact checking the false claim about the role of Arson in Australia\\u2019s Bushfires", "summary": "Claim: Various claims online suggest that climate change hasn\\u2019t contributed to the bushfires ravaging the East Coast of Australia, pinning the blame instead on arson. Verdict: False. Australian Bureau of Meteorology said that the second half of 2019 was particularly dry across most of the southern half of Australia, and followed several years of below average rainfall over parts of Queensland and New South Wales. Those hot, dry conditions allowed for one of the most severe fire seasons on Australia\\u2019s East Coast in decades. \\u201cThere are fingerprints of climate change in all of these blazes that really can\\u2019t be denied,\\u201d Jennifer Marlon, a research scientist at the Yale School of Forestry & Environmental Studies said in an interview.", "link": "https://www.factcheck.org/2020/01/setting-the-record-straight-on-climate-change-and-arson-in-australias-bushfires/", "image": "https://mgnsw.org.au/wp-content/uploads/2019/11/11443527473_a33ec74d9f_k.jpg"}, {"id": "a4", "headline": "Greenland, Antarctica Melting Six Times Faster Than in the 1990s", "summary": "Observations from 11 satellite missions monitoring the Greenland and Antarctic ice sheets have revealed that the regions are losing ice six times faster than they were in the 1990s. If the current melting trend continues, the regions will be on track to match the \\"worst-case\\" scenario of the Intergovernmental Panel on Climate Change (IPCC) of an extra 6.7 inches (17 centimetres) of sea level rise by 2100. The findings, published in the journal Nature from an international team of 89 polar scientists from 50 organizations, are the most comprehensive assessment to date of the changing ice sheets.", "link": "https://climate.nasa.gov/news/2958/greenland-antarctica-melting-six-times-faster-than-in-the-1990s/", "image": "https://cdn.britannica.com/s:700x500/08/135708-050-2346C1CF/Paradise-Bay-Antarctica.jpg"}]'
MIN_ARTICLES_TO_READ = 4
LOGFILE = 'log_conspiracy_conversations.csv'

def logUserAction(uid, fn, articleId):
    if(not path.exists(LOGFILE)):
        with open(LOGFILE, "a") as f:
            f.write('%s;%s;%s;%s\n' % ('uid', 'function', 'articleId', 'timestamp'))
            f.close()    
    with open(LOGFILE, "a") as f:
        f.write('%s;%s;%s;%s\n' % (uid, fn, articleId, datetime.now()))
        f.close()

    print("Log written: %s" % (os.getcwd()+'/'+LOGFILE))

class ActionRandomArticle(Action):

    def name(self) -> Text:
        return "action_random_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # filepath_server = '/etc/rasa/Infobot_chat_script_formatted.csv'
        # filepath_local = './data/Infobot_chat_script_formatted.csv'

        # dataSheet = [row for row in csv.DictReader(open(filepath_server))]

        dataSheet = json.loads(ARTICLES)
        print(dataSheet)

        # check if article sequence is initialized otherwise randomize 

        sequence = tracker.get_slot('article_sequence')
        index = tracker.get_slot('article_index')
        uid = tracker.get_slot('uid')
        
        if(sequence is not None and index is not None):
            print('+ Article sequence already initialized.')
            # sequence = json.loads(sequence)
            index += 1
        else:
            print('- Initializing article sequence')
            sequence = [item['id'] for item in dataSheet]
            random.shuffle(sequence)
            index = 0

        # print('article index: %d' % index)
        # print('article sequence: %s' % json.dumps(sequence))

        if(sequence and index >= len(sequence)): # That's it, no more articles
            sequence = None
            index = None
            dispatcher.utter_message(text="That's it. These are all the articles I've got.")
        else:
            nextArticleId = sequence[index]
            randomArticle = [item for item in dataSheet if item['id']==nextArticleId][0]

            print('Retrieved article: (id: %s) %s' % (randomArticle['id'], randomArticle['headline']))
            print('Index: %d' % index)
            print('Article sequence: %s' % json.dumps(sequence))

            # with links:
            # mrkdown = '[{}]({})'.format(randomArticle['headline'], randomArticle['link'])

            # without links:
            mrkdown = '{}'.format(randomArticle['headline'])

            dispatcher.utter_message(text=mrkdown, image=randomArticle['image'], type= 'mrkdwn')

            responseSelections = [
                {"title": "Yes", "payload": '/article_summary'},
                {"title": "No. Give me another article.", "payload": '/random_article'}
                     ]

            dispatcher.utter_message(template="utter_want_summary", buttons=responseSelections)
            logUserAction(uid, self.name(), nextArticleId)

        return [SlotSet("article_sequence", sequence), SlotSet("article_index", index)]


class ActionGetSummary(Action):

    def name(self) -> Text:
        return "action_get_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # filepath_server = '/etc/rasa/Infobot_chat_script_formatted.csv'
        # filepath_local = './data/Infobot_chat_script_formatted.csv'

        # dataSheet = [row for row in csv.DictReader(open(filepath_server))]
        dataSheet = json.loads(ARTICLES)

        sequence = tracker.get_slot('article_sequence')
        index = tracker.get_slot('article_index')
        uid = tracker.get_slot('uid')
        
        if(sequence is not None and index is not None):
            articleId = sequence[index]
        
            print('Retrieved article id: %s' % articleId)
            article = {
                'summary': 'article not found'
            }
            for item in dataSheet:
                if(item['id']==articleId):
                    article = item
                    break

            print(article['headline'])

            if(index<MIN_ARTICLES_TO_READ):
                title = 'We have more articles for you! Click here!'
            else:
                title = 'Want more news?'

            responseSelections = [
                {"title": title, "payload": '/random_article'}
                     ]
            # dispatcher.utter_message(text="{}".format(article['headline']), type= 'mrkdwn')
            dispatcher.utter_message(text="{}".format(article['summary']), type= 'mrkdwn', buttons=responseSelections)
            logUserAction(uid, self.name(), article['id'])

        else:
            dispatcher.utter_message(text="Mhm.... I don't have a summary for this article.")
            dispatcher.utter_message(template="utter_introduction")

        return []