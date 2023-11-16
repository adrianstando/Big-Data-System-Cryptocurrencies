import bs4
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urlencode
from webdriver_manager.chrome import ChromeDriverManager
from utils import scrape_paragraphs


def get_news(min_date, api_key):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {"profile.default_content_settings": {"images": 2}}
    options.experimental_options["prefs"] = chrome_prefs

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    params = {
        'auth_token': api_key,
        'public': 'true'
    }
    url = 'https://cryptopanic.com/api/posts/?' + urlencode(params)

    response = requests.get(url, headers=headers)
    web_json = response.json()
    res = []

    for i in range(len(web_json.get('results'))):
        date = web_json.get('results')[i].get('created_at')
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').timestamp()

        if date > min_date:
            res_one = web_json.get('results')[i]
            out = parse_one_news(res_one, browser)
            if out is not None:
                out['publish_timestamp'] = date
                res.append(out)
        else:
            continue

    browser.close()

    return res


def parse_one_news(webjson, browser):
    cryptos = []
    if webjson.get('currencies') is not None:
        for i in webjson.get('currencies'):
            cryptos.append(i.get('code'))
    else:
        pass

    crypto = ''
    for i in cryptos:
        crypto = crypto + i + ' '

    browser.get(webjson.get('url'))

    wait = WebDriverWait(browser, 300)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'description-body')))

    html = browser.page_source
    doc = bs4.BeautifulSoup(html, 'lxml')
    real_url = doc.find('h1', {'class': 'post-title'})

    real_url = bs4.BeautifulSoup(str(real_url), 'lxml')
    publish_time = real_url.find('time')['datetime']
    real_url = real_url.findAll('a')[1]['href']

    content = doc.find('div', {'class': 'description-body'})
    content = bs4.BeautifulSoup(str(content), 'lxml')
    if content is None: return None
    content = content.find('p')
    if content is None: return None
    content = content.get_text()
    content_scrapped = scrape_paragraphs(real_url)

    news = {
        'title': webjson.get('title'),
        'timestamp': publish_time,
        'id': webjson.get('id'),
        'url': real_url,
        'crypto': crypto,
        'content_partial': content,
        'content': content_scrapped
    }
    return news
