from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import HotTopic, StockListing, Company

# Create your views here.
def article_home(request):
    return render(request, 'article/home.html')

def article_report(request):
    # # Initialize Parameters for Checking and Inserting Hot Topics if Necessary 
    # today = datetime.today().strftime("%Y-%m-%d")
    # past_2days = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    # next_1month = (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d")

    # # Get last hot topic, stock listing
    # last_hottopic = HotTopic.objects.order_by('-created_at').first()
    # last_stocklisting = StockListing.objects.order_by('-created_at').first()
    
    # message = insert_latest_hot_topics(last_hottopic, past_2days, today)
    # message = insert_latest_stock_listings(last_stocklisting, today, next_1month)
    return render(request, 'article/report.html', {"message": "Nice"})

def article_stock_listings(request):
    last_stocklisting = StockListing.objects.order_by('-created_at').first()
    last_stocklistings = StockListing.objects.filter(group_id = last_stocklisting.group_id)    
    return render(request, 'article/stock_listings.html', {"stock_listings": last_stocklistings})

def article_hot_topic(request, id):
    hot_topic = HotTopic.objects.filter(id=id).first()    
    return render(request, 'article/hot_topic.html',{'hot_topic': hot_topic})

def article_stock_comparison(request):
    code1 = request.GET.get('company1', 'AAPL')
    code2 = request.GET.get('company2', 'ORCL')

    company1 = Company.objects.filter(code=code1).first()
    company2 = Company.objects.filter(code=code2).first()
    all_company_codes = Company.objects.order_by('code').values_list('code', flat=True)
    
    return render(request, 'article/stock_comparison.html', {"company1": company1, 
                                                             "company2": company2,
                                                             "company_codes":all_company_codes})

def article_stock_analysis(request):
    return render(request, 'article/stock_analysis.html')

def article_stock_insider(request):
    return render(request, 'article/stock_insider.html')