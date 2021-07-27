from django.contrib import admin

from .models import GameState,Player,Settings,Game,Simulation

admin.site.register(GameState)
admin.site.register(Player)
admin.site.register(Settings)
admin.site.register(Game)
admin.site.register(Simulation)
