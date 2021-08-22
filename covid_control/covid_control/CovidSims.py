from datetime import date
from datetime import timedelta

import covasim as cv

class CovasimSim:

    def __init__(self):
        cv.options.set(dpi=100, show=False, close=True, verbose=1)

    def initialize(self,start_day_date='2019-01-19'):
        start_date = date.fromisoformat(start_day_date)
        end_date = start_date + timedelta(days=1)
        sim = cv.Sim(start_day=start_day_date,end_day=end_date.isoformat())
        sim.save('gamedata/my_sim.sim')

    def step(self,step_size=1):
        sim = cv.load('gamedata/my_sim.sim')
        start_date = date.fromisoformat( str(sim.pars['end_day']) )
        sim.pars['start_day'] = start_date.isoformat()
        sim.pars['end_day'] = (start_date + timedelta(days=step_size)).isoformat()
        sim.initialize()
        sim.run()
        sim.save('gamedata/my_sim.sim')

