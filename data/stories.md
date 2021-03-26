## website arrival path
* greet{"bot_type": "A"}
  - utter_greet
  - utter_introduction
* show_articles
  - action_show_all_articles
* article_summary{"article_id": "d1"}
  - action_get_summary
* get_survey_code
  - action_get_survey_code
* goodbye
  - utter_goodbye

## select article with survey code path
* show_articles
 - action_show_all_articles
* article_summary{"article_id": "d1"}
  - action_get_summary
* get_survey_code
  - action_get_survey_code

## select article path
* show_articles
 - action_show_all_articles
* article_summary{"article_id": "d1"}
  - action_get_summary