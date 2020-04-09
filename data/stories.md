## one-go path
* greet
  - utter_greet
  - utter_introduction
* affirm
  - action_random_article
* article_summary
  - action_get_summary
* goodbye
  - utter_goodbye

## no summary path
* greet
  - utter_greet
  - utter_introduction
* affirm
  - action_random_article
* goodbye
  - utter_goodbye

## more headlines path
* greet
  - utter_greet
  - utter_introduction
* affirm
  - action_random_article
* random_article
  - action_random_article
* article_summary
  - action_get_summary
* goodbye
  - utter_goodbye

## select article path
* show_articles
 - utter_article_selection