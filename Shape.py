from Vector3 import *
import trimesh

class Shape:
    def __init__(self, position : Vector3, filename=None):
        self.position = position 
        self.triangles = self.load_object(filename)
    
    def load_object(self, filename):
        vertices = []
        triangles = []

        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):  # Vertex line
                    _, x, y, z = line.strip().split()
                    vertices.append(Vector3(float(x), float(y), float(z)))
                elif line.startswith('f '):  # Face line
                    parts = line.strip().split()[1:]
                    indices = [int(p.split('/')[0]) - 1 for p in parts]  # OBJ is 1-indexed
                    # Assuming triangulated faces
                    if len(indices) == 3:
                        triangles.append([vertices[indices[0]],
                                        vertices[indices[1]],
                                        vertices[indices[2]]])
                    else:
                        # Split quad into two triangles
                        triangles.append([vertices[indices[0]], vertices[indices[1]], vertices[indices[2]]])
                        triangles.append([vertices[indices[0]], vertices[indices[2]], vertices[indices[3]]])
        return triangles