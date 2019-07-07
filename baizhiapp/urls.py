
from django.urls import path
from baizhiapp.views import *
app_name = 'baizhiapp'

urlpatterns = [
    path('introduce/',introduce,name = 'introduce'),
    path('login/',login,name = 'login'),
    path('main/',main,name = 'main'),
    path('menu/',menu,name = 'menu'),
    path('mainc/',mainc,name = 'mainc'),
    path('register/',register,name = 'register'),
    path('register_logic/',register_logic,name = 'register_logic'),
    path('login_logic/',login_logic,name = 'login_logic'),
    path('move_code/',move_code,name = 'move_code'),
    path('decorate/',decorate,name='decorate'),
]