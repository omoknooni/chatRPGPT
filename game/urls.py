from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='index'),
    path('create/', views.create_game_session, name='create_session'),
    path('join/<int:session_id>/', views.join_game_session, name='join_session'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('select-theme/<int:session_id>/', views.select_theme, name='select_theme'),
]
