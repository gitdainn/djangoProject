# models.py
from pymongo import MongoClient
from django.db import models
from django.core.files import File
import os

import requests
from urllib.parse import urlparse

class Weather:
    def __init__(self, observation_point, observation_time, sea_level, water_temperature, salinity, temperature, pressure, wind_direction, wind_speed, gust):
        self.observation_point = observation_point #관측명
        self.observation_time = observation_time #관측시간
        self.sea_level = sea_level #조위
        self.water_temperature = water_temperature #수온
        self.salinity = salinity #염분
        self.temperature = temperature #기온
        self.pressure = pressure #기압
        self.wind_direction = wind_direction #풍향
        self.wind_speed = wind_speed #풍속
        self.gust = gust #돌풍

    def save(self):
        client = MongoClient('127.0.0.1', 27017)
        db = client['testDB']
        weather_collection = db['weather']

        weather_data = {
            'observation_point': self.observation_point,
            'observation_time': self.observation_time,
            'sea_level': self.sea_level,
            'water_temperature': self.water_temperature,
            'salinity': self.salinity,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'wind_direction': self.wind_direction,
            'wind_speed': self.wind_speed,
            'gust': self.gust
        }

        weather_collection.insert_one(weather_data)

    @staticmethod
    def load_all():
        client = MongoClient('127.0.0.1', 27017)
        db = client['testDB']
        weather_collection = db['weather']

        return list(weather_collection.find())

class naverDB(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    image = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    media_outlet = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    article_link = models.URLField(blank=True, null=True)

    @staticmethod
    def database():
        client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['naverDB']

        return collection.find_one()  # Get one document as a sample

    @staticmethod
    def load_naver_db():
        client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['naverDB']

        mongo_documents = list(collection.find())  # MongoDB에서 모든 문서 가져오기

        django_objects = [naverDB(
            id=doc.get('_id', None),
            image=doc.get('이미지 URL', None),
            title=doc.get('제목', None),
            media_outlet=doc.get('언론사', None),
            date=doc.get('날짜', None),
            article_link=doc.get('기사 링크', None)
        ) for doc in mongo_documents]

        return django_objects

class NewsDB(models.Model):
    id = models.CharField(max_length=500, primary_key=True)
    address = models.URLField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    media_outlet = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    category1 = models.CharField(max_length=255)
    category2 = models.CharField(max_length=255)
    category3 = models.CharField(max_length=255)
    entity_location = models.CharField(max_length=255)
    entity_company = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    main_body = models.TextField()
    original_source = models.URLField()

    @staticmethod
    def database():
        client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['newsDB']

        return collection.find_one()  # Get one document as a sample

    @staticmethod
    def load_news_db():
        client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['newsDB']

        mongo_documents = list(collection.find())  # MongoDB에서 모든 문서 가져오기
        # doc = collection.find_one()  # MongoDB에서 한 문서 가져오기

        # MongoDB에서 가져온 데이터를 Django 모델로 변환
        # 클래스명(변수명=doc['mongoDB필드명'], ~)
        django_objects = [NewsDB(
            id=doc.get('_id', None),
            address=doc.get('주소', None),
            date=doc.get('일자', None),
            media_outlet=doc.get('언론사', None),
            author=doc.get('기고자', None),
            title=doc.get('제목', None),
            category1=doc.get('통합 분류1', None),
            category2=doc.get('통합 분류2', None),
            category3=doc.get('통합 분류3', None),
            entity_location=doc.get('개체명(지역)', None),
            entity_company=doc.get('개체명(기업기관)', None),
            keywords=doc.get('키워드', None),
            feature=doc.get('특성추출', None),
            main_body=doc.get('본문', None),
            original_source=doc.get('원본주소', None),

        ) for doc in mongo_documents]

        return django_objects