from datetime import timedelta, timezone, datetime
from article.models import *
from .chatgpt import *
from .finnhub import *
from .newsapi import *

def is_old_enough(model, hours_ago):
    if model:
        # Get the current time in UTC
        now = datetime.now(timezone.utc)

        # Check if the last entry is older than 4 hours
        if now - model.created_at > timedelta(hours=hours_ago):
            return True  # More than hours_ago hours old
        else:
            return False  # Still fresh
    else:
        return True  # No entries exist, so it's "old" by default
    
def format_value(num, currency):
    if num > 1000000:
        if not num % 1000000:
            return f'{currency}{num // 1000000}M'
        return f'{currency}{round(num / 1000000, 1)}M'
    return f'{currency}{num // 1000}K'
    
def get_hot_topics(from_date, to_date):
    articles = get_hot_article_news(from_date, to_date)
    articles = calculate_article_influence_score(articles)
    articles = [item for item in articles if float(item["article_influence_score"]) > 40][:4]
    articles = sorted(articles, key=lambda article: article['article_influence_score'], reverse=True)

    chatgpt_results = []
    for article in articles:
        content = get_text_from_url(article["url"])
        chatgpt_result = json.loads(analyze_hot_topic(content))
        chatgpt_results.append(chatgpt_result)


    """
    Filters out dictionaries with duplicate titles.
    
    :param data_dict: A list of dictionaries where each dictionary has a "title" key.
    :return: A list of dictionaries with unique titles.
    """
    seen_titles = set()
    unique_articles = []

    for entry in chatgpt_results:
        title = entry["title"]
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(entry)

    unique_titles = [item["title"] for item in unique_articles]
    filtered_titles = filter_similar_articles(unique_titles)
    filtered_articles = [article for article in unique_articles if article["title"] in filtered_titles]
    return filtered_articles


def insert_latest_hot_topics(last_hottopic, from_date, to_date):
    try:
        message =  "Init"
        group_id = 1 if last_hottopic is None else last_hottopic.group_id + 1

        if is_old_enough(last_hottopic, 4):
            message = "Calling articles = get_hot_topics(%s, %s)" % (from_date, to_date)
            articles = get_hot_topics(from_date, to_date)

            message = "Inserting articles to database"
            print("Number of articles: %s" % len(articles))
            for article in articles:
                print("Inserting Article: %s" % article["title"])
                HotTopic.objects.create(
                    group_id = group_id,
                    title = article["title"],
                    description = article["description"],
                    topic_1 = article["topic_1"],
                    background_topic_1 = article["background_topic_1"],
                    influence_topic_1 = article["influence_topic_1"],
                    topic_2 = article["topic_2"],
                    background_topic_2 = article["background_topic_2"],
                    influence_topic_2 = article["influence_topic_2"],
                    topic_3 = article["topic_3"],
                    background_topic_3 = article["background_topic_3"],
                    influence_topic_3 = article["influence_topic_3"],
                    sector_1 = article["sector_1"],
                    impact_1 = article["impact_1"],
                    stock_1 = article["stock_1"],
                    sector_2 = article["sector_2"],
                    impact_2 = article["impact_2"],
                    stock_2 = article["stock_2"],
                    sector_3 = article["sector_3"],
                    impact_3 = article["impact_3"],
                    stock_3 = article["stock_3"]
                )
            message = "Inserted hot topics to database"
        else:
            message = "Last hot topic isn't more than 4 hours ago, it was %s " % last_hottopic.created_at

    except Exception as e:
        message = str(e)

    return message

def insert_latest_stock_listings(stock_listing, from_date, to_date):
    try:
        message =  "Init"
        check_hours_ago = 24
        group_id = 1
        if stock_listing is not None:
            group_id = stock_listing.group_id + 1

        if is_old_enough(stock_listing, check_hours_ago):
            message = "Calling stock_listings = get_latest_ipo(%s, %s)" % (from_date, to_date)
            stock_listings = get_latest_ipo(from_date, to_date)

            message = "Inserting stock_listings to database"
            print("Number of stock listings: %s" % len(stock_listings))
            
            for stock_listing in stock_listings:
                print("Inserting Stock Listings: %s" % stock_listing["name"])
                StockListing.objects.create(
                    group_id = group_id,
                    date = stock_listing["date"],
                    company = stock_listing["name"],
                    code = stock_listing["symbol"],
                    business_description = "",
                    price_range = "$" + stock_listing["price"],
                    total_shares_value = format_value(int(stock_listing["totalSharesValue"]), "$"),
                    number_of_shares = format_value(int(stock_listing["numberOfShares"]), "")
                )

            message = "Inserted Stock Listings to database"
        else:
            message = "Last Stock Listing isn't more than %s hours ago, it was %s " % check_hours_ago, stock_listing.created_at

    except Exception as e:
        message = str(e)

    return message

insert_latest_stock_listings(None, "2025-02-15", "2025-03-15")