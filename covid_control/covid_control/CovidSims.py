from datetime import date
from datetime import timedelta

import covasim as cv

class CovasimSim:

    def __init__(self):
        cv.options.set(dpi=100, show=False, close=True, verbose=0)

    def initialize(self,start_day_date,end_day_date):
        sim = cv.Sim(start_day=start_day_date,end_day=end_day_date)
        sim.save('gamedata/my_sim.sim')

    def step(self,end_date,path='gamedata/'):
        sim = cv.load(path + 'my_sim.sim')
        sim.run(until=end_date.isoformat())
        sim.save('gamedata/my_sim.sim')

