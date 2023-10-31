import requests
from newsapi import NewsApiClient
import pprint
import yfinance as yf
from datetime import datetime, timedelta


def get_stock_data(symbol):
    now = datetime.now()

    # Create a ticker object
    ticker = yf.Ticker(symbol)

    # Get data for specific dates
    data_today = round(ticker.history(period="1d")['Close'].tail(1).iloc[0],2)
    data_last_week = round( ticker.history(start=(now - timedelta(days=7)).strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"))['Close'].head(
        1).iloc[0],2)

    data_last_month = round(ticker.history(start=(now - timedelta(days=30)).strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"))['Close'].head(
        1).iloc[0],2)

    data_last_year = round(ticker.history(start=(now - timedelta(days=365)).strftime("%Y-%m-%d"), end=now.strftime("%Y-%m-%d"))['Close'].head(
        1).iloc[0], 2)

    data_beginning = round(ticker.history(period="max")['Close'].iloc[0],3)


    # Display the data
    print(f"Closing price today: ${data_today:.2f}")
    print(f"Closing price last week: ${data_last_week:.2f}")
    print(f"Closing price last month: ${data_last_month:.2f}")
    print(f"Closing price last year: ${data_last_year:.2f}")
    print(f"Closing price max: ${data_beginning:.2f}")

    week_percent = get_percent(data_last_week,data_today)
    month_percent = get_percent(data_last_month,data_today)
    year_percent = get_percent(data_last_year,data_today)
    max_percent = get_percent(data_beginning,data_today)


    return {
        'symbol': symbol,
        'today_price': data_today,
        'week_price': data_last_week,
        'month_price': data_last_month,
        'week_percent': week_percent,
        'month_percent': month_percent,
        'year_price': data_last_year,
        'year_percent': year_percent,
        'beginning_price': data_beginning,
        'beginning_percent': max_percent
            }

def get_percent(old_price,price_today):
    old_price = float(str(old_price).replace("$",""))
    price_today = float(str(price_today).replace("$",""))


    return round(((price_today - old_price)/old_price)*100,2)
def get_stock_news(symbol,api_key):
    # Fetch news via external API or use dummy data
    import requests
    url = ('https://newsapi.org/v2/everything?'
           f'q={symbol}&'
           'from=2023-10-05&'
           'to=2023-11-04&'
           'language=en&'
           'sort_by=relevancy&'
           'page=1&'
           f'apiKey={api_key}')

    response = requests.get(url)
    data = response.json()

    # Check if articles are present
    article_list = []
    if data['totalResults'] > 0:
        article_list = data['articles']

        #for article in article_list:
            #pprint.pprint(article)

    else:
        print("No articles found.")

    return [{'news': article_list}]
    #Keys: author, publishedAt, source, title, url


def fetch_historical_data(symbol, start_date="2023-01-01", end_date="2023-12-31"):
    # Fetch historical data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)
    # Transform the data into a list of [date, close_price] pairs
    return data['Close'].reset_index().values.tolist()