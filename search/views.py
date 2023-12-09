from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_trending_news():
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.select('.ranking_headline a')

        trending_news = []
        for news in news_list:
            title = news.get_text(strip=True)
            link = news['href']
            trending_news.append({'title': title, 'link': link})

        return trending_news
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

@app.route('/')
def index():
    trending_news = get_trending_news()
    return render_template('news_DB/index.html', trending_news=trending_news)

if __name__ == 'main':
    app.run(debug=True)