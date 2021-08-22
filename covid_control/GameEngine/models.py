from django.db import models

import sys

from covid_control.CovidSims import CovasimSim

class Player(models.Model):
    name = models.CharField(max_length=200,default='anonymous')

    def __str__(self):
        return self.name

class GameState(models.Model):
    current_turn = models.IntegerField(default=1)

    def __str__(self):
        return str(self.game) + "_t" + str(self.current_turn)

class Simulation(models.Model):
    type = models.CharField(max_length=20,default="")
    start_date = models.DateField()

    def init(self,type="covasim",start_date='2019-01-19'):
        self.type = type
        self.start_date = start_date
        if type == "covasim":
            sim = CovasimSim()
        sim.initialize(start_day_date=start_date)

    def step(self,step_size):
        if self.type == "covasim":
            sim = CovasimSim()
        sim.step(step_size)

class Settings(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE,related_name="settings")
    step_size = models.IntegerField(default=1)

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
        self.history.add(self.game_state)
        self.settings.simulation.step(self.settings.step_size)
        self.game_state = GameState()
        self.game_state.current_turn = current_turn
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
                simulation = Simulation()
                simulation.init()
                simulation.save()
                settings.simulation = simulation
                settings.save()
            game.settings = settings
            gamestate = GameState()
            gamestate.save()
            game.game_state = gamestate
            game.save()
            return game
        except:
            print(sys.exc_info()[1])
            return None



    

