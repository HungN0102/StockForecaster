from django.db import models
from django.urls import reverse
from datetime import datetime


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    cod = models.CharField(max_length=255)
    market = models.CharField(max_length=255)
    sales = models.CharField(max_length=255)
    net_income = models.CharField(max_length=255)
    discounted_cash_flow_fair_value = models.CharField(max_length=255)
    peter_lynch_fair_value = models.CharField(max_length=255)
    economic_value_added_fair_value = models.CharField(max_length=255)
    average_fair_value = models.CharField(max_length=255)
    return_on_equity = models.CharField(max_length=255)
    profit_margin = models.CharField(max_length=255)
    debt_to_equity_ratio = models.CharField(max_length=255)
    earnings_per_share = models.CharField(max_length=255)
    annual_dividend = models.CharField(max_length=255)
    shareholders_yield = models.CharField(max_length=255)
    altman_z_score = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name

class Report(models.Model):
    country_1 = models.CharField(max_length=255)
    news_country_1 = models.TextField(blank=True,null=True)
    stock_exchange_country_1 = models.CharField(max_length=255)
    impact_country_1 = models.TextField(blank=True,null=True)
    affected_stock_1_country_1 = models.CharField(max_length=255)
    affected_stock_desc_1_country_1 = models.TextField(blank=True,null=True)
    affected_stock_2_country_1 = models.CharField(max_length=255)
    affected_stock_desc_2_country_1 = models.TextField(blank=True,null=True)
    affected_stock_3_country_1 = models.CharField(max_length=255)
    affected_stock_desc_3_country_1 = models.TextField(blank=True,null=True)

    country_2 = models.CharField(max_length=255)
    news_country_2 = models.TextField(blank=True,null=True)
    stock_exchange_country_2 = models.CharField(max_length=255)
    impact_country_2 = models.TextField(blank=True,null=True)
    affected_stock_1_country_2 = models.CharField(max_length=255)
    affected_stock_desc_1_country_2 = models.TextField(blank=True,null=True)
    affected_stock_2_country_2 = models.CharField(max_length=255)
    affected_stock_desc_2_country_2 = models.TextField(blank=True,null=True)
    affected_stock_3_country_2 = models.CharField(max_length=255)
    affected_stock_desc_3_country_2 = models.TextField(blank=True,null=True)

    country_3 = models.CharField(max_length=255)
    news_country_3 = models.TextField(blank=True,null=True)
    stock_exchange_country_3 = models.CharField(max_length=255)
    impact_country_3 = models.TextField(blank=True,null=True)
    affected_stock_1_country_3 = models.CharField(max_length=255)
    affected_stock_desc_1_country_3 = models.TextField(blank=True,null=True)
    affected_stock_2_country_3 = models.CharField(max_length=255)
    affected_stock_desc_2_country_3 = models.TextField(blank=True,null=True)
    affected_stock_3_country_3 = models.CharField(max_length=255)
    affected_stock_desc_3_country_3 = models.TextField(blank=True,null=True)

    major_company_1 = models.CharField(max_length=255)
    news_major_company_1 = models.TextField(blank=True,null=True)
    impact_major_company_1 = models.TextField(blank=True,null=True)
    
    major_company_2 = models.CharField(max_length=255)
    news_major_company_2 = models.TextField(blank=True,null=True)
    impact_major_company_2 = models.TextField(blank=True,null=True)

    major_company_3 = models.CharField(max_length=255)
    news_major_company_3 = models.TextField(blank=True,null=True)
    impact_major_company_3 = models.TextField(blank=True,null=True)

    minor_company_1 = models.CharField(max_length=255)
    news_minor_company_1 = models.TextField(blank=True,null=True)
    impact_minor_company_1 = models.TextField(blank=True,null=True)
    
    minor_company_2 = models.CharField(max_length=255)
    news_minor_company_2 = models.TextField(blank=True,null=True)
    impact_minor_company_2 = models.TextField(blank=True,null=True)

    minor_company_3 = models.CharField(max_length=255)
    news_minor_company_3 = models.TextField(blank=True,null=True)
    impact_minor_company_3 = models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'Report'
    
    def __str__(self):
        return 'ArticleReport_' + self.created_at
    
    # def get_absolute_url(self):
    #     return reverse("property_info", kwargs={"pk": self.pk})



class HotTopic(models.Model):
    group_id = models.IntegerField(editable=False)
    title = models.TextField(blank=True,null=True) # Title of the newspaper  

    description = models.TextField(blank=True,null=True) # Description of the newspaper  

    topic_1 = models.TextField(blank=True,null=True) # First topic in the news 
    background_topic_1 = models.TextField(blank=True,null=True) # More detail description about the First topic
    influence_topic_1 = models.TextField(blank=True,null=True) # Potential influence First topic can cause

    topic_2 = models.TextField(blank=True,null=True) # Second topic in the news 
    background_topic_2 = models.TextField(blank=True,null=True) # More detail description about the Second topic 
    influence_topic_2 = models.TextField(blank=True,null=True) # Potential influence Second topic can cause

    topic_3 = models.TextField(blank=True,null=True) # Third topic in the news 
    background_topic_3 = models.TextField(blank=True,null=True) # More detail description about the Third topic
    influence_topic_3 = models.TextField(blank=True,null=True) # Potential influence Third topic can cause

    sector_1 = models.CharField(max_length=255) # First sector that can be influenced by the analysis of this news
    impact_1 = models.CharField(max_length=255) # Positive or Negative
    stock_1 = models.TextField(blank=True,null=True) # Stock related to the first sector that can be influenced

    sector_2 = models.CharField(max_length=255) # Second sector that can be influenced by the analysis of this news
    impact_2 = models.CharField(max_length=255) # Positive or Negative
    stock_2 = models.TextField(blank=True,null=True) # Stock related to the Second sector that can be influenced

    sector_3 = models.CharField(max_length=255) # Third sector that can be influenced by the analysis of this news
    impact_3 = models.CharField(max_length=255) # Positive or Negative
    stock_3 = models.TextField(blank=True,null=True) # Stock related to the Third sector that can be influenced

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'HotTopics'
    
    def __str__(self):
        return 'HotTopic_' + str(self.created_at)
    
    # def get_absolute_url(self):
    #     return reverse("property_info", kwargs={"pk": self.pk})
    
class StockListing(models.Model):
    group_id = models.IntegerField(editable=False)

    date = models.CharField()
    company = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    business_description = models.TextField(blank=True,null=True)
    price_range = models.CharField(max_length=255)
    total_shares_value = models.CharField(max_length=255)
    number_of_shares = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'StockListings'
    
    def __str__(self):
        return self.company

class InsiderTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    insider = models.CharField(max_length=255)
    transaction = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'InsiderTransaction'
    
    def __str__(self):
        return 'InsiderTransaction_' + self.company.name
    
    # def get_absolute_url(self):
    #     return reverse("property_info", kwargs={"pk": self.pk})