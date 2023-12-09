# views.py
from django.http import HttpResponse
from django.shortcuts import render
# 뉴스 날씨 가져오기 #
from urllib.parse import quote # 키워드 url과 합치기 위해 매개변수 타입 변환용
from .forms import  WeatherForm

import feedparser # RSS 피드 파싱용

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

def my_view(request):
    weather_data = get_weather_data('Seoul')
    return render(request, 'news_DB/viewHtml.html', {'weather_data': weather_data})


# 키워드 입력받는 함수
from django.shortcuts import render
from .forms import WeatherForm
from .views import get_weather_data

def get_weather(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            weather_city = form.cleaned_data['city']
            # get_weather_data 함수를 호출하여 날씨 데이터를 가져옴
            weather_data = get_weather_data(weather_city)
            return render(request, 'news_DB/testHtml.html', {'form': form, 'weather_data': weather_data})
    else:
        form = WeatherForm()

    return render(request, 'news_DB/testHtml.html', {'form': form})

# 날씨 데이터 가져오기
weather_city = 'Seoul'
weather_titles = get_weather_data(weather_city)

#확인용
weather_data = get_weather_data(weather_city)
print(weather_data)
print(weather_titles)