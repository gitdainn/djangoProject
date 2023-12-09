#from django.test import TestCase

# Create your tests here.

from urllib.parse import quote # 키워드 url과 합치기 위해 매개변수 타입 변환용
from .forms import  WeatherForm
from django.shortcuts import render
from .forms import WeatherForm

import feedparser # RSS 피드 파싱용

def get_weather_data2(city):
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

def my_view(request):
    weather_data = None  # 초기화

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data2(city)

    else:
        form = WeatherForm()

    return render(request, 'news_DB/testHtml.html', {'form': form, 'weather_data': weather_data})
