from .utils import natural_colors
from .mesh_handler import MeshBuilder
from rich import inspect

class ShapeHandler(MeshBuilder):
    """
    Classe que abstrai a criação de objetos a partir de malhas no simulador sim.

    Esta classe herda da classe `MeshHandler` e fornece métodos para criar objetos simples a partir de malhas de caixa.

    Atributos:
        sim: Instância do simulador sim.

    Métodos:
        create_box_object(self, height, width, length, pos=(0, 0, 0)):
            Cria um objeto caixa no simulador sim.

            Parâmetros:
                height (float): Altura da caixa.
                width (float): Largura da caixa.
                length (float): Comprimento da caixa.
                pos (tuple, opcional): Posição da caixa no mundo (padrão (0, 0, 0)).

            Retorna:
                int: ID do objeto criado no simulador.
    """

    mass = 0
    color = "green"

    def __init__(self, sim):
        """
        Inicializa a classe `ShapeHandler`.

        Parâmetros:
            sim: Instância do simulador sim.
        """
        self.sim = sim

    def _set_object_properties(self,obj, properties):
        self.mass = float(properties.get('mass',10))
     
        self.sim.setShapeMass(obj, self.mass)
        self.sim.setShapeColor(obj, self.color, 0, natural_colors[self.color])
        self.sim.computeMassAndInertia(obj, 2.3)

    def create_box_object(self, x_dimension, y_dimension, z_dimension, pos=(0, 0, 0), properties={}):
        """
        Cria um objeto caixa no simulador sim.

        Cria um objeto caixa com as dimensões especificadas e o posiciona no mundo.

        Parâmetros:
            height (float): Altura da caixa.
            width (float): Largura da caixa.
            length (float): Comprimento da caixa.
            pos (tuple, opcional): Posição da caixa no mundo (padrão (0, 0, 0)).

        Retorna:
            int: ID do objeto criado no simulador.
        """
        vertices, faces = super().create_box_mesh(y_dimension, x_dimension, z_dimension, pos)
       
        shadingAngle = 45.0
        options = 0
       
        obj = self.sim.createShape(options, shadingAngle, vertices, faces)
        self._set_object_properties(obj, properties={
           'mass':1,
        })
        
        return obj
    
    def create_cylinder_object(self, radius, height, pos=(0, 0, 0), properties={}):
        """
        Cria um objeto cilindro no simulador sim.

        Cria um objeto cilindro com as dimensões especificadas e o posiciona no mundo.

        Parâmetros:
            radius (float): Raio do cilindro.
            height (float): Altura do cilindro.
            pos (tuple, opcional): Posição do cilindro no mundo (padrão (0, 0, 0)).

        Retorna:
            int: ID do objeto criado no simulador.
        """
        vertices, faces = super().create_cylinder_mesh(radius, height, pos)
        shadingAngle = 45.0
        options = 0
       
        obj = self.sim.createShape(options, shadingAngle, vertices, faces)
        self._set_object_properties(obj, properties={
           'mass': 1,
        })
        
        return obj
