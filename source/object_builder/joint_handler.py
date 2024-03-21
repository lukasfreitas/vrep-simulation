
from rich import inspect
import numpy as np
import math
class JointHandler:

    _alias = None
    id = None
    _position = (0,0,0)

    _parent_object = None

    def __init__(self, sim, name_alias=None):
 
        self.sim = sim
        self._alias = name_alias
        self.joint_type = {
        'revolute':self.sim.joint_revolute_subtype,
        'prismatic':self.sim.joint_prismatic_subtype,
        'spherical':self.sim.joint_spherical_subtype
        }
        self._position_type = self.sim.handle_world

    @property
    def alias(self):
        if self.id:
            self._alias = self.sim.getObjectAlias(self.id)
        return self._alias

    @alias.setter
    def alias(self, alias):
        self._alias = alias

        if self.id:
            self.sim.setObjectAlias(self.id, alias)

    def load_joint_object(self,joint_type, length, diameter):
        if self.id:
            raise Exception(f'Joint alredy exist [id={self.id}, type={self.joint_type[joint_type]}]')
        
        self.id = self.sim.createJoint(self.joint_type[joint_type],  self.sim.joint_revolute_subtype, 0, (length,diameter))
        self.alias = self._alias if self._alias else 'shape'

    def bound_joint_parent(self, parent_object):
        if not self.id:
            raise Exception(f'Joint doas not exist')
        
        self.sim.setObjectParent(self.id, parent_object.id, False)
        self._parent_object = parent_object
        self._position_type = self.sim.handle_parent
    
    def rotacionar_objeto(self, angulo_x=0, angulo_y=0, angulo_z=0):
      
        eulerAngles = self.sim.getObjectOrientation(self.id, self._position_type)

        eulerAngles[0] += math.radians(angulo_x)
        eulerAngles[1] += math.radians(angulo_y)
        eulerAngles[2] += math.radians(angulo_z)
      
        self.sim.setObjectOrientation(self.id, eulerAngles, self._position_type)

    @property
    def position(self):
        if not self.id:
            raise Exception(f'Joint doas not exist')
        self._position = self.sim.getObjectPosition(self.id, self._position_type)

        return self._position

    @position.setter
    def position(self, pos):
        if not self.id:
            raise Exception('Joint does not exist')

        center_pos = pos
        self.sim.setObjectPosition(self.id, center_pos, self._position_type)
        self._position = self.sim.getObjectPosition(self.id, self._position_type)

   
        