from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='index'),
    path('create/', views.create_game_session, name='create_game_session'),
    path('join/', views.join_game_session, name='join_game_session'),
    path('session/<int:session_id>/', views.session_detail, name='game_session_detail'),
    path('select-theme/<int:session_id>/', views.select_theme, name='select_game_theme'),
]
