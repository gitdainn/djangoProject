from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # dainnproj.urls에 있는 url과 합해짐 (즉, dainnproj.urls에 중복되는 함수 작성 X)
    path('', include('Final.urls')),
]