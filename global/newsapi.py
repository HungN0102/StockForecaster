import requests
import openai
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from chatgpt import analyze_hot_topic,calculate_global_impact_score

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

def get_hot_global_news():
    try:
        # Get today's date
        today = datetime.today()

        # Get the date two days ago
        two_days_ago = today - timedelta(days=2)

        # Format the dates as "YYYY-MM-DD"
        today_str = today.strftime("%Y-%m-%d")
        two_days_ago_str = two_days_ago.strftime("%Y-%m-%d")

        params = {
            "q": "trump OR economy OR global markets OR stock market OR finance OR inflation OR recession OR central banks OR federal reserve OR trade war OR geopolitical risk OR global economy OR china OR us economy OR europe economy OR commodities OR interest rates OR oil prices OR cryptocurrency",
            "from": two_days_ago_str,
            "to": today_str,
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

def get_hot_topics():
    articles = get_hot_global_news()
    articles = calculate_global_influence_score(articles)
    articles = [item for item in articles if float(item["global_influence_score"]) > 40][:5]
    articles = sorted(articles, key=lambda article: article['global_influence_score'], reverse=True)
    return articles


articles = get_hot_global_news()
articles = calculate_global_influence_score(articles)
articles = [item for item in articles if float(item["global_influence_score"]) > 40]
articles = sorted(articles, key=lambda article: article['global_influence_score'], reverse=True)

for article in articles:
    print("------------------------------------------")
    print(article["title"])
    print(article["url"])
    print(article["publishedAt"])
    print(article["source"]["name"])
    print(article["global_influence_score"])

print("------------------------------------")
print(articles[1]["url"])
print("------------------------------------")
content = get_text_from_url(articles[0]["url"])
print("------------------------------------")
print(content)
print("------------------------------------")
result = analyze_hot_topic(content)
print(type(result))
print("------------------------------------")
print(result)
