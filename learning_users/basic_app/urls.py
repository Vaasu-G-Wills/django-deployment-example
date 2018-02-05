from django.urls import path
from . import views

#TEMPLATE TAGGING
app_name = 'basic_app'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.registration, name='registration'),
    path('special/', views.special, name='special'),
]
