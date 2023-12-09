from django.apps import AppConfig

#이 name을 가지고 djongo와 pymongo를 연동
class FinalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Final'
