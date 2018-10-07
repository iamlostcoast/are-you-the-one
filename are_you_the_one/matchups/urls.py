from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matchups', views.matchups, name='matchups'),
    path('remove_matchups', views.remove_pairs, name='remove_matchups'),
    path('check_match', views.check_match, name='check_match'),
]