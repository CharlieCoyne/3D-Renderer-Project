import math

class Vector3:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def add(self, vector2):
        return Vector3(self.x + vector2.x, self.y + vector2.y, self.z + vector2.z)

    def subtract(self, vector2):
        return Vector3(self.x - vector2.x, self.y - vector2.y, self.z - vector2.z)
    
    def get_unit_vector(self) -> "Vector3":
        length = self.get_length()

        if length == 0:
            return Vector3(0, 0, 0)

        return Vector3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def do_dot_product(self, vector2: "Vector3") -> float:
        return (
            self.x * vector2.x +
            self.y * vector2.y +
            self.z * vector2.z
        )

    def do_unit_dot_product(self, vector2: "Vector3") -> float:
        vector1_unit = self.get_unit_vector()
        vector2_unit = vector2.get_unit_vector()

        return (
            vector1_unit.x * vector2_unit.x +
            vector1_unit.y * vector2_unit.y +
            vector1_unit.z * vector2_unit.z
        )
    
    def do_vector_cross_product(self , vector2):
        new_vector = Vector3()
        new_vector.x = self.y * vector2.z - self.z * vector2.y
        new_vector.y = self.z * vector2.x - self.x * vector2.z
        new_vector.z = self.x * vector2.y - self.y * vector2.x
        return new_vector

    def get_unit_normal_vector(self, vector2: "Vector3") -> "Vector3":
        normal = self.do_vector_cross_product(vector2)
        unit_normal = normal.get_unit_vector()
        
        return unit_normal
    
    def do_vector_matrix_multiplication(self, m) -> "Vector3":
        output_vector = Vector3()
        output_vector.x = self.x * m[0][0] + self.y * m[1][0] + self.z * m[2][0] + m[3][0]
        output_vector.y = self.x * m[0][1] + self.y * m[1][1] + self.z * m[2][1] + m[3][1]
        output_vector.z = self.x * m[0][2] + self.y * m[1][2] + self.z * m[2][2] + m[3][2]
        w               = self.x * m[0][3] + self.y * m[1][3] + self.z * m[2][3] + m[3][3]

        # Normalising vector
        if w != 0:
            output_vector.x /= w
            output_vector.y /= w
            output_vector.z /= w 

        return output_vector

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
        