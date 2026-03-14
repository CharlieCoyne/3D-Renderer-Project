import math

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def get_unit_vector(self) -> "Vector3":
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        if length == 0:
            return Vector3(0, 0, 0)

        return Vector3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def do_unit_dot_product(self, vector2: "Vector3") -> float:
        vector1_unit = self.get_unit_vector()
        vector2_unit = vector2.get_unit_vector()

        return (
            vector1_unit.x * vector2_unit.x +
            vector1_unit.y * vector2_unit.y +
            vector1_unit.z * vector2_unit.z
        )

    def get_unit_normal_vector(self, vector2: "Vector3") -> "Vector3":
        normal = Vector3()
        normal.x = self.y * vector2.z - self.z * vector2.y
        normal.y = self.z * vector2.x - self.x * vector2.z
        normal.z = self.x * vector2.y - self.y * vector2.x

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

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
        