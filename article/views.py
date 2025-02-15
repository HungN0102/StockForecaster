from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import HotTopic
from utilities.functions import insert_latest_hot_topics

# Create your views here.
def article_home(request):
    return render(request, 'article/home.html')

def article_report(request):
    # Initialize Parameters for Checking and Inserting Hot Topics if Necessary 
    to_date = datetime.today().strftime("%Y-%m-%d")
    from_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    last_hottopic = HotTopic.objects.order_by('-created_at').first()

    message = insert_latest_hot_topics(last_hottopic, from_date, to_date)
    return render(request, 'article/report.html', {"message": message})

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