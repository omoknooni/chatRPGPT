from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GameSession, Theme
from .forms import ThemeSelectionForm

import random, json, redis

r = redis.Redis(host='localhost', port=6379, db=0)


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
            game_session.chat_channel_id = f"chat:{game_session.id}"
            game_session.save()

            # Redis에 채널 생성
            r.subscribe(game_session.chat_channel_id)

            # Game Session을 생성 후 이동
            return redirect('game:session_detail', {'session_id': game_session.id})
    else:
        form = ThemeSelectionForm()
    return render(request, 'game/create_game_session.html', {'form': form})

@login_required
def join_game_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        game_session = get_object_or_404(GameSession, id=session_id)
        game_session.players.add(request.user)

        # Redis 채널에 참가
        r.subscribe(game_session.chat_channel_id)
        return render(request, 'game/session_detail.html', {'game_session': game_session})
    elif request.method == 'GET':
        # 게임 세션 목록 조회, player가 4 이하인 항목만 조회
        game_sessions = GameSession.objects.filter(players__lte=4)
        return render(request, 'game/game_session_list.html', {'game_sessions': game_sessions})
    else:
        return redirect('game:home')


@login_required
def expire_game_session(request, session_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        game_session = get_object_or_404(GameSession, id=session_id)

        if game_session.players.count() == 0:
            game_session.is_active = False
            game_session.save()
    
    return redirect('game:home')


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

