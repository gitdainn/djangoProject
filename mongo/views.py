# views.py
from django.shortcuts import render
from django.http import HttpResponse
from . import models

import pymongo
from pymongo import MongoClient

def save_testDB(request):
    # 저장
    weather_data = models.Weather(
        observation_point="울산",
        observation_time="2021-07-07 15:00:00",
        sea_level=61.0,
        water_temperature=21.5,
        salinity=30.3,
        temperature=23.5,
        pressure=1007.7,
        wind_direction=272.0,
        wind_speed=0.6,
        gust=1.2
    )
    weather_data.save()

    return

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

def total(request):
    total_data = {}

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        date = request.POST.get('date')
        search_type = request.POST.get('search_type')

        if search_type == 'keyword':
            total_data = search_total_keyword(keyword)
            return HttpResponse(f"NoData:{total_data}")


        elif search_type == 'date':
            total_data = search_total_date(date)

    return render(request, 'news_DB/mongoHtml.html', {'total_data': total_data})

def search_total_keyword(_keyword):
    news_data = models.NewsDB.load_news_db()

    data_list = []

    for data in news_data:
        # 해당 데이터에 keyword 필드가 있다면 수행
        if data.keywords:
            keyword_list = data.keywords.split(',')  # 키워드를 쉼표를 기준으로 단어들을 나눕니다.

            for keyword in keyword_list:
                # 입력받은 키워드와 동일한 키워드라면
                if _keyword == keyword:
                    data_list.append(data)

    return data_list


def search_total_date(_date):
    naver_data = models.naverDB.load_naver_db()

    data_list = []

    for data in naver_data:
        if _date in data.date:
            data_list.append(data)

    return data_list

def test(request):
    loaded_data = models.NewsDB.load_news_db()

    keyword_data = search_total_keyword('폭염')
    date_data = search_total_keyword('2022.01.03')
    return render(request, 'news_DB/mongoHtml.html', {'loaded_data': loaded_data})

def find_fieldname(request):
    database = models.naverDB.database() # 아 .. database 함수 지워버렸따 ..
    keys = database.keys()
    keys_str = "\n".join(keys)
    return HttpResponse(f"Field Names:\n{keys_str}")


