from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Game,Player,Simulation

def game_view(request):
    try:
        current_player = Player.objects.get(id=request.session['player_id'])
    except:
        current_player = Player()
        current_player.save()
        request.session['player_id'] = current_player.id
    if request.method == 'POST':
        try:
            if request.POST.get('action') == 'next_turn':
                game = Game.objects.get(id=request.session['current_game_id'])
                game.next_turn()
            elif request.POST.get('action') == 'new_game':
                game = Game.create_game(player=current_player)
                if game == None:
                    return HttpResponse("Error while creating game.")
        except KeyError:
             return HttpResponse("Error: session corrupt. Quitting.")
        except ObjectDoesNotExist:
            return HttpResponse("Error: game not found.")
    else:
        if request.session['current_game_id']:
            game = Game.objects.get(id=request.session['current_game_id'])
        else:
            game = Game.create_game(player=current_player)
            if game == None:
                return HttpResponse("Error while creating game.")
    request.session['current_game_id'] = game.id
    return render(request, "GameEngine/game_view.html", {'game': game, 'mode': "master"})


