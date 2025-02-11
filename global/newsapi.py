import requests
import openai
from bs4 import BeautifulSoup
from decouple import config
from datetime import datetime, timedelta
import json
from chatgpt import analyze_hot_topic, calculate_global_impact_score

NEWSAPI_KEY = config("NEWSAPI_KEY")
def get_text_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        # Check if request was successful
        if response.status_code != 200:
            raise("Cant connect to URL: %s" % url)

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # Extract the page title
        title = soup.title.text
        print(f"🔹 Title: {title}\n")

        # Extract all paragraph texts
        content = soup.find_all(["p", "span", "li", "h1", "h2", "h3", "h4", "h5"])

        # Extract the text from each element, whether it's a <p>, <span>, <li>, etc.
        full_text = " ".join([element.get_text(strip=True) for element in content])

        return full_text

    except Exception as e:
        print(e)

def get_hot_global_news(from_date, to_date):
    try:
        params = {
            "q": "trump OR economy OR global markets OR stock market OR finance OR inflation OR recession OR central banks OR federal reserve OR trade war OR geopolitical risk OR global economy OR china OR us economy OR europe economy OR commodities OR interest rates OR oil prices OR cryptocurrency",
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "popuplarity",
            "pageSize": 20,
            'domains': 'bbc.com,forbes.com,businessinsider.com,apnews.com',
            "apiKey": NEWSAPI_KEY,
        }

        url = "https://newsapi.org/v2/everything"
        response = requests.get(url, params=params)

        if not response.status_code == 200:
            raise("Cant find anything")

        data = response.json()
        articles = data["articles"][:100]
        # articles = [item for item in articles if item["source"]["name"] in ["BBC News", "Forbes", "Associated Press"]]

        print("------------------------------------------")
        print("Number of articles is: %s" % len(articles))
        print("------------------------------------------")


        return articles
    except Exception as e:
        print(e)

def calculate_global_influence_score(articles):
    for i, article in enumerate(articles):
        global_influence_score = calculate_global_impact_score(article["title"], article["description"])
        articles[i]["global_influence_score"] = float(global_influence_score)
        print("CHATGPT FINISHED ARTICLE NUMBER %s" % i)
    return articles

def get_hot_topics(from_date, to_date):
    articles = get_hot_global_news(from_date, to_date)
    articles = calculate_global_influence_score(articles)
    articles = [item for item in articles if float(item["global_influence_score"]) > 40][:4]
    articles = sorted(articles, key=lambda article: article['global_influence_score'], reverse=True)

    chatgpt_results = []
    for article in articles:
        content = get_text_from_url(article["url"])
        chatgpt_result = json.loads(analyze_hot_topic(content))
        chatgpt_results.append(chatgpt_result)
    return chatgpt_results


# articles = get_hot_global_news()
# articles = calculate_global_influence_score(articles)
# articles = [item for item in articles if float(item["global_influence_score"]) > 40]
# articles = sorted(articles, key=lambda article: article['global_influence_score'], reverse=True)

# for article in articles:
#     print("------------------------------------------")
#     print(article["title"])
#     print(article["url"])
#     print(article["publishedAt"])
#     print(article["source"]["name"])
#     print(article["global_influence_score"])

# print("------------------------------------")
# print(articles[1]["url"])
# print("------------------------------------")
# content = get_text_from_url(articles[0]["url"])
# print("------------------------------------")
# print(content)
# print("------------------------------------")
# result = analyze_hot_topic(content)
# print(type(result))
# print("------------------------------------")
# print(result)
