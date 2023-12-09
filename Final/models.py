# models.py
from pymongo import MongoClient
from django.db import models

class naverDB(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    image = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    media_outlet = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    article_link = models.URLField(blank=True, null=True)

    @staticmethod
    def database():
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['naverDB']

        return collection.find_one()  # Get one document as a sample

    @staticmethod
    def load_naver_db():
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('127.0.0.1', 27017)
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
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['newsDB']

        return collection.find_one()  # Get one document as a sample

    @staticmethod
    def load_news_db():
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['newsDB']

        # 처음 두 개의 문서만 가져오기
        mongo_documents = list(collection.find().limit(2))

        django_objects = []

        for doc in mongo_documents:
            django_objects.append(NewsDB(
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
            ))


        # for문 돌릴거면 [for doc in mongo_documents] 로 묶어주기

        return django_objects

    @staticmethod
    def load_news_db_all():
        client = MongoClient('mongodb://localhost:27017/')
        # client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['newsDB']

        mongo_documents = list(collection.find())

        django_objects = []

        for doc in mongo_documents:
            django_objects.append(NewsDB(
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
            ))

        # for문 돌릴거면 [for doc in mongo_documents] 로 묶어주기

        return django_objects

# djongo와 pymongo 연결하는 라우터
class Router:
    # 앱 'Final'이면 mongodb 사용, 그 외는 settings.py에서 설정한 default 데이터베이스를 사용하라는 뜻
    def db_for_read(self, model, **hints):
        if 'Final' in  model._meta.app_label.lower():
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if 'Final' in model._meta.app_label.lower():
            return 'mongodb'

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if 'final' in obj1._meta.app_label.lower() or 'final' in obj2._meta.app_label.lower():
            return True
        return None

class FactNews(models.Model):
    class Meta:
        db_table = 'factDB'  # 콜렉션 이름

    subject = models.CharField(max_length=255)
    fact = models.TextField()
    source = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.subject

class FactDB(models.Model):
    subject = models.CharField(max_length=255)
    fact = models.TextField()
    source = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.subject

    @staticmethod
    def load_fact():
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('127.0.0.1', 27017)
        db = client['newsDB']
        collection = db['factDB']

        # 처음 두 개의 문서만 가져오기
        mongo_documents = list(collection.find())

        django_objects = []

        for doc in mongo_documents:
            django_objects.append(FactDB(
                subject=doc.get('주제', None),
                fact=doc.get('팩트 사실', None),
                source=doc.get('출처', None),
                url=doc.get('url', None),
            ))

        # for문 돌릴거면 [for doc in mongo_documents] 로 묶어주기

        return django_objects

# models.py

class NewsArticle(models.Model):
    address = models.CharField(max_length=255)
    date = models.DateField()
    media = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.title
