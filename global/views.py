from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def global_home(request):
    return render(request, 'global/home.html')

def global_report(request):
    return render(request, 'global/report.html')

def global_stock_listings(request):
    return render(request, 'global/stock_listings.html')

def global_hot_topic(request, hot_topic):
    formatted_topic = hot_topic.replace('-',' ').title()
    return render(request, 'global/hot_topic.html',{'hot_topic': formatted_topic})

def global_stock_comparison(request):
    return render(request, 'global/stock_comparison.html')

def global_stock_analysis(request):
    return render(request, 'global/stock_analysis.html')

def global_stock_insider(request):
    return render(request, 'global/stock_insider.html')