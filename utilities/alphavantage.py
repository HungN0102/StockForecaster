import finnhub
from decouple import config
from .utilities import *
import requests

ALPHAVANTAGE_KEY = config("ALPHAVANTAGE_KEY")

def get_latest_company_overview(code):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={code}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
    return data


def get_latest_company_dividend(code):
    url = f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={code}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
    return data["data"][0]

def get_latest_company_income_statement(code):
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={code}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
    if data["annualReports"][0]["fiscalDateEnding"] > data["quarterlyReports"][0]["fiscalDateEnding"]:
        return data["annualReports"][0]
    return data["quarterlyReports"][0]

def get_latest_company_balance_sheet(code):
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={code}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
    if data["annualReports"][0]["fiscalDateEnding"] > data["quarterlyReports"][0]["fiscalDateEnding"]:
        return data["annualReports"][0]
    return data["quarterlyReports"][0]

def get_latest_company_cash_flow(code):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={code}&apikey={ALPHAVANTAGE_KEY}'
    r = requests.get(url)
    data = r.json()
    if data["annualReports"][0]["fiscalDateEnding"] > data["quarterlyReports"][0]["fiscalDateEnding"]:
        return data["annualReports"][0]
    return data["quarterlyReports"][0]

def get_latest_company_information(company_code):
    try:
        company_overview = get_latest_company_overview(company_code)
        balance_sheet = get_latest_company_balance_sheet(company_code)
        income_statement = get_latest_company_income_statement(company_code)

        company_name = validate_equation(lambda: company_overview["Name"])
        company_code = validate_equation(lambda: company_overview["Symbol"])
        company_currency = validate_equation(lambda: income_statement["reportedCurrency"])
        company_description = validate_equation(lambda: company_overview["Description"])
        company_fiscal_date_ending = validate_equation(lambda: income_statement["fiscalDateEnding"])
        company_market_capitalization = validate_equation(lambda: float(company_overview["MarketCapitalization"]))
        company_total_revenue = validate_equation(lambda: float(income_statement["totalRevenue"]))
        company_gross_profit = validate_equation(lambda: float(income_statement["grossProfit"]))
        company_net_income = validate_equation(lambda: float(income_statement["netIncome"]))
        company_ebitda = validate_equation(lambda: float(income_statement["ebitda"]))
        company_operating_margin = validate_equation(lambda: round(100*float(company_overview['OperatingMarginTTM']),2))
        company_profit_margin = validate_equation(lambda: round(100*float(company_overview['ProfitMargin']),2))
        company_quarterly_revenue_growth =  validate_equation(lambda: round(100*float(company_overview['QuarterlyRevenueGrowthYOY']),2))
        company_quarterly_earnings_growth =  validate_equation(lambda: round(100*float(company_overview['QuarterlyEarningsGrowthYOY']),2))
        company_total_assets =  validate_equation(lambda: float(balance_sheet["totalAssets"]))
        company_total_liabilities =  validate_equation(lambda: float(balance_sheet["totalLiabilities"]))
        company_shareholder_equity =  validate_equation(lambda: float(balance_sheet["totalShareholderEquity"]))
        company_current_asset_to_liability_ratio = validate_equation(lambda: round(float(balance_sheet["totalCurrentAssets"]) / float(balance_sheet["totalCurrentLiabilities"]),2), None)
        company_debt_to_equity_ratio = validate_equation(lambda: round(float(balance_sheet["totalLiabilities"]) / float(balance_sheet["totalShareholderEquity"]),2))
        company_eps = validate_equation(lambda: float(company_overview["EPS"]))
        company_price_to_sales_ratio = validate_equation(lambda: float(company_overview["PriceToSalesRatioTTM"]))
        company_ev_to_ebitda = validate_equation(lambda: float(company_overview["EVToEBITDA"]))
        company_52_week_low = validate_equation(lambda: float(company_overview["52WeekLow"]))
        company_52_week_high = validate_equation(lambda: float(company_overview["52WeekHigh"]))
        company_50_day_moving_average = validate_equation(lambda: float(company_overview["50DayMovingAverage"]))
        company_200_day_moving_average = validate_equation(lambda: float(company_overview["200DayMovingAverage"]))
        company_analyst_target_price = validate_equation(lambda: float(company_overview["AnalystTargetPrice"]))
        company_peter_lynch_fair_value = None if float(company_overview['EPS']) < 0 else validate_equation(lambda: float(company_overview['EPS']) * (8.5 + 2 * 100*float(company_overview["QuarterlyEarningsGrowthYOY"])))
        company_price_to_earnings_fair_value = None if float(company_overview['EPS']) < 0 else validate_equation(lambda: round(float(company_overview['EPS']) * float(company_overview["TrailingPE"]),2))
        company_altman_z_score =   validate_equation(lambda: round(1.2 * (float(balance_sheet["totalCurrentAssets"]) - float(balance_sheet["totalCurrentLiabilities"])) / float(balance_sheet["totalAssets"]) + \
                     1.4 * (float(balance_sheet["retainedEarnings"]) / float(balance_sheet["totalAssets"])) +  \
                     3.3 * (float(income_statement["operatingIncome"]) / float(balance_sheet["totalAssets"])) + \
                     0.6 * (float(company_overview["MarketCapitalization"]) / float(balance_sheet["totalCurrentLiabilities"])) + \
                     1 * (float(income_statement["totalRevenue"]) / float(balance_sheet["totalAssets"])),2))

        company_information = {
            "name": company_name,
            "code": company_code,
            "currency": company_currency,
            "description": company_description,
            "fiscal_date_ending": company_fiscal_date_ending,
            "market_capitalization": company_market_capitalization,
            "total_revenue":  company_total_revenue,
            "gross_profit": company_gross_profit,
            "net_income":  company_net_income,
            "ebitda": company_ebitda,
            "operating_margin": company_operating_margin,
            "profit_margin": company_profit_margin,
            "quarterly_revenue_growth": company_quarterly_revenue_growth,
            "quarterly_earnings_growth": company_quarterly_earnings_growth,
            "total_assets": company_total_assets,
            "total_liabilities": company_total_liabilities,
            "shareholder_equity": company_shareholder_equity,
            "current_asset_to_liability_ratio": company_current_asset_to_liability_ratio,
            "debt_to_equity_ratio": company_debt_to_equity_ratio,
            "eps": company_eps,
            "price_to_sales_ratio": company_price_to_sales_ratio,
            "ev_to_ebitda": company_ev_to_ebitda,
            "52-week-low": company_52_week_low,
            "52-week-high": company_52_week_high,
            "50-day-moving-average": company_50_day_moving_average,
            "200-day-moving-average": company_200_day_moving_average,
            "analyst-target-price": company_analyst_target_price,
            "peter_lynch_fair_value": company_peter_lynch_fair_value,
            "price_to_earnings_fair_value": company_price_to_earnings_fair_value,
            "altman_z_score":   company_altman_z_score
        }

        return company_information
    
    except Exception as e:
        return trace(e)
    
get_latest_company_information("TSLA")
# info = get_latest_company_information("AAPL")

# company_overview = get_latest_company_overview("LUNR")
# income_statement = get_latest_company_income_statement("LUNR")
# balance_sheet = get_latest_company_balance_sheet("LUNR")
        
# company_overview["EVToEBITDA"]


# company_code = "LUNR"
# code = "LUNR"
# key = "PDND5UVZJ9VYSERY"
