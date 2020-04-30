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

ARTICLES = '[{"id": "d1", "headline": "Defeated Activist Greta Whines Climate Strikes Have \\u2018Achieved Nothing,\\u2019 Claims People Are \\u2018Dying Today\\u2019", "summary": "In December, far-left activist Greta Thunberg struck a somber, defeatist tone while speaking to fellow climate activists gathered at the United Nations climate talks in Madrid, Spain. Thunberg claimed that people are currently \\u201csuffering and dying\\u201d due to effects of supposed man-made climate change. Since 2017, Thunberg has been pushed by politicos on the far-left and their allies in the media to lead the climate change agenda, which conveniently promotes socialist policies as solutions.", "link": "https://www.dailywire.com/news/defeated-greta-whines-climate-strikes-have-achieved-nothing-claims-people-are-dying-today", "image": "https://dw-wp-production.imgix.net/2019/12/Screen-Shot-2019-12-06-at-8.28.29-PM.png?auto=format&fit=crop&ixlib=react-8.6.4&h=546&w=970&q=75&dpr=1"}, {"id": "d2", "headline": "Sadiq Khan to Blow \\u00a350m on \\u2018Green New Deal\\u2019 Instead of Police as London Gripped by Crime Wave", "summary": "London assembly member David Kurten grilled London mayor Sadiq Khan on his decision to plough tens of millions of pounds into a \\u201cGreen New Deal\\u201d while violent crime spirals in London. Kurten said that money could have \\u201cpaid for up to 800 extra police officers\\u201d to keep streets safe. In September of 2019, a 16-strong knife gang had targetted a group of young athletes in London\\u2019s Finsbury Park, robbing and threatening to kill the three white people in the group but telling the black people with them \\u201cYou\\u2019re good.\\u201d", "link": "https://www.breitbart.com/europe/2020/02/25/sadiq-khan-blow-50m-green-new-deal-instead-police/", "image": "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"}, {"id": "d3", "headline": "Pete Buttigieg Falsely Claims That Climate Change Doomsday Deadline Is \\u20182020\\u2019", "summary": "Claim: Pete Buttigieg said during Wednesday\\u2019s debate in Las Vegas, Nevada, that the climate change doomsday deadline is now and asserted that \\u201cwe will never meet any of the other scientific or policy deadlines that we need to\\u201d if the country does not elect someone who will take action. Verdict: False. Climate change alarmists have been reconfiguring the so-called \\u201cdoomsday\\u201d clock for years and have 50 years\\u2019 worth of failed predictions\\u2014 predictions that faltered as the country continued to progress and reach its policy goals.", "link": "https://www.breitbart.com/politics/2020/02/20/pete-buttigieg-says-climate-change-doomsday-deadline-2020/", "image": "https://media.breitbart.com/media/2017/03/protesters-activist-march-against-climate-change-getty-640x480.jpg"}, {"id": "d4", "headline": "NASA and NOAA\\u2019S latest climate warning is a result of purposefully flawed data.", "summary": "NASA and NOAA announced that 2019 was the second warmest year since modern record keeping began in 1880. But as has been hammered home repeatedly over the years by meteorologist Anthony Watts  (who is also a Senior Fellow with The Heartland Institute), rather than cite data from their best sources, NASA and NOAA chose to use severely compromised data from temperature readings adjusted\\u2014in a process called \\u201chomogenization\\u201d\\u2014they and others gathered from biased monitoring stations. Numerous reports have shown data manipulation is not limited to the United States, but is common across the globe.", "link": "https://www.heartland.org/news-opinion/news/nasa-and-noaas-latest-climate-warning-is-a-result-of-purposefully-flawed-data", "image": "https://www.heartland.org/sebin/h/n/Climate.jpg"}, {"id": "a1", "headline": "Greta Thunberg nominated for a Nobel Peace Prize for her efforts to prevent Climate Change", "summary": "Two lawmakers in Sweden have nominated Swedish teenage climate activist Greta Thunberg for the 2020 Nobel Peace Prize. Jens Holm and Hakan Svenneling, who are both members of the Sweden\\u2019s Left Party, said Monday that Greta \\u201chas worked hard to make politicians open their eyes to the climate crisis\\u201d and \\u201caction for reducing our emissions and complying with the Paris agreement is therefore also an act of making peace.\\u201d", "link": "https://www.washingtonpost.com/lifestyle/kidspost/greta-thunberg-nominated-for-nobel-peace-prize/2020/02/03/d296c146-46a7-11ea-ab15-b5df3261b710_story.html?itid=lk_inline_manual_1", "image": "https://specials-images.forbesimg.com/imageserve/1193255203/960x0.jpg"}, {"id": "a2", "headline": "Study: global banks \'failing miserably\' on climate crisis by funnelling trillions into fossil fuels", "summary": "The world\\u2019s largest investment banks have funnelled more than \\u00a32.2tn ($2.66tn) into fossil fuels since the Paris agreement, new figures show, prompting warnings they are failing to respond to the climate crisis. Analysis of the 35 leading global investment banks, by an alliance of US-based environmental groups, said that financing for the companies most aggressively expanding in new fossil fuel extraction since the Paris agreement has surged by nearly 40% in the last year.", "link": "https://www.theguardian.com/environment/2020/mar/18/global-banks-climate-crisis-finance-fossil-fuels", "image": "https://i.guim.co.uk/img/media/c95b9c44d2928658e93051bb30d4b71ad3a71c6d/67_0_3366_2022/master/3366.jpg?width=620&quality=45&auto=format&fit=max&dpr=2&s=0d1c02141e9febce06aa6f3d2ea6bc26"}, {"id": "a3", "headline": "Fact checking the false claim about the role of Arson in Australia\\u2019s Bushfires", "summary": "Claim: Various claims online suggest that climate change hasn\\u2019t contributed to the bushfires ravaging the East Coast of Australia, pinning the blame instead on arson. Verdict: False. Australian Bureau of Meteorology said that the second half of 2019 was particularly dry across most of the southern half of Australia, and followed several years of below average rainfall over parts of Queensland and New South Wales. Those hot, dry conditions allowed for one of the most severe fire seasons on Australia\\u2019s East Coast in decades. \\u201cThere are fingerprints of climate change in all of these blazes that really can\\u2019t be denied,\\u201d Jennifer Marlon, a research scientist at the Yale School of Forestry & Environmental Studies said in an interview.", "link": "https://www.factcheck.org/2020/01/setting-the-record-straight-on-climate-change-and-arson-in-australias-bushfires/", "image": "https://cdn.factcheck.org/UploadedFiles/Fires3-415x355.jpg"}, {"id": "a4", "headline": "Greenland, Antarctica Melting Six Times Faster Than in the 1990s", "summary": "Observations from 11 satellite missions monitoring the Greenland and Antarctic ice sheets have revealed that the regions are losing ice six times faster than they were in the 1990s. If the current melting trend continues, the regions will be on track to match the \\"worst-case\\" scenario of the Intergovernmental Panel on Climate Change (IPCC) of an extra 6.7 inches (17 centimetres) of sea level rise by 2100. The findings, published in the journal Nature from an international team of 89 polar scientists from 50 organizations, are the most comprehensive assessment to date of the changing ice sheets.", "link": "https://climate.nasa.gov/news/2958/greenland-antarctica-melting-six-times-faster-than-in-the-1990s/", "image": "https://imagecache.jpl.nasa.gov/images/640x350/greenland20200316-16-640x350.jpg"}, {"id": "p1", "headline": "AOC deletes gleeful tweet on oil industry\'s coronavirus collapse: \'You absolutely love to see it\'", "summary": "Rep. Alexandria Ocasio-Cortez faced a torrent of social-media backlash on Monday after tweeting her \\u201clove\\u201d for the oil industry\\u2019s pandemic-prompted implosion. News that oil prices have spiralled into \\u201cnegative values\\u201d prompted the New York Democrat to send out a gleeful tweet to her 6.7 million followers. \\u201cYou absolutely love to see it,\\u201d she tweeted. The message was soon deleted and replaced. Critics noted the stark contrast in rhetoric. Some responses include: \\u201cCheering for the collapse of an industry that supports millions of people is a perfect example of why your proposal has failed to garner meaningful support.\\u201d and \\u201cYou\\u2019re literally basking in the pink slips of American workers. Disgraceful.\\u201d", "link": "https://www.washingtontimes.com/news/2020/apr/20/aoc-deletes-gleeful-tweet-on-oil-industrys-coronav/", "image": "https://twt-thumbs.washtimes.com/media/image/2020/01/26/Election_2020_Bernie_Sanders_60461.jpg-4e768_c0-379-5472-3569_s885x516.jpg?79beb960f0e00b628bd5fdbfd870ccee1dbf2e2a"}, {"id": "p2", "headline": "Covid-19 Highlights Trump\\u2019s Malignant Narcissism \\u2014 And Proves Americans Will Survive Despite Him", "summary": "Major catastrophes lay bare the truth about our leaders. Trump\\u2019s criminally negligent, chaotic handling of the Covid-19 pandemic has exposed, once and for all, that he is a corrupt, narcissistic psychopath. Because of COVID-19, the nation now recognizes what should have been obvious ever since Trump took office: His first response to every crisis is to insist on complete authority, while at the same time abandoning all responsibility. Despite his inaction and incompetence, he won\\u2019t relinquish control over the government\\u2019s resources to those who know how to use them. Thus, in the total absence of national leadership or direction, governors have had to take charge, leading Trump to lash out at them.", "link": "https://theintercept.com/2020/04/22/trump-coronavirus-governors/", "image": "https://theintercept.imgix.net/wp-uploads/sites/1/2020/04/GettyImages-1210379159.jpg?auto=compress%2Cformat&q=90&w=1024&h=683"}, {"id": "b1", "headline": "Pope Francis Disgraces Himself with Coronavirus-Climate change Blood Libel", "summary": "Pope Francis said he believes the Chinese coronavirus pandemic is \\u201ccertainly nature\\u2019s response\\u201d to humanity\\u2019s failure to address the \\u201cpartial catastrophes\\u201d wrought by human-induced climate change. Pope Francis blaming the coronavirus epidemic on humanity, specifically humanity\\u2019s failure to address Climate Change (which is a hoax) is nothing short of a blood libel. This is absolutely disgraceful. This is no different than blaming this China virus plague on abortion or homosexuality, which is something we have heard from the fringes during other human tragedies and disasters.", "link": "https://www.breitbart.com/faith/2020/04/09/nolte-pope-francis-disgraces-himself-with-coronavirus-blood-libel/", "image": "https://media.breitbart.com/media/2017/11/Pope-Weinandy-640x480.jpg"}, {"id": "b2", "headline": "Fall in COVID-linked carbon emissions won\\u2019t halt climate change - UN weather agency chief", "summary": "An expected drop in greenhouse gas emissions linked to the global economic crisis caused by the COVID-19 pandemic is only \\u201cshort-term good news\\u201d, said Professor Petteri Taalas, World Meteorological Organization (WMO) Secretary-General, in reference to a 5.5 to 5.7 per cent fall in levels of carbon dioxide due to the pandemic, that have been flagged by leading climate experts, including the Center for International Climate Research. \\u201cThere might even be a boost in emissions because some of the industries have been stopped\\u201d, the WMO head cautioned. Latest data from WMO published to coincide with the 50th anniversary of Earth Day, on 22 April, indicates that carbon dioxide (CO2) levels and other greenhouse gases in the atmosphere rose to new records last year.", "link": "https://news.un.org/en/story/2020/04/1062332", "image": "https://global.unitednations.entermediadb.net/assets/mediadb/services/module/asset/downloads/preset/Libraries/Production+Library/02-03-2020-Mogobane-Botswana.jpg/image1170x530cropped.jpg"}, {"id": "c1", "headline": "Michael Moore-backed \\u2018Planet of the Humans\\u2019 Takes Apart the Left\\u2019s Green Energy Scams", "summary": "Left-wing filmmaker Michael Moore released a new documentary, Planet of the Humans, on Tuesday, ahead of the 50th Earth Day on Apr. 22. Like most Moore projects, it targets corporate greed and hypocrisy. But this time, the greed and hypocrisy it targets are on the environmentalist left. The film exposes the solar and wind energy industries as scams that pretend to be saving the planet from climate change while consuming more fossil fuels than they save, and causing ecological damage.", "link": "https://www.breitbart.com/environment/2020/04/22/michael-moore-backed-planet-of-the-humans-takes-apart-the-lefts-green-energy-scams/", "image": "https://media.breitbart.com/media/2020/01/BernieIowacelebs1-640x480.jpg"}, {"id": "c2", "headline": "Documentary Endorsing Human-made Climate Change Released on Earth Day", "summary": "Planet of the Humans takes a harsh look at how the environmental movement has lost the battle through well-meaning but disastrous choices, including the belief that solar panels and windmills would save us, and by giving in to the corporate interests of Wall Street. Moore and Gibbs say they decided that with the American public \\u2013 and much of the world \\u2013 confined to their homes amid the coronavirus pandemic \\u201cand suddenly having to consider the role humans and their behavior have played in our fragile ecosystems, the moment was too urgent to wait until later this year for the film\\u2019s planned release.\\u201d", "link": "https://deadline.com/2020/04/michael-moore-releases-planet-of-the-humans-documentary-eve-earth-day-1202913761/", "image": "https://postmediacanoe.files.wordpress.com/2020/04/documentary_78120372-e1587497118429.jpg"}]'
MIN_ARTICLES_TO_READ = 4
LOGFILE = 'log_conspiracy_conversations.csv'
URL_SURVEY = 'https://www.qualtrics.com/'
SALT = 'conspiracy' # used to create unique user id (uuid)
HASH_MAX_INDEX = 5

def logUserAction(uuid, pid, fn, articleId):
    if(not path.exists(LOGFILE)):
        with open(LOGFILE, "a") as f:
            f.write('%s;%s;%s;%s;%s\n' % ('uuid', 'pid', 'function', 'articleId', 'timestamp'))
            f.close()    
    with open(LOGFILE, "a") as f:
        f.write('%s;%s;%s;%s;%s\n' % (uuid, pid, fn, articleId, datetime.now()))
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

        # filepath_server = '/etc/rasa/Infobot_chat_script_formatted.csv'
        # filepath_local = './data/Infobot_chat_script_formatted.csv'

        # dataSheet = [row for row in csv.DictReader(open(filepath_server))]

        dataSheet = json.loads(ARTICLES)
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
            logUserAction(uuid, pid, 'no_more_articles', str(articlesRead))
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
            logUserAction(uuid, pid, self.name(), nextArticleId)

        return [SlotSet("article_sequence", sequence), SlotSet("article_index", index)]


class ActionGetSummary(Action):

    def name(self) -> Text:
        return "action_get_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        articleId = tracker.get_slot('article_id')

        # filepath_server = '/etc/rasa/Infobot_chat_script_formatted.csv'
        # filepath_local = './data/Infobot_chat_script_formatted.csv'

        # dataSheet = [row for row in csv.DictReader(open(filepath_server))]
        dataSheet = json.loads(ARTICLES)

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
                
                dispatcher.utter_message(text="{}".format(article['summary']), type= 'mrkdwn')
                dispatcher.utter_message(text="Once you're done reading you can return to the final part of the survey.")
                dispatcher.utter_message(text='To get back to the survey you can simply close this window.')
                dispatcher.utter_message(template="utter_goodbye")
            else:
                responseSelections = [
                {"title": 'Yes, please!', "payload": '/show_articles'}
                     ]
                dispatcher.utter_message(text="{}".format(article['summary']), type= 'mrkdwn', buttons=responseSelections)
                dispatcher.utter_message(text='Want more news?')

            
            # dispatcher.utter_message(text="{}".format(article['headline']), type= 'mrkdwn')
            
            logUserAction(uuid, pid, self.name(), article['id'])

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

        pid = tracker.sender_id;
        articlesRead = tracker.get_slot('articles_read')
        dataSheet = json.loads(ARTICLES)
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
        logUserAction(uuid, pid, self.name(), ','.join(ids))
        dispatcher.utter_message(text="Here are some articles for you! Click on the headline to get a summary.", json_message={"payload":"cardsCarousel","data": articles})

        return [SlotSet("uuid", uuid)]