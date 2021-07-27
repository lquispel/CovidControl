from django.urls import path

from . import views

urlpatterns = [
    path('player_view', views.player_view, name='player_view'),
]