from django.urls import path

from . import views

urlpatterns = [
    path('game_view', views.game_view, name='game_view'),
]