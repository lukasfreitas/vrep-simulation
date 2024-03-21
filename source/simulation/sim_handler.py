from object_builder.object_handler import ObjectHandler
from object_builder.joint_handler import JointHandler
from models.car.car_handler import CarHandler
from server.server import client
from rich import inspect

class Simulation:
    
    objects = []

    def __init__(self):

        self.sim = client.require('sim')
     

    def insert_objects(self):
        car = CarHandler(self.sim)
        car.build(x_dimension=0.5, y_dimension=0.75, z_dimension=0.2, pos=(1,0,1))

    def setup(self):
       self.sim.setArrayParam(self.sim.arrayparam_gravity, [0,0,-9.81]) 
    
    def context(self):
        ...

    def run(self, duration_seconds=None):
        self.insert_objects()
        self.setup()
        self.sim.setStepping(True)

        self.sim.startSimulation()
        
        t = 0
        duration_rule = True if not duration_seconds else (t := self.sim.getSimulationTime()) < duration_seconds
        while duration_rule:
            duration_rule = True if not duration_seconds else (t := self.sim.getSimulationTime()) < duration_seconds
            self.sim.step()
         
            # print(f'Simulation time: {t:.2f} [s]')
            self.context()
            
            
        self.sim.stopSimulation()