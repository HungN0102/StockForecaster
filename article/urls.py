from django.urls import path
from django.utils.text import slugify
from . import views 

urlpatterns = [
    path('', views.article_home, name='article_home'),
    path('whats-going-on-around-the-world/', views.article_report, name='article_report'),
    path('hot-topic/<int:id>/' ,views.article_hot_topic,      name='article_hot_topic'),
    path('upcoming-stock-listings/', views.article_stock_listings, name='article_stock_listings'),
    path('stock-comparison/', views.article_stock_comparison, name='article_stock_comparison'),
    path('stock-analysis/', views.article_stock_analysis, name='article_stock_analysis'),
    path('stock-insider/', views.article_stock_insider, name='article_stock_insider'),
]
