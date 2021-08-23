from django.db import models

from datetime import date
from datetime import timedelta

import sys

from covid_control.CovidSims import CovasimSim

class Player(models.Model):
    name = models.CharField(max_length=200,default='anonymous')

    def __str__(self):
        return self.name

class GameState(models.Model):
    current_turn = models.IntegerField(default=1)
    current_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.game) + "_t" + str(self.current_turn)

class Simulation(models.Model):
    type = models.CharField(max_length=20,default="")
    sim = None

    def init(self,type="covasim",start_date='2019-01-19',end_date='2021-09-01'):
        self.type = type
        if type == "covasim":
            self.sim = CovasimSim()
        self.sim.initialize(start_day_date=start_date,end_day_date=end_date)

    def step(self,step_size):
        if self.type == "covasim":
            self.sim = CovasimSim()
        self.sim.step(step_size)

class Settings(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE,related_name="settings")
    step_size = models.IntegerField(default=1)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "settings_" + str(self.id)

class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,related_name="games")
    game_state = models.OneToOneField(GameState, on_delete=models.CASCADE, related_name="game")
    history = models.ManyToManyField(GameState,related_name="created_by")
    settings = models.ForeignKey(Settings,on_delete=models.CASCADE,related_name="games")

    def __str__(self):
        return str(self.player.id) + "_" + str(self.id) + "_" + self.player.name

    def next_turn(self):
        current_turn = self.game_state.current_turn + 1
        current_date = self.game_state.current_date + timedelta(days=self.settings.step_size)
        self.history.add(self.game_state)
        self.settings.simulation.step(current_date)
        self.game_state = GameState()
        self.game_state.current_turn = current_turn
        self.game_state.current_date = current_date
        self.game_state.save()
        self.save()

    @classmethod
    def create_game(cls, player=None, settings=None):
        try:
            game = cls()
            if player == None:
                player = Player()
                player.save()
            game.player = player
            if settings == None:
                settings = Settings()
                settings.step_size = 3
                settings.start_date = date.fromisoformat('2019-01-23')
                settings.end_date = date.fromisoformat('2021-09-01')
                simulation = Simulation()
                simulation.init(type="covasim",start_date=settings.start_date.isoformat(),end_date=settings.end_date.isoformat())
                simulation.save()
                settings.simulation = simulation
                settings.save()
            game.settings = settings
            gamestate = GameState()
            gamestate.current_date = settings.start_date
            gamestate.save()
            game.game_state = gamestate
            game.save()
            return game
        except:
            print(sys.exc_info()[1])
            return None



    

