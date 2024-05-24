from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GameSession, Theme
from .forms import ThemeSelectionForm

import random

def home(request):
    return render(request, 'game/home.html')

@login_required
def create_game_session(request):
    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            selected_theme = form.cleaned_data['theme']
            game_session = GameSession.objects.create(theme=selected_theme)
            game_session.players.add(request.user)
            return redirect('game:session_detail', id=game_session.id)
    else:
        form = ThemeSelectionForm()
    return render(request, 'game/create_game_session.html', {'form': form})

@login_required
def join_game_session(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)
    game_session.players.add(request.user)
    return redirect('game:session_detail', id=session_id)


@login_required
def session_detail(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)
    return render(request, 'game/session_detail.html', {'game_session': game_session})


@login_required
def select_theme(request, session_id):
    game_session = get_object_or_404(GameSession, id=session_id)

    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            selected_theme = form.cleaned_data['theme']
            game_session.theme = selected_theme
            game_session.save()
            return redirect('game:session_detail', session_id=game_session.id)
    else:
        form = ThemeSelectionForm()
    
    if not game_session.theme and game_session.players.count() > 0:
        # 투표 없으면 Theme 랜덤 선택
        select_theme = random.choice(form.fields['theme'].choices)[0]
        game_session.theme = select_theme
        game_session.save()
    return render(request, 'game/select_theme.html', {'form': form, 'game_session': game_session})

