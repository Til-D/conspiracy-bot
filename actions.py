# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this gpide on how to implement these action:
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
import time
import hashlib 

ARTICLES = '[{"id": "1", "headline": "COVID-19 virus was not manufactured in a lab", "summary": "Coronaviruses exist in nature and can infect many different creatures. SARS-like coronaviruses are found in bats, pigs, cats, and ferrets, etc. The most widely agreed upon origin of SARS-CoV-2 is that its ancestors moved around in wild animals\\u2014swapping genetic features as they went along\\u2014before they jumped into humans. The virus may have moved directly into people from bats, or first jumped into another animal, such as a pangolin, before transitioning into humans.", "link": "", "image": "1.jpeg"}, {"id": "2", "headline": "Fact-check: Bill Gates is not responsible for Covid-19", "summary": "A false claim that the Covid-19 pandemic was planned by Bill Gates is circulating on the internet based on an old quote by Gates about pandemic readiness. There is no evidence that the pandemic was deliberately planned or that Bill Gates has any links with such a plan. Covid-19 is believed to have spread from an animal to a person much like MERS and SARS and there is no indication or publicly available evidence suggesting that the coronavirus was \\"designed\\".", "link": "", "image": "2.jpeg"}, {"id": "3", "headline": "Natural herd immunity is not a viable option for protection against the coronavirus", "summary": "Experts estimate that roughly 60 to 70 percent of people would need to get COVID-19 for herd immunity to be possible. Given the high mortality rate of the disease, letting it infect that many people could lead to millions of deaths. As is evidenced in two countries that tried this approach early on in the pandemic, the U.K.\\u2019s COVID-19 death rate is among the world\\u2019s highest whereas Sweden has had significantly more deaths than neighbouring countries, and its economy has suffered despite the lack of a shutdown.", "link": "", "image": "3.png"}, {"id": "4", "headline": "Instagram post wrongly claims that Covid-19 death reports are exaggerated", "summary": "An Instagram post from Robert F. Kennedy Jr., wrongly claims that the Centers for Disease Control and Prevention is reporting all pneumonia and influenza deaths as caused by Covid-19. The CDC has for years monitored deaths of pneumonia and influenza together as one measure of the flu\\u2019s mortality. As of an update on Jan 29, the provisional death count reported 431,619 deaths attributed to Covid-19 in the US. Kennedy\\u2019s post is wrong that the CDC is simply reporting \\u201cthem all as Covid deaths.\\u201d If that was true, the reported Covid-19 death count would be much higher.", "link": "", "image": "4.jpeg"}, {"id": "5", "headline": "Covid-19 vaccines don\\u2019t change your DNA", "summary": "Some recent news articles claim that high-profile figures like Bill Gates and Robert F. Kennedy Jr have warned that Covid-19 vaccines can change a person\'s DNA. This is false; mRNA vaccines - the type of vaccines developed for Covid-19, deliver genetic instructions to build these proteins directly into the cells, effectively turning the body into a vaccine-making factory. However, they do not change a person\\u2019s DNA because all the processes involved happen in the cytoplasm, while the DNA is stored in a different part of the cell called nucleus.", "link": "", "image": "5.jpeg"}, {"id": "6", "headline": "Video shared on Facebook inflates risk of Moderna vaccine 40-fold", "summary": "Social media posts are spreading an inaccurate claim about the safety of the Moderna coronavirus vaccine. With the headline, \\"Do not take the vaccine,\\" a video post features James Lyons-Weiler giving this dire assessment of the Moderna vaccine trial data. He said that \\u201c21% of people are having serious adverse events from this vaccine\\", but the actual number is 0.5% and that was the same level for the placebo group. Therefore, there is no indication the vaccine caused any of these serious events.", "link": "", "image": "6.jpeg"}, {"id": "7", "headline": "Covid-19 Vaccines Don\\u2019t Have Patient-Tracking Devices", "summary": "A video circulating on social media wrongly claims that vaccines for Covid-19 have a microchip that \\u201ctracks the location of the patient.\\u201d This is a false claim because such chips are designed only to know exactly that the right dose hasn\\u2019t expired. The chip only refers to the dose \\u2014 there\\u2019s no personal information and it cannot be injected into a patient. It\\u2019s also worth noting that such syringes aren\\u2019t currently being used for COVID-19 vaccines.", "link": "", "image": "7.jpeg"}, {"id": "8", "headline": "Video Misinterprets Fauci\\u2019s Comments on Covid-19 Vaccine", "summary": "A CNN interview with Dr. Anthony Fauci is being misrepresented to falsely suggest that a Covid-19 vaccine authorized in the U.S doesn\\u2019t \\u201cprotect you from covid.\\u201d The vaccine does protect against Covid -19, but it may not prevent someone from contracting the virus. While for most individuals, the coronavirus symptoms are relatively mild. But in some patients, particularly those who are older or who have certain health conditions, Covid-19 can be deadly. Fauci was referring to the ability of the vaccine to prevent such a severe case of Covid-19.", "link": "", "image": "8.jpeg"}, {"id": "9", "headline": "French Nobel prize winner: \\u2018Covid-19 made in lab\\u2019", "summary": "Professor Luc Montagnier has accused biologists of having created SARS-CoV-2 - the virus that causes Covid-19 - in a lab. The scientist, who won the Nobel Prize in 2008 for his work on HIV said in an interview this week that the virus has come out of a laboratory in Wuhan, which has been specialising in these types of coronaviruses since the beginning of the 2000s. He also added that molecular biologists have inserted DNA sequences from HIV into a coronavirus, probably as part of their work to find a vaccine against AIDS.", "link": "", "image": "9.jpeg"}, {"id": "10", "headline": "Covid-19 Testing Fraud: Elite using Chinese tests to manufacture a pandemic", "summary": "The Covid-19 pandemic has shown us how easy it is to manufacture panic and control entire populations through deceptive means. The false appearance of a lethal pandemic has been manufactured by using a test that was developed based on a genetic sequence published by Chinese scientists. PCR tests cannot distinguish between \\"live\\" viruses and noninfectious viral particles and therefore cannot be used as a diagnostic tool. The flaws of Covid testing have been capitalized upon to incite fear in order to benefit the Great Reset agenda developed by a technocratic elite.", "link": "", "image": "10.jpeg"}, {"id": "11", "headline": "Peer reviewed article warns against bodily control devices inside Covid vaccine", "summary": "An article on how the pandemic facilitated a financial, tech, biopharmaceutical and military-intelligence push for centralized, technocratic control has been accepted by the International Journal of Vaccine Theory, Practice and Research. According to the article, \\u201cthe evidence suggests that Trojan horse coronavirus vaccines may challenge bodily integrity and informed consent in entirely new ways, transporting invasive technologies into people\'s brains and bodies\\u201d and that \\u201cthree increasingly interwoven sectors (Big Finance, Big Tech, and Big Pharma) are reaping rewards from Covid-19.\\"", "link": "", "image": "11.jpeg"}, {"id": "12", "headline": "Top Medical Inventor: Covid mRNA \\u201cVaccine\\u201d Not A Vaccine", "summary": "Medical inventor and author David Martin proves that the Pfizer and Moderna vaccines are not vaccines by medical definition and that Big Pharma is forcing these untested gene therapies onto us. He states that vaccines are defined as \\u2018a product that stimulates a person\\u2019s immune system to produce immunity to a specific disease, protecting the person from that disease\\u2019. Since the Moderna and Pfizer \\u201calleged vaccine\\u201d trials have explicitly acknowledged that their gene therapy technology has no impact on viral infection or transmission, their products cannot be considered vaccines.", "link": "", "image": "12.jpeg"}]'
# one-sided bot: presents a selection of eight news headlines only aimed at debunking COVID-19 related conspiracy theories.
ARTICLES_ONE_SIDED_GENERAL = ['1', '2', '3', '4']
ARTICLES_ONE_SIDED_COVID = ['5', '8', '6', '7']
articles_one_sided = [article for article in json.loads(ARTICLES) if article['id'] in (ARTICLES_ONE_SIDED_GENERAL + ARTICLES_ONE_SIDED_COVID)]

    # balanced bot: presents a selection of eight news headlines on COVID-19 related conspiracy theories, four of which debunk conspiracy theories while four support them.
ARTICLES_BALANCED_SUPPORT_GENERAL = ['9', '10']
ARTICLES_BALANCED_SUPPORT_COVID = ['11', '12'] # used 12 instead of the specified 8

# shuffle article selection: ensure that the 4 debunking articles are being randomly presented from a larger selection of 8 debunking articles
quasi_random_articles = ARTICLES_BALANCED_SUPPORT_GENERAL + ARTICLES_BALANCED_SUPPORT_COVID + random.sample(ARTICLES_ONE_SIDED_GENERAL, 2) + random.sample(ARTICLES_ONE_SIDED_COVID, 2)
quasi_random_articles
articles_balanced = [article for article in json.loads(ARTICLES) if article['id'] in quasi_random_articles]

BOT_TYPES = {'A': articles_one_sided, 'B': articles_balanced}

MIN_ARTICLES_TO_READ = 4
LOGFILE = 'log_conspiracy_conversations_v2.csv'
URL_SURVEY = 'https://www.qualtrics.com/'
SALT = 'conspiracy' # used to create unique user id (uuid)
HASH_MAX_INDEX = 5
FOLLOW_UP_SURVEY_CODE = 'blue'

def logUserAction(uuid, pid, fn, articleId, botType):
    if(not path.exists(LOGFILE)):
        with open(LOGFILE, "a") as f:
            f.write('%s;%s;%s;%s;%s;%s\n' % ('uuid', 'pid', 'function', 'articleId', 'botType', 'timestamp'))
            f.close()    
    with open(LOGFILE, "a") as f:
        f.write('%s;%s;%s;%s;%s;%s\n' % (uuid, pid, fn, articleId, botType, datetime.now()))
        f.close()

    print("Log written: %s" % (os.getcwd()+'/'+LOGFILE))


# class ActionInstructions(Action):

#     def name(self) -> Text:
#         return "action_instructions"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(template="utter_greet")
#         dispatcher.utter_message(template="utter_introduction")

#         print('new user connected: ')       

#         return []


class ActionRandomArticle(Action):

    def name(self) -> Text:
        return "action_random_article"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        botType = tracker.get_slot('bot_type')
        dataSheet = BOT_TYPES[botType]

        # print(dataSheet)
        # check if article sequence is initialized otherwise randomize 

        sequence = tracker.get_slot('article_sequence')
        index = tracker.get_slot('article_index')
        articlesRead = tracker.get_slot('articles_read_count')
        pid = tracker.sender_id
        uuid = tracker.get_slot('uuid')
        
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
            dispatcher.utter_message(text='To get back to the survey you can simply close this window.')
            dispatcher.utter_message(template="utter_goodbye")
            logUserAction(uuid, pid, 'no_more_articles', str(articlesRead), botType)
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
            logUserAction(uuid, pid, self.name(), nextArticleId, botType)

        return [SlotSet("article_sequence", sequence), SlotSet("article_index", index)]


class ActionGetSummary(Action):

    def name(self) -> Text:
        return "action_get_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        articleId = tracker.get_slot('article_id')

        print("ActionGetSummary(), articleID: " + articleId)

        # filepath_server = '/etc/rasa/Infobot_chat_script_formatted.csv'
        # filepath_local = './data/Infobot_chat_script_formatted.csv'

        # dataSheet = [row for row in csv.DictReader(open(filepath_server))]

        botType = tracker.get_slot('bot_type')
        dataSheet = BOT_TYPES[botType]

        # dataSheet = json.loads(ARTICLES)

        sequence = tracker.get_slot('article_sequence')
        index = tracker.get_slot('article_index')
        articlesRead = tracker.get_slot('articles_read')
        pid = tracker.sender_id
        uuid = tracker.get_slot('uuid')

        if(articlesRead is None):
            articlesRead = []

        if(articleId is not None):
            
            # dispatcher.utter_message(text="Delivering this article: " + articleId, type= 'mrkdwn')

            print('retrieving article id: %s' % articleId)
            article = {
                'summary': 'article not found'
            }
            for item in dataSheet:
                if(item['id']==articleId):
                    article = item
                    break

            print(article['headline'])
            articlesRead.append(article['id'])

            if(len(articlesRead) >= MIN_ARTICLES_TO_READ):
                # index<MIN_ARTICLES_TO_READ):
                
                # dispatcher.utter_message(text="{}".format(article['summary']), type= 'mrkdwn')
                dispatcher.utter_message(json_message={"payload": "article", "articleId": articleId, "headline": article['headline'], "summary": "{}".format(article['summary']), "scrollToBottom": False})

                responseSelections = [
                {"title": 'Got it!', "payload": '/get_survey_code'}
                     ]
                dispatcher.utter_message(text="Once you're done, click here to obtain the code for the rest of the survey", buttons=responseSelections)
                
            else:
                responseSelections = [
                {"title": 'Yes, please!', "payload": '/show_articles'}
                     ]
                # dispatcher.utter_message(text="{}".format(article['summary']), type= 'mrkdwn', json_message={"articleId": articleId})
                dispatcher.utter_message(json_message={"payload": "article", "articleId": articleId, "headline": article['headline'], "summary": "{}".format(article['summary']), "scrollToBottom": False})
                dispatcher.utter_message(text='Want more news?', buttons=responseSelections)

            
            # dispatcher.utter_message(text="{}".format(article['headline']), type= 'mrkdwn')
            
            logUserAction(uuid, pid, self.name(), article['id'], botType)

        else:
            dispatcher.utter_message(text="Mhm.... I don't have a summary for this article.")
            dispatcher.utter_message(template="utter_introduction")
        
        
        # if(sequence is not None and index is not None):
        #     articleId = sequence[index]
        
        


        return [SlotSet("articles_read", articlesRead)]

class ActionShowAllArticles(Action):

    def name(self) -> Text:
        return "action_show_all_articles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pid = tracker.sender_id
        articlesRead = tracker.get_slot('articles_read')

        print("showAllArticles(), sender_id: " + pid)
        print(tracker)

        botType = tracker.get_slot('bot_type')

        if(botType is not None and botType in BOT_TYPES.keys()):
            print('-bot type set by url: ' + botType)
        else:
            botType = random.choice(BOT_TYPES.keys())
            print('-bot type randomly set: ' + botType)

        dataSheet = BOT_TYPES[botType]
        # dataSheet = json.loads(ARTICLES)

        uuid = tracker.get_slot('uuid')

        if(uuid is None):
            ts = str(time.time())
            uuid = hashlib.md5((SALT + ts).encode()).hexdigest()
            if(len(uuid)>HASH_MAX_INDEX):
                uuid = uuid[:HASH_MAX_INDEX]

        articles = []
        for article in dataSheet:
            articles.append({
                'id': article['id'],
                'name': article['headline'],
                'image': article['image']
                })

        # remote articles already read
        if(articlesRead is not None):
            articles = [article for article in articles if article['id'] not in articlesRead]

        print('%d articles unread' % len(articles))

        random.shuffle(articles)
        ids = [article['id'] for article in articles]
        logUserAction(uuid, pid, self.name(), ','.join(ids), botType)
        dispatcher.utter_message(text="Here are some articles for you! Click on the headline to get a summary.", json_message={"payload":"cardsCarousel","data": articles})

        return [SlotSet("uuid", uuid), SlotSet("bot_type", botType)]

class ActionGetSurveyCode(Action):

    def name(self) -> Text:
        return "action_get_survey_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("ActionGetSurveyCode()")

        botType = tracker.get_slot('bot_type')

        if(botType is not None and botType in BOT_TYPES.keys()):
            print('-bot type set by url: ' + botType)
        else:
            botType = random.choice(BOT_TYPES.keys())
            print('-bot type randomly set: ' + botType)

        pid = tracker.sender_id
        uuid = tracker.get_slot('uuid')

        dispatcher.utter_message(text="Your survey code is: " + FOLLOW_UP_SURVEY_CODE)
        dispatcher.utter_message(text='To continue with the survey you can simply close this window.')
        dispatcher.utter_message(template="utter_goodbye")

        logUserAction(uuid, pid, self.name(), '', botType)

        return []