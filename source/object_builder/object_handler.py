from object_builder.shape_handler import ShapeHandler
from scipy.spatial.transform import Rotation
import math
from rich import inspect

class ObjectHandler(ShapeHandler):

    _alias = None
    id = None
    properties = None

    def __init__(self, sim, name_alias=None):
        super(ObjectHandler, self).__init__(sim)

        """
        Inicializa a classe `ShapeHandler`.

        Parâmetros:
            sim: Instância do simulador sim.
        """
        
        self.sim = sim
        self._alias = name_alias
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

    @property
    def position(self):
        if not self.id:
            raise Exception(f'Object does not exist')
        self._position = self.sim.getObjectPosition(self.id, self._position_type)
        return self._position

    @position.setter
    def position(self, pos):
        if not self.id:
            raise Exception(f'Object does not exist')
        self.sim.setObjectPosition(self.id, pos, self._position_type)
        self._position = self.sim.getObjectPosition(self.id, self._position_type)

    def rotacionar_objeto(self, angulo_x=0, angulo_y=0, angulo_z=0):
        if not self.id:
            raise Exception(f'Object does not exist')
        
        eulerAngles = self.sim.getObjectOrientation(self.id, self._position_type)

        eulerAngles[0] += math.radians(angulo_x)
        eulerAngles[1] += math.radians(angulo_y)
        eulerAngles[2] += math.radians(angulo_z)
      
        self.sim.setObjectOrientation(self.id, eulerAngles, self._position_type)

    def bound_object_parent(self, parent_object):
        if not self.id:
            raise Exception(f'Object does not exist')
        
        self.sim.setObjectParent(self.id, parent_object.id, False)
        self._parent_object = parent_object
        self._position_type = self.sim.handle_parent

    def __str__(self) -> str:
        return self.alias


class BoxHandler(ObjectHandler):
    x_dimension = None
    y_dimension = None
    z_dimension = None

    def __init__(self, sim, name_alias=None):
        super().__init__(sim, name_alias)

    def create_object(self, x_dimension, y_dimension, z_dimension, pos=(0, 0, 0), properties={}):
        if self.id:
            raise Exception(f'Object alredy exist [id={self.id}, alias={self.alias}]')

        self.id = self.create_box_object(x_dimension, y_dimension, z_dimension, pos, properties)

        self.alias = self._alias if self._alias else 'shape'
     
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.z_dimension = z_dimension
 


class CylinderHandler(ObjectHandler):
    radius = None
    height = None 

    def __init__(self, sim, name_alias=None):
        super().__init__(sim, name_alias)

    def create_object(self, radius, height, pos=(0, 0, 0), properties={}):
        if self.id:
            raise Exception(f'Object alredy exist [id={self.id}, alias={self.alias}]')
        
        self.id = self.create_cylinder_object(radius, height, pos, properties)
        self.alias = self._alias if self._alias else 'shape'

        self.radius = radius
        self.height = height
    
        