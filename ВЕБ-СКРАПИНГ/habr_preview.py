import requests
from bs4 import BeautifulSoup
import time

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 5-секундная пауза перед запросом
time.sleep(5)

resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, 'html.parser')

articles = soup.find_all('article', class_='post_preview')

for article in articles:
    title_tag = article.find('h2')
    title = title_tag.text.strip()
    link = title_tag.find('a').get('href')
    date = article.find('time').get('datetime')[:10]

    preview_text = article.get_text().lower()
    if any(k.lower() in preview_text for k in KEYWORDS):
        print(f"{date} – {title} – {link}")