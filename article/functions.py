import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forecaster.settings")
django.setup()

from django.core.files import File

from datetime import timedelta, timezone, datetime
from article.models import HotTopic, StockListing, Company, InsiderTransaction
from utilities.chatgpt import *
from utilities.finnhub import *
from utilities.newsapi import *
from utilities.alphavantage import *
from utilities.utilities import *

def insert_latest_hot_topics(last_hottopic, from_date, to_date):
    try:
        message =  "Init"
        group_id = 1 if last_hottopic is None else last_hottopic.group_id + 1

        if validate_model_insert(last_hottopic, 4):
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

        if validate_model_insert(stock_listing, check_hours_ago):
            print("Calling stock_listings = get_latest_ipo(%s, %s)" % (from_date, to_date))
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
            message = "Last Stock Listing isn't more than %s hours ago, it was %s " % (check_hours_ago, stock_listing.created_at)

    except Exception as e:
        message = str(e)

    return message


def insert_latest_insider_transactions(symbol, from_date, to_date):
    message =  trace(f"Initialize insert_latest_insider_transactions({symbol}, {from_date}, {to_date})")
    check_hours_ago = 24*7
    try:
        trace(f"Get company with cod={symbol}")
        company_db = Company.objects.filter(code=symbol).first()

        trace(f"Get old insider transaction with cod={symbol}")
        last_insider_transaction_db = InsiderTransaction.objects.filter(company=company_db).first()

        if not validate_model_insert(last_insider_transaction_db, check_hours_ago):
            raise Exception(f"Insider transaction {symbol} did not meet validation to insert")
        
        trace(f"Delete old insider transaction with cod={symbol}")
        InsiderTransaction.objects.filter(cod=symbol).delete()

        trace(f"Calling insider_transactions = get_latest_insider_transactions({symbol}, {from_date}, {to_date})")
        insider_transactions = get_latest_insider_transactions(symbol, from_date, to_date)

        print(f"Number of insider_transactions: {len(insider_transactions)}")
        for insider_transaction in insider_transactions:
            currency = insider_transaction["currency"] if len(insider_transaction["currency"]) > 0 else "$"

            print(f"Inserting Insider Transactions: {insider_transaction["symbol"]}")
            InsiderTransaction.objects.create(
                company = Company.objects.get(cod=insider_transaction["symbol"]),
                date = insider_transaction["filingDate"],
                insider = insider_transaction["name"],
                transaction_type = translate_insider_transaction(insider_transaction["transactionCode"], 
                                                                    insider_transaction["transactionPrice"],
                                                                    insider_transaction["isDerivative"]),

                number_of_shares = insider_transaction["change"],
                transaction_price = insider_transaction["transactionPrice"],
                transaction_value = insider_transaction["change"] * insider_transaction["transactionPrice"],
                
                transaction_price_text = format_value(insider_transaction["transactionPrice"], currency),
                transaction_value_text = format_value(insider_transaction["change"] * insider_transaction["transactionPrice"], currency)
            )

    except Exception as e:
        print(f"Exception with insider transaction with cod={symbol}: {e}")

    return message

def insert_latest_company_information(symbol):
    message =  trace(f"Init insert_latest_company_information({symbol})")
    try:
        message = trace(f"Delete company with cod={symbol}")
        Company.objects.filter(code=symbol).delete()

        message = trace(f"Calling company_information = get_latest_company_information({symbol})")
        company_information = get_latest_company_information(symbol)

        message = trace(f"Successfully extracted latest company information from API: {company_information["name"]}. Now adding company with latest information to database")
        Company.objects.create(
            name = company_information["name"],
            code = company_information["code"],
            currency = company_information["currency"],
            description = company_information["description"],
            fiscal_date_ending = company_information["fiscal_date_ending"],
            market_capitalization = company_information["market_capitalization"],
            total_revenue = company_information["total_revenue"],
            gross_profit = company_information["gross_profit"],
            net_income = company_information["net_income"],
            ebitda = company_information["ebitda"],
            operating_margin = company_information["operating_margin"],
            profit_margin = company_information["profit_margin"],
            quarterly_revenue_growth = company_information["quarterly_revenue_growth"],
            quarterly_earnings_growth = company_information["quarterly_earnings_growth"],
            total_assets = company_information["total_assets"],
            total_liabilities = company_information["total_liabilities"],
            shareholder_equity = company_information["shareholder_equity"],
            current_asset_to_liability_ratio = company_information["current_asset_to_liability_ratio"],
            debt_to_equity_ratio = company_information["debt_to_equity_ratio"],
            eps = company_information["eps"],
            price_to_sales_ratio = company_information["price_to_sales_ratio"],
            ev_to_ebitda = company_information["ev_to_ebitda"],
            week_52_high = company_information["52-week-high"],
            week_52_low = company_information["52-week-low"],
            day_50_moving_average = company_information["50-day-moving-average"],
            day_200_moving_average = company_information["200-day-moving-average"],
            analyst_target_price = company_information["analyst-target-price"],
            peter_lynch_fair_value = company_information["peter_lynch_fair_value"],
            price_to_earnings_fair_value = company_information["price_to_earnings_fair_value"],
            altman_z_score = company_information["altman_z_score"]
        )
        message = trace(f"Successfully inserting {company_information["name"]} to company model in database")

    except Exception as e:
        message = trace(f"Exception with insert_latest_company with cod={symbol}: {e}")

    return message


# insert_latest_company_information("AAPL")
# insert_latest_company_information("LUNR")
# insert_latest_company_information("ORCL")
# insert_latest_company_information("NVDA")
# insert_latest_company_information("GOOGL")
# insert_latest_company_information("JPM")
# insert_latest_company_information("RARE")

# insert_latest_company_information("NEE")
# insert_latest_company_information("YETI")
# insert_latest_company_information("MSFT")
# insert_latest_company_information("AMZN")
# insert_latest_company_information("AMD")
# insert_latest_company_information("BAC")
# insert_latest_company_information("BP")

# insert_latest_company_information("CVS")
# insert_latest_company_information("CEG")
# insert_latest_company_information("GE")
# insert_latest_company_information("VST")
# insert_latest_company_information("FFIV")
# insert_latest_company_information("SBUX")
# insert_latest_company_information("MMM")

# insert_latest_company_information("DVA")
# insert_latest_company_information("META")
# insert_latest_company_information("TPL")
# insert_latest_company_information("PLTR")
# insert_latest_company_information("TSLA")