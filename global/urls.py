from django.urls import path
from django.utils.text import slugify
from . import views 

urlpatterns = [
    path('', views.global_home, name='global_home'),
    path('whats-going-on-around-the-world/', views.global_report, name='global_report'),
    path('hot-topic/<int:id>/' ,views.global_hot_topic,      name='global_hot_topic'),
    path('upcoming-stock-listings/', views.global_stock_listings, name='global_stock_listings'),
    path('stock-comparison/', views.global_stock_comparison, name='global_stock_comparison'),
    path('stock-analysis/', views.global_stock_analysis, name='global_stock_analysis'),
    path('stock-insider/', views.global_stock_insider, name='global_stock_insider'),
]
