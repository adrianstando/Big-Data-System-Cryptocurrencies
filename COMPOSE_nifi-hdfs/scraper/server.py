import os
from fastapi import FastAPI
from yahoo_utils import *
from cryptopanic_utils import *
from utils import *
import requests
import json

app = FastAPI()

CURRENCIES = ['USDT', 'CRO', 'XPRT', 'EOS', 'LTC', 'DOGE', 'DASH', 'BCH', 'DVPN', 'BNB', 'WAVES',
              'ETH', 'BTC', 'ZEC', 'RUNE', 'DAI', 'QTUM']


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/scrap/yahoo")
async def scrap_yahoo():
    """
    Scrap Yahoo Finance for news about the monitored tickers; returns data from the last hour
    """
    monitored_tickers = CURRENCIES + ['crypto', 'cryptocurrency', 'cryptocurrencies', 'blockchain', 'bitcoin']
    raw_urls = {ticker: search_for_stock_news_links(ticker) for ticker in monitored_tickers}
    cleaned_urls = {ticker: strip_unwanted_urls(raw_urls[ticker]) for ticker in monitored_tickers}
    articles = {ticker: scrape_and_process_yahoo(cleaned_urls[ticker]) for ticker in monitored_tickers}

    out = []
    for key, lst in articles.items():
        for elem in lst:
            elem['currency'] = key
            out.append(elem)

    return {"articles": out}


@app.get("/scrap/cryptopanic")
async def scrap_cryptopanic(min_date: int):
    """
    Scrap CryptoPanic for news
    :param min_date: timestamp of the first news to return
    """
    api_key = os.getenv("API_KEY_CRYPTOPANIC")
    return {"articles": get_news(min_date, api_key)}


@app.get("/scrap/cryptocompare")
async def scrap_cryptocompare(min_date: int):
    """
    Scrap CryptoCompare for news
    :param min_date: timestamp of the first news to return
    """
    api_key = os.getenv("API_KEY_CRYPTOCOMPARE")
    url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}"
    content = requests.get(url).text
    content = json.loads(content)['Data']

    content_filtered = [
        d
        for d in content
        if d.get('published_on') > min_date
    ]

    for elem in content_filtered:
        elem['content'] = scrape_paragraphs(elem['url'])
        elem['timestamp'] = elem.pop('published_on')

    return {"articles": content_filtered}


@app.get("/scrap/alphavantage")
async def scrap_alphavantage(min_date: int, max_date: int):
    """
    Scrap AlphaVantage for news
    :param min_date: timestamp of the first news to return
    :param max_date: timestamp of the last news to return
    """
    api_key = os.getenv("API_KEY_ALPHAVANTAGE")

    date_obj = datetime.datetime.utcfromtimestamp(min_date)
    formatted_date_min = date_obj.strftime("%Y%m%dT%H%M")
    date_obj = datetime.datetime.utcfromtimestamp(max_date)
    formatted_date_max = date_obj.strftime("%Y%m%dT%H%M")

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&" \
          f"time_from={formatted_date_min}&time_to={formatted_date_max}&limit=100&apikey={api_key}" \
          f"&topics=blockchain"

    content = requests.get(url).text
    content = json.loads(content)['feed']

    for elem in content:
        elem['content'] = scrape_paragraphs(elem['url'])

        d = elem.pop('time_published')
        d = datetime.datetime.strptime(d, '%Y%m%dT%H%M%S').timestamp()
        elem['timestamp'] = d

    return {"articles": content}


@app.get("/scrap/newsapi")
async def scrap_newsapi(min_date: int):
    """
    Scrap NewsAPI for news
    !!! it can only scrap data after 24h delay !!!
    :param min_date: timestamp of the first news to return
    """
    api_key = os.getenv("API_KEY_NEWSAPI")

    date_obj = datetime.datetime.utcfromtimestamp(min_date)
    formatted_date_min = date_obj.strftime("%Y-%m-%dT%H:%M:%S")
    url = f"https://newsapi.org/v2/everything?q=bitcoin OR crypto OR ethereum&apiKey={api_key}&from={formatted_date_min}"

    content = requests.get(url).text
    content = json.loads(content)['articles']

    for elem in content:
        elem['content_partial'] = elem.pop('content')
        elem['content'] = scrape_paragraphs(elem['url'])

        d = elem.pop('publishedAt')
        d = datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ').timestamp()
        elem['timestamp'] = d

    return {"articles": content}

