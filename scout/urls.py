from django.urls import path

from . import views

app_name = 'scout'

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<str:player_nick>/',views.scout_report, name='report'),


]
