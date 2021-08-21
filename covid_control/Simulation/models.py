from django.db import models

class Simulation(models.Model):
    n_total = models.IntegerField(default=0)
    n_infected = models.IntegerField(default=0)
    n_ill = models.IntegerField(default=0)
    n_dead = models.IntegerField(default=0)
    n_recovered = models.IntegerField(default=0)

    def step(self,state,stepsize):
        return state


