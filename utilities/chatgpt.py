from openai import OpenAI
from decouple import config
import os

CHATGPT_KEY = config("CHATGPT_KEY")
def calculate_article_impact_score(article_title, article_description):
    client = OpenAI(
        api_key = CHATGPT_KEY
    )

    prompt = f"""
    Given this news headline and description:
    - Title: {article_title}
    - Description: {article_description}
    Does this news significantly impact global **stock markets**? If yes, provide a short explanation (max 50 words).
    From a score of 0 to 100, give me a score of how this news can impact the global stock market. 
    **Return only the score as a number, without any other text, explanation, or characters.**
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )

    return chat_completion.choices[0].message.content


def analyze_hot_topic(article):
    client = OpenAI(
        api_key = CHATGPT_KEY
    )

    prompt = f"""
    Analyze the following newspaper article and extract structured information with the goal of analysis on the global stock market. 
    Audience are the people who trade consistenly.
    {article}
    Please return a JSON object with the following fields:
    - title: A short title of the article.

    - description: A short summary of the article.
    
    - topic_1: topic 1
    - background_topic_1: background of topic 1
    - influence_topic_1: potential influence from topic 1

    - topic_2: topic 2
    - background_topic_2: background of topic 2
    - influence_topic_2: potential influence from topic 2

    - topic_3: topic 3
    - background_topic_3: background of topic 3
    - influence_topic_3: potential influence from topic 3
    
    - sector_1: First sector that might be affected
    - impact_1: Positive or Negative
    - stock_1: Company NAMES related to the first sector that might be affected. Text format
    
    - sector_2: Second sector that might be affected
    - impact_2: Positive or Negative
    - stock_2: Company NAMES related to the second sector that might be affected. Text format

    - sector_3: Third sector that might be affected
    - impact_3: Positive or Negative
    - stock_3: Company NAMES related to the third sector that might be affected. Text format
    
    **Ensure the response is valid JSON.**
    **There shouldnt be any null values**
    **Do not wrap the json codes in JSON markers.**
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )

    return chat_completion.choices[0].message.content






def filter_similar_articles(article_titles):
    client = OpenAI(
        api_key = CHATGPT_KEY
    )

    titles_str = "\n".join(article_titles)

    prompt = f"""
    Please analyze the following article titles and remove any duplicates with similar meanings. 
    The titles are:

    {titles_str}

    Return a list of the unique titles, each on a new line, without any explanation.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )
    result = chat_completion.choices[0].message.content
    return result.split("\n")

