from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from .newsapi import get_hot_topics
from .models import HotTopic
from .ults import is_last_hottopic_old

# Create your views here.
def article_home(request):
    return render(request, 'article/home.html')

def article_report(request):
    try:
        dict_ = {"message": "Init"}
        # Get today's date
        to_date = datetime.today().strftime("%Y-%m-%d")
        from_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        last_hottopic = HotTopic.objects.order_by('-created_at').first()
        group_id = 1 if last_hottopic is None else last_hottopic.group_id + 1

        if is_last_hottopic_old(last_hottopic):
            dict_["message"] = "Calling articles = get_hot_topics(%s, %s)" % (from_date, to_date)
            articles = get_hot_topics(from_date, to_date)

            dict_["message"] = "Inserting articles to database"
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
            dict_["message"] = "Inserted hot topics to database"
        else:
            dict_["message"] = "Last hot topic isn't more than 4 hours ago, it was %s " % last_hottopic.created_at

    except Exception as e:
        dict_["message"] = str(e)

    return render(request, 'article/report.html', dict_)

def article_stock_listings(request):
    return render(request, 'article/stock_listings.html')

def article_hot_topic(request, id):
    hot_topic = HotTopic.objects.filter(id=id).first()    
    return render(request, 'article/hot_topic.html',{'hot_topic': hot_topic})

def article_stock_comparison(request):
    return render(request, 'article/stock_comparison.html')

def article_stock_analysis(request):
    return render(request, 'article/stock_analysis.html')

def article_stock_insider(request):
    return render(request, 'article/stock_insider.html')