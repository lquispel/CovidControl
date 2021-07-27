from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Game,Player,Settings,Simulation,GameState

def player_view(request):
    try:
        current_player = Player.objects.get(id=request.session['player_id'])
        if request.session['current_game_id'] == 0:
            game = Game.create_game(player=current_player)
            if game == None:
                return HttpResponse("Error while creating game.")
        else:
            game = Game.objects.get(id=request.session['current_game_id'])
    except KeyError:
        request.session['player_id'] = 1
        request.session['current_game_id'] = 0
        return HttpResponse("Error: session corrupt. Quitting. Reload to use defaults.")
    except ObjectDoesNotExist:
        return HttpResponse("Error: player/game not found.")
    request.session['current_game_id'] = game.id
    if 'action' in request.GET:
        if request.GET.get('action') == 'next_turn':
            game.next_turn()
    return render(request, "GameEngine/player_view.html", {'game': game})

