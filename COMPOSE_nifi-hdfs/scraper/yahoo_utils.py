from bs4 import BeautifulSoup
import requests
import re
import datetime
from urllib.parse import urlparse

# Based on: https://github.com/nicknochnack/Stock-and-Crypto-News-ScrapingSummarizationSentiment/blob/main/scrapesummarizesentiment.py


def search_for_stock_news_links(ticker):
    search_url = 'https://www.google.com/search?q=yahoo+finance+{}&tbm=nws&tbs=qdr%3Ah'.format(ticker)
    r = requests.get(search_url, cookies={
        'User-Agent': 'Mozilla/5.0',
        'CONSENT': 'PENDING+871',
        'AEC': 'Ackid1QxmDzTaVJatsVt_NiwaV9DaWs4PBTNW6nMkVIQPCECG6ywry--hQ',
        'DV': 'k4mxdAcYH6gUQIF0XFQkBVg9aHLluxg',
        'nid': '511=NEhICdGn3ITkSJgkRXLQR00KE2_B8yIYhfTShVzJHHM5EgiAaOQq7QXs2TFnXaXgs_HMW6NtsGMmPpBpk1ykhcDbOS77WuBSaIZIV5RA-0857YCP1psN8TWrhTKFNbZhH1GcUCFhVGQYmZqmfWltbLIkP5V4kOGmvaUoQHONE8-R7fo-EVrg',
        'SOCS': 'CAISHAgCEhJnd3NfMjAyMzExMDYtMF9SQzEaAnBsIAEaBgiAiLuqBg'
    })
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return hrefs


def strip_unwanted_urls(urls):
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']
    val = []
    for url in urls:
        if 'https://' in url and not any(exc in url for exc in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))


def is_finance_yahoo(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname == 'finance.yahoo.com'


def scrape_and_process_yahoo(URLs):
    ARTICLES = []
    for url in URLs:
        if is_finance_yahoo(url):
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            results = soup.find_all('p')
            if len(results) == 0:
                continue
            text = [res.text for res in results]
            words = ' '.join(text).split(' ')
            ARTICLE = ' '.join(words)

            results = soup.find_all('time')
            if len(results) == 0:
                continue
            text = results[0]['datetime']
            date = datetime.datetime.timestamp(
                datetime.datetime.strptime(text, '%Y-%m-%dT%H:%M:%S.%fZ')
            )

            ARTICLES.append({
                'timestamp': date,
                'content': ARTICLE,
                'url': url
            })
    return ARTICLES