
from django.contrib import admin
from django.urls import path
#from .views import news_search
from . import views

urlpatterns = [
    #path('', news_search, name='news_search'),  # news_search 함수를 뷰로 사용
    #path('', views.my_view, name='dainnproj_myView'),
    #path('', views.news_search, name='dainnproj_newsSearch'),
    path('', views.dainn_weather, name='dainn')
    #path('', views.get_weather, name='dainnproj')

    # 원래는 경로 이렇게 지정해주면 서로 다른 뷰파일 여러 개를 띄울수 있다는데..
    # 나는 왜 루트 '' 에서만 실행이 되는지.. 그러면 첫번째 path만 맵핑이 됨
    #path('testView/', testView.index, name='testView_index'),
    #path('dainnproj/', views.my_view, name='my_view'),0
]