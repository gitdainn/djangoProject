# Create your views here.

#from django.http import HttpResponse
#from urllib.parse import quote # 키워드 url과 합치기 위해 매개변수 타입 변환용
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from . import models

import requests
import xml.etree.ElementTree as ET

from selenium import webdriver
import time

from django.views import View
import random
from django.utils.html import escapejs
from .models import NewsArticle

import feedparser
from django.views.decorators.csrf import csrf_exempt #javascript로 넘겨받은 값 출력용
# 진회
def db_home(request):
    if request.method == 'POST':
        selected_news = request.POST.get('selected_news', '')
        # 뉴스 유튜브 링크 오픈
        if selected_news == 'naver':
            naver_news_link = 'https://news.naver.com/'
            return redirect(naver_news_link)

        elif selected_news == 'bbc':
            bbc_news_link = 'https://www.bbc.com/news'
            return redirect(bbc_news_link)

    # XML 데이터 가져오기
    xml_url = 'https://www.yonhapnewstv.co.kr/category/news/headline/feed/'
    response = requests.get(xml_url)

    # 확인용: XML 데이터를 콘솔에 출력
    print(response.content)

    # XML 파싱
    root = ET.fromstring(response.content)

    # 필요한 정보 추출
    items = root.findall('.//item')[:3]

    # 네임스페이스 정의
    ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}

    # 각 아이템에서 title, link, description, enclosure, content 추출
    data_list = []
    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text

        # enclosure URL 추출
        enclosure = item.find('.//enclosure')
        enclosure_url = enclosure.attrib.get('url') if enclosure is not None else None

        # content 추출
        content_encoded = item.find('.//content:encoded', namespaces=ns).text if item.find('.//content:encoded', namespaces=ns) is not None else None

        data_list.append({'title': title, 'link': link, 'description': description, 'enclosure_url': enclosure_url, 'content_encoded': content_encoded})

    # 확인용: 추출된 정보 출력
    for data in data_list:
        print(data)

    # 추출된 정보를 템플릿으로 전달
    context = {'data_list': data_list}
    return render(request, 'db.html', context)

class RandomFactNewsView(View):
    template_name = 'db.html'

    def get(self, request, *args, **kwargs):
        # 데이터베이스에서 모든 데이터 가져오기
        all_data = models.FactNews.objects.all()

        # 랜덤하게 하나의 데이터 선택
        random_fact_news = random.choice(all_data)

        # 선택된 데이터를 템플릿에 전달
        context = {
            'random_fact_news': random_fact_news,
        }

        return render(request, self.template_name, context)

#로그인
def main(request):
    datas = models.FactDB.load_fact()
    site = f"https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR&hl=ko"
    trend_datas = trend_search(request, site)
    mainnews_datas = mainnews()
    trot_datas = get_trot()
    context = {'random_fact_news': datas, 'trend_datas': trend_datas, 'mainnews_datas': mainnews_datas, 'trot_datas': trot_datas}
    return render(request, 'db_news.html', context)

def rss_feed(request):
    return render(request, '로그인화면.html')

def date_search(request):
    date_data = {}
    if request.method == 'POST':
        date = request.POST.get('date')
        search_type = request.POST.get('search_type')
        if search_type == 'date':
            date_data = search_total_date(date)
    # date_search.html에 대한 뷰 로직 작성
    return render(request, 'date_search.html', {'date_data': date_data})

def keyword_search(request):
    # keyword_search.html에 대한 뷰 로직 작성
    keyword_data = {}
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        search_type = request.POST.get('search_type')

        if search_type == 'keyword':
            keyword_data = search_total_keyword(keyword)

    return render(request, 'keyword_search.html', {'keyword_data': keyword_data})
def weather_search(request):
    site = f"https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"
    # keyword_search.html에 대한 뷰 로직 작성

    weather_data = []
    city = '서울'
    if request.method == 'POST':
        city = request.POST.get('city')

        # 기상청 날씨 가져오기
    weather_data = get_weather_data(site, city)
    return render(request, 'weatherHtml.html', {'weather_data': weather_data})

# 기상청 날씨 가져오기 #
def get_weather_data(site, searchcity):
    #encoded_city = quote(city)
    #rss_url = f'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108&city={encoded_city}'
    response = requests.get(site)

    # site로부터 제대로 추출됐을 경우 == 200
    #if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'xml')

    items = soup.find_all('item')
    # title과 link 정보를 저장할 리스트 초기화
    weather_data = []
    previous_date = {}

    # .find(태그명) 해당 태그의 첫 번째 태그 값을 반환함
    for item in items:
    # 찾은 모든 city 태그에 대해 반복
        locations = soup.find_all('location')
        for location in locations:
            city_tag = location.find('city')
            # 찾은 city 태그 값이 입력받은 도시명과 동일하다면
            if searchcity == city_tag.text:
                city_result = city_tag.text if city_tag else 'No city'
                # 해당 city의 data 태그 모두 가져옴
                data_list = location.find_all('data')
                for data in data_list:
                    tmEf = data.find('tmEf').text
                    wf = escapejs(data.find('wf').text)
                    tmn = data.find('tmn').text
                    tmx = data.find('tmx').text

                    date = tmEf.split(' ')[0].split()[0].strip()
                    if(previous_date != date):
                        weather_data.append({'city': city_result, 'date': date, 'weather': wf, 'tmn': tmn, 'tmx': tmx})
                        previous_date = date
                    # tmEF에서 날짜만 따와서 날짜가 이전에 받아온 데이터의 날짜와 다른 경우에만 값 추가하기

                #weather_data.append({'city': city_result, 'datetime': tmEf, 'weather': "0", 'tmn': "0"})

        else:
            print("해당 도시가 없습니다.")

    return weather_data

def trend_data(request):
    site = f"https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR&hl=ko"
    trend_datas = trend_search(request, site)
    return render(request, 'test.html', {'trend_data': trend_datas})

def trend_search(request, site):
    # site = f"https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR&hl=ko"
    # 웹 드라이버 시작
    driver = webdriver.Chrome()
    driver.get(site)

    time.sleep(1)

    # 현재 페이지의 소스를 가져오기
    page_source = driver.page_source

    # Selenium 웹 드라이버 종료
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    # 대소문자 구분 없이 'div' 태그 찾기
    trend_div = soup.find('div', {'class': 'feed-list-wrapper'})

    # 각 기사 불러오기
    articles = trend_div.find_all('div', {'class': 'details'})
    trend_datas = []
    previous_title = {}

    for article in articles[:7]:
        # 제목 가져오기 # javascripts로 문자열 넘길 땐 escapejs 해주기
        title = escapejs(article.find('span').text.strip())
        # 조회수 가져오기
        views = article.find('div', {'class': 'subtitles-overlap hidden'}).text # details-bottom

        first_char = None
        second_char = None
        first_int = {}

        for i, char in enumerate(views):
            if not char.isspace() and char != '\n':
                if first_char is None:
                    # 첫 번째 문자 추출
                    first_char = char
                elif second_char is None and i != 1:
                    # 두 번째 문자 추출 (두 번째 문자는 첫 번째 문자 이외에서 추출)
                    second_char = char

        if second_char == '만':
            first_int = int(first_char) * 10000
            trend_datas.append({'title': title, 'views': first_int})

        elif second_char == '천':
            first_int = int(first_char) * 1000
            trend_datas.append({'title': title, 'views': first_int})

    return trend_datas

# Final_Function 최종 뷰함수 #
def Final_Function(request):
    # 기상청 사이즈
    site = f"https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"
    keyword_data = {}
    date_data = {}
    search_type = {}  # html에서 받아오는 검색 타입
    selected_news = {}  # html에서 받아오는 언론사 유튜브 뉴스
    context = {}

    #요청받은 메소드 타입이 'POST'일 때
    if request.method == 'POST':
        # 키워드, 날짜 검색
        # html의 각 <input> 이름으로 입력받은 값을 받아옴
        keyword = request.POST.get('keyword')
        date = request.POST.get('date')
        search_type = request.POST.get('search_type')
        selected_news = request.POST.get('selected_news', '')
        weather_city = request.POST.get('weather_input')

        # 기상청 날씨 가져오기
        weather_data = get_weather_data(site, weather_city)

        if search_type == 'keyword':
            keyword_data = search_total_keyword(keyword)
            return render(request, '검색창.html', {'keyword_data': keyword_data})

        elif search_type == 'date':
            date_data = search_total_date(date)

        # 뉴스 유튜브 링크 오픈
        elif selected_news == 'naver':
            naver_news_link = 'https://news.naver.com/'
            return redirect(naver_news_link)

        elif selected_news == 'bbc':
            bbc_news_link = 'https://www.bbc.com/news'
            return redirect(bbc_news_link)

        # html에 넘겨줄 변수 저장
        context = {
            'keyword_data': keyword_data,
            'date_data': date_data,
            'weather_data': weather_data
        }

        # 'post' 메소드 들어왔을 때 실행
        return render(request, 'news_DB/testHtml.html', context)

    return render(request, 'news_DB/testHtml.html', context)

# 언론사별 유튜브 열람 #
def open_news_youtube(request):
    if request.method == 'POST':
        # POST 메소드가 들어왔을 때의 처리
        # form에서 전달된 값을 확인하여 링크를 설정
        selected_news = request.POST.get('selected_news', '')

        if selected_news == 'naver':
            naver_news_link = 'https://news.naver.com/'
            return redirect(naver_news_link)
        elif selected_news == 'bbc':
            bbc_news_link = 'https://www.bbc.com/news'
            return redirect(bbc_news_link)

    # GET 요청이나 다른 메소드에 대한 처리
    # 여기에 필요한 코드 추가

    return render(request, 'news_DB/youtubeHtml.html')

# DB로부터 검색 기능 (키워드, 날짜) #
def search_total_keyword(_keyword):
    news_data = models.NewsDB.load_news_db()

    data_list = []

    for data in news_data:
        # 해당 데이터에 keyword 필드가 있다면 수행
        if data.keywords:
            #키워드를 쉼표를 기준으로 단어들을 나눔 (몽고DB에 키워드가 쉼표로 분리되어 저장되어 있음)
            keyword_list = data.keywords.split(',')

            for keyword in keyword_list:
                # 입력받은 키워드와 동일한 키워드라면
                if _keyword == keyword:
                    data_list.append(data)

    return data_list

def search_total_date(_date):
    #DB 안의 데이터 내용 가져오기
    naver_data = models.naverDB.load_naver_db()

    data_list = []

    for data in naver_data:
        if _date in data.date:
            data_list.append(data)

    return data_list

# 분리해서 검색 #
def load_newsDB_keyword(request):
    Input = {}
    loaded_data = {}

    if request.method == 'POST':
        Input = request.POST.get('keyword')
        #loaded_data = search_keyword(Input)
        loaded_data = search_keyword_newsDB(Input)

    return render(request, 'news_DB/mongoHtml.html', {'loaded_data': loaded_data})

def search_keyword_newsDB(_keyword):
    loaded_data = models.NewsDB.load_news_db()

    data_list = []

    for data in loaded_data:
        # 해당 데이터에 keyword 필드가 있다면 수행
        if data.keywords:
            keyword_list = data.keywords.split(',')  # 키워드를 쉼표를 기준으로 단어들을 나눕니다.

            for keyword in keyword_list:
                # 입력받은 키워드와 동일한 키워드라면
                if _keyword == keyword:
                    data_list.append(data)

    return data_list

def load_naverDB_keyword(request):
    Input = {}
    loaded_data = {}

    if request.method == 'POST':
        Input = request.POST.get('keyword')
        #loaded_data = search_keyword(Input)
        loaded_data = search_keyword_naverDB(Input)

    return render(request, 'news_DB/mongoHtml.html', {'loaded_data': loaded_data})

def search_keyword_naverDB(_keyword):
    loaded_data = models.naverDB.load_naver_db()

    data_list = []

    for data in loaded_data:
        if _keyword in data.date:
            data_list.append(data)

    return data_list

class RandomFactNewsView(View):
    template_name = 'db.html'

    def get(self, request, *args, **kwargs):
        # 데이터베이스에서 모든 데이터 가져오기
        all_data = models.FactNews.objects.all()

        # 랜덤하게 하나의 데이터 선택
        random_fact_news = random.choice(all_data)

        # 선택된 데이터를 템플릿에 전달
        context = {
            'random_fact_news': random_fact_news,
        }

        return render(request, self.template_name, context)

    # views.py

    from django.shortcuts import render
    import requests
    from bs4 import BeautifulSoup

def get_news_data(search_term, site):
    url = f'https://news.google.com/rss/search?q={search_term}+site:{site}&hl=ko&gl=KR&ceid=KR:ko'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')

    items = soup.find_all('item')

    # title, link 정보를 저장할 리스트 초기화
    titles = []
    links = []

    for item in items:
        title = item.find('title').text if item.find('title') else 'No title'
        link = item.find('link').text if item.find('link') else 'No link'

        titles.append(title)
        links.append(link)

    return titles, links

def press_search(request):
    # 기본값 설정
    titles, links = ['No Data'], ['No Data']

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        site = request.POST.get('site')
        titles, links = get_news_data(search_term, site)

    # context에 검색 결과 추가
    titles_and_links = [{'title': title, 'link': link} for title, link in zip(titles, links)]

    context = {
        'titles_and_links': titles_and_links,
    }

    return render(request, 'press_search.html', context)


# views.py

def import_data_from_mongodb(request):
    # MongoDB 연결
    datas = models.NewsDB.load_news_db_category()

    keyword = '경제'
    filter_query = {
        '$or': [
            {'통합 분류1': keyword},
            {'통합 분류2': keyword},
            {'통합 분류3': keyword},
            {'키워드': keyword}
        ]
    }
    cursor = datas.find(filter_query)

    return render(request, '경제.html', {'articles': cursor})

from pymongo import MongoClient

def economic_category(request):
    data_list = search_category('경제')
    return render(request, 'categoryHtml.html', {'keyword': '경제', 'data_list': data_list})

def politics_category(request):
    data_list = search_category('정치')
    return render(request, 'categoryHtml.html', {'keyword': '정치', 'data_list': data_list})

def sports_category(request):
    data_list = search_category('스포츠')
    return render(request, 'categoryHtml.html', {'keyword': '스포츠', 'data_list': data_list})

def search_category(_keyword):
    # 기상청 날씨 가져오기
    news_data = models.NewsDB.load_news_db_all()

    data_list = []

    if news_data is not None:
        for data in news_data:

                keyword_matched = False
                category1_matched = False
                category2_matched = False
                category3_matched = False

                # 해당 데이터에 keyword 필드가 있다면 수행
                # 키워드를 쉼표를 기준으로 단어들을 나눔 (몽고DB에 키워드가 쉼표로 분리되어 저장되어 있음)
                if data.keywords is not None:
                    keyword_list = data.keywords.split(',')
                    # 하나라도 '경제' 키워드가 있으면 해당 데이터를 한 번만 넣도록
                    keyword_matched = any(_keyword == keyword for keyword in keyword_list)

                if data.category1 is not None:
                    category1_matched = _keyword in data.category1
                if data.category2 is not None:
                    category2_matched = _keyword in data.category2
                if data.category3 is not None:
                    category3_matched = _keyword in data.category3

                if keyword_matched or category1_matched or category2_matched or category3_matched:
                    data_list.append(data)

    return data_list

# 메인 뉴스에 띄울 뉴스
# views.py
def mainnews():
    rss_url = "https://www.yonhapnewstv.co.kr/category/news/headline/feed/"
    feed = feedparser.parse(rss_url)

    items = []
    if not feed.bozo:
        for entry in feed.entries:
            title = entry.title
            description = entry.description
            content = entry.content[0].value if 'content' in entry and entry.content else ''
            enclosure_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else ''
            link_url = entry.link if isinstance(entry.link, str) else ''


            items.append({
                'title': title,
                'description': description,
                'content': content,
                'enclosure_url': enclosure_url,
                'link': link_url
            })

    return items

def get_trot():
    # XML 데이터 가져오기
    xml_url = 'https://fs.jtbc.co.kr/RSS/newsflash.xml'
    response = requests.get(xml_url)

    # 확인용: XML 데이터를 콘솔에 출력
    #print(response.content)

    # XML 파싱
    root = ET.fromstring(response.content)

    # 필요한 정보 추출
    items = root.findall('.//item')[:3]

    # 각 아이템에서 title, link, description 추출
    data_list = []
    for item in items:
        raw_title = item.find('title').text
        cleaned_title = raw_title.replace('\u0027', "'").replace('\n', ' ')
        title = escapejs(cleaned_title)
        link = escapejs(item.find('link').text)
        description = escapejs(item.find('description').text)

        data_list.append({'title': title, 'link': link, 'description': description})

    return data_list


