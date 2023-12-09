from django.urls import path, include
from . import views
from allauth.account.views import LogoutView, LoginView

urlpatterns = [
    #path('', views.Final_Function) #Final_Function
    # 진회 로그인
    path('', LoginView.as_view(), name='login'),  # 기본 홈페이지를 로그인 뷰로 지정
    path('rss-feed/', views.rss_feed, name='rss_feed'),
    path('main/', views.main, name='main'),  # main 뷰에 대한 URL 패턴 추가
    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),

    #path('import-data/', views.import_data_from_mongodb, name='import_data_from_mongodb'),
    path('economic_category/', views.economic_category, name='economy'),
    path('politics_category/', views.politics_category, name='politics'),
    path('sports_category/', views.sports_category, name='sports'),

    # 기능
    path('', views.db_home, name='db_home'),
    path('', views.trend_data, name='trend_data'),
    path('date_search/', views.date_search, name='date_search'),
    path('keyword_search/', views.keyword_search, name='keyword_search'),
    path('weather_search/', views.weather_search, name='weather_search'),
    path('press_search/', views.press_search, name='press_search'),
]