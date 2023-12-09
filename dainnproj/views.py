# views.py
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote # 키워드 url과 합치기 위해 매개변수 타입 변환용
from .forms import  WeatherForm # forms.py의 Weatherform 클래스 실행함

import requests
from bs4 import BeautifulSoup
import feedparser # RSS 피드 파싱용-

def get_weather_data(city):
    encoded_city = quote(city)
    rss_url = f'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108&city={encoded_city}'
    feed = feedparser.parse(rss_url)

    # title과 link 정보를 저장할 리스트 초기화
    weather_data = []

    for entry in feed.entries:
        title = entry.title if hasattr(entry, 'title') else 'No title'
        link = entry.link if hasattr(entry, 'link') else 'No link'

        weather_data.append({'title': title, 'link': link})

    return weather_data

def get_weather_data_xml(site, searchcity):
    #encoded_city = quote(city)
    #rss_url = f'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108&city={encoded_city}'
    response = requests.get(site)

    # site로부터 제대로 추출됐을 경우 == 200
    #if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'xml')

    items = soup.find_all('item')
    # title과 link 정보를 저장할 리스트 초기화
    weather_data = []

    # .find(태그명) 해당 태그의 첫 번째 태그 값을 반환함


    for item in items:
    # 찾은 모든 city 태그에 대해 반복
        city_tags = item.find_all('city')
        for city_tag in city_tags:
            # 찾은 city 태그 값이 입력받은 도시명과 동일하다면
            if searchcity == city_tag.text:
                city_result = city_tag.text if city_tag else 'No city'
                # 해당 city의 data 태그 모두 가져옴
                data_list = item.find_all('data')
                for data in data_list:
                    tmEf = data.find('tmEf').text
                    wf = data.find('wf').text
                    tmn = data.find('tmn').text

                    weather_data.append({'city': city_result, 'datetime': tmEf, 'weather': wf, 'tmn': tmn})

                #weather_data.append({'city': city_result, 'datetime': tmEf, 'weather': "0", 'tmn': "0"})

        else:
            print("해당 도시가 없습니다.")

    return weather_data

def dainn_weather(request):
    context = {} # 초기화

    if request.method == 'POST':
        weather_city = request.POST.get('weather_city')
        #site = request.POST.get('site')
        site = f"https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"
        weather_data = get_weather_data_xml(site, weather_city)

        context = {
            'weather_data': weather_data
        }

    return render(request, 'news_DB/viewHtml.html', context)

def my_view(request):
    weather_data = get_weather_data('Seoul')
    return render(request, 'news_DB/weatherHtml.html', {'weather_data': weather_data})

def get_weather_data_form(city):
    encoded_city = quote(city)
    rss_url = f'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108&city={encoded_city}'
    feed = feedparser.parse(rss_url)

    # RSS피드에서 날씨 정보 추출
    weather_data = []
    for item in feed.entries:
        date = item.title
        description = item.description
        weather_data.append({
            'date': date,
            'description': description
        })

    return weather_data

def get_weather(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        # 폼이 유효한 경우, 입력값을 사용하여 날씨 데이터를 가져오는 로직을 추가
        if form.is_valid():
            weather_city = form.cleaned_data['city']
            # get_weather_data 함수를 호출하여 날씨 데이터를 가져옴
            # 날씨 데이터를 가져오는 함수 또는 API 호출 등을 수행
            weather_data = get_weather_data_form(weather_city)
            return render(request, 'news_DB/testHtml.html', {'form': form, 'weather_data': weather_data})
    else:
        form = WeatherForm()

    return render(request, 'news_DB/testHtml.html', {'form': form})


def get_news_data(search_term, site):
    url = f'https://news.google.com/rss/search?q={search_term}+site:{site}&hl=ko&gl=KR&ceid=KR:ko'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')

    items = soup.find_all('item')

    # title과 link 정보를 저장할 리스트 초기화
    titles = []
    links = []

    for item in items:
        title = item.find('title').text if item.find('title') else 'No title'
        link = item.find('link').text if item.find('link') else 'No link'

        titles.append(title)
        links.append(link)

    return titles, links

# DB_news/views.py
def news_search(request):
    titles, links = ['No Data'], ['No Data']
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        site = request.POST.get('site')
        titles, links = get_news_data(search_term, site)

    # views.py
    context = {
        'titles_and_links': zip(titles, links),
    }

    return render(request, 'news_DB/newsHtml.html', context)
