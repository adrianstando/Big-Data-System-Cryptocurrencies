import datetime
import requests
from bs4 import BeautifulSoup


def format_date_to_timestamp(date):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').timestamp()


def scrape_paragraphs(url):
    try:
        r = requests.get(url)
    except Exception as e:
        return ''

    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('p')
    if len(results) == 0:
        return ''
    text = [res.text for res in results]
    words = ' '.join(text).split(' ')
    article = ' '.join(words)

    return article
