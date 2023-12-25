import os
import sys
import constants as c
from swarmSimulation import SWARM_SIMULATION
import pybullet as p

# Playback swarm of robots
overallBot = 0
for swarm in range(c.numberOfSwarms):
    for bot in range(c.botsPerSwarm):
        botInSwarm = overallBot % 10
        swarmSim = SWARM_SIMULATION('GUI', overallBot)
        swarmSim.Run()
        swarmSim.Get_Fitness()
        overallBot += 1
p.disconnect()


