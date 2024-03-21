# from meshpy import meshpy
from meshpy.meshpy.geometry import make_box, make_cylinder
import meshpy
from rich import inspect
from rich import print as rprint

class MeshBuilder:

    def flatten_list(self,lst):
      """
      Flattens a list of lists without using itertools.chain.

      Args:
          lst: A list of lists to flatten.

      Returns:
          A single list containing all elements from the nested lists.
      """
      flattened_list = []
      for sublist in lst:
        flattened_list.extend(sublist)
      return flattened_list
    
    def correct_cylinder_data(self, vertices, faces):
        """
        Corrige os dados da caixa gerada pela função make_box.

        Argumentos:
            vertices (list): Lista de vértices da caixa.
            faces (list): Lista de faces da caixa.

        Retorna:
            tuple: Tupla contendo os vértices e as faces corrigidas.
        """
      
        flat_vertices = self.flatten_list(vertices)
        hot_fix_faces_list = []
        for face in faces:
            hot_fix_faces_list += [face, face, face]

        flat_faces = self.flatten_list(hot_fix_faces_list)

        return flat_vertices, self.flatten_list(flat_faces)
    
    def correct_box_data(self, vertices, faces):
        """
        Corrige os dados da caixa gerada pela função make_box.

        Argumentos:
            vertices (list): Lista de vértices da caixa.
            faces (list): Lista de faces da caixa.

        Retorna:
            tuple: Tupla contendo os vértices e as faces corrigidas.
        """

        flat_vertices = self.flatten_list(vertices)
        hot_fix_faces_list = []
        for face in faces:
            hot_fix_faces_list += [face, face, face]

        flat_faces = self.flatten_list(hot_fix_faces_list)

        return flat_vertices, flat_faces
    

    def create_box_mesh(self, height, width, length, pos):
        """
        Creates a box mesh using MeshPy.

        Args:
            height (float): Height of the box.
            width (float): Width of the box.
            length (float): Length of the box.
            pos (tuple, optional): Position of the box's lower-left corner. Defaults to (0, 0, 0).

        Returns:
            tuple: A tuple containing two lists: vertices and faces of the box mesh.
        """

        min_corner = (0, 0, 0)
        max_corner = (width, height, length)

        # Ensure correct dimensions are passed to make_box
        box = make_box(min_corner, max_corner)

        return self.correct_box_data(box[0], box[1])
    
    def create_cylinder_mesh(self, radius, height, pos):
        """
        Creates a cylinder mesh using MeshPy.

        Args:
            radius (float): Radius of the cylinder.
            height (float): Height of the cylinder.
            pos (tuple, optional): Position of the cylinder's base center. Defaults to (0, 0, 0).

        Returns:
            tuple: A tuple containing two lists: vertices and faces of the cylinder mesh.
        """

        cylinder = make_cylinder(radius, height)

        
        return self.correct_cylinder_data(cylinder[0], cylinder[1])
