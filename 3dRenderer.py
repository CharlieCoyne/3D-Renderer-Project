# pygame is used to obtain inputs from the user and also display the rendering in a window 
import pygame
import sys
import math
from Vector3 import *

pygame.init()

# Pygame Settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3d Renderer")
start_time = pygame.time.get_ticks()

# Temporary Cube
cubeTriangles = [
    # South Triangles
    [Vector3(0,0,0), Vector3(0,1,0), Vector3(1,1,0)],
    [Vector3(0,0,0), Vector3(1,1,0), Vector3(1,0,0)],

    # East Triangles
    [Vector3(1,0,0), Vector3(1,1,0), Vector3(1,1,1)],
    [Vector3(1,0,0), Vector3(1,1,1), Vector3(1,0,1)],

    # North Triangles
    [Vector3(1,0,1), Vector3(1,1,1), Vector3(0,1,1)],
    [Vector3(1,0,1), Vector3(0,1,1), Vector3(0,0,1)],

    # West Triangles
    [Vector3(0,0,1), Vector3(0,1,1), Vector3(0,1,0)],
    [Vector3(0,0,1), Vector3(0,1,0), Vector3(0,0,0)],

    # Top Triangles
    [Vector3(0,1,0), Vector3(0,1,1), Vector3(1,1,1)],
    [Vector3(0,1,0), Vector3(1,1,1), Vector3(1,1,0)],

    # Bottom Triangles
    [Vector3(1,0,1), Vector3(0,0,1), Vector3(0,0,0)],
    [Vector3(1,0,1), Vector3(0,0,0), Vector3(1,0,0)],
]

# Projection Matrix
fNear = 0.1
fFar = 1000
fFOV = 90
fAspectRatio = (HEIGHT / WIDTH)
fFOVRad = 1 / math.tan(fFOV * 0.5 / 180 * math.pi) # converted to radians

projectionMatrix = [[0,0,0,0] for _ in range(4)]

projectionMatrix[0][0] = fAspectRatio * fFOVRad
projectionMatrix[1][1] = fFOVRad
projectionMatrix[2][2] = fFar / (fFar - fNear)
projectionMatrix[3][2] = (-fFar * fNear) / (fFar - fNear)
projectionMatrix[2][3] = 1 # used to get z back out during matrix multiplication


def distance_between(point1: Vector3, point2: Vector3) -> Vector3:
    return Vector3(point1.x - point2.x, point1.y - point2.y, point1.z - point2.z)

def draw_triangle(x1,y1,x2,y2,x3,y3, colour = (255,255,255)):
    pygame.draw.line(screen, colour, (x1,y1),(x2,y2), 3)
    pygame.draw.line(screen, colour, (x2,y2),(x3,y3), 3)
    pygame.draw.line(screen, colour, (x3,y3),(x1,y1), 3)

camera_location = Vector3(0,0,0)
camera_direction = Vector3(0,0,0)
speed = 0.01

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_location.z += speed
    if keys[pygame.K_s]:
        camera_location.z -= speed
    if keys[pygame.K_a]:
        camera_location.x -= speed
    if keys[pygame.K_d]:
        camera_location.x += speed

    fElapsedTime = (pygame.time.get_ticks() - start_time) / 1000
    fTheta = fElapsedTime

    # Rotation of cube
    zRotationMatrix = [[0,0,0,0] for _ in range(4)]
    xRotationMatrix = [[0,0,0,0] for _ in range(4)]

    # Z rotation
    zRotationMatrix[0][0] = math.cos(fTheta)
    zRotationMatrix[0][1] = -math.sin(fTheta)
    zRotationMatrix[1][0] = math.sin(fTheta)
    zRotationMatrix[1][1] = math.cos(fTheta)
    zRotationMatrix[2][2] = 1
    zRotationMatrix[3][3] = 1

    # X rotation
    xRotationMatrix[0][0] = 1
    xRotationMatrix[1][1] = math.cos(fTheta * 0.5)
    xRotationMatrix[1][2] = -math.sin(fTheta * 0.5)
    xRotationMatrix[2][1] = math.sin(fTheta * 0.5)
    xRotationMatrix[2][2] = math.cos(fTheta * 0.5)
    xRotationMatrix[3][3] = 1

    screen.fill((0, 0, 0))  # fill screen with black

    # Start of drawing stuff

    # Drawing Triangles
    for triangle in cubeTriangles:
        offset = 3 #Temporary offset so that cube isn't rendered inside of the "camera"

        p0 = Vector3(triangle[0].x, triangle[0].y, triangle[0].z)
        p1 = Vector3(triangle[1].x, triangle[1].y, triangle[1].z)
        p2 = Vector3(triangle[2].x, triangle[2].y, triangle[2].z)

        # Applying Z Rotation
        p0 = p0.do_vector_matrix_multiplication(zRotationMatrix)
        p1 = p1.do_vector_matrix_multiplication(zRotationMatrix)
        p2 = p2.do_vector_matrix_multiplication(zRotationMatrix)

        # Applying X Rotation
        p0 = p0.do_vector_matrix_multiplication(xRotationMatrix)
        p1 = p1.do_vector_matrix_multiplication(xRotationMatrix)
        p2 = p2.do_vector_matrix_multiplication(xRotationMatrix)
        
        # Applying offset and projecting to screen
        p0.x += -camera_location.x
        p1.x += -camera_location.x
        p2.x += -camera_location.x

        p0.z += offset - camera_location.z
        p1.z += offset - camera_location.z
        p2.z += offset - camera_location.z

        # Normal calculations
        line1 = Vector3()
        line1.x = p1.x - p0.x
        line1.y = p1.y - p0.y
        line1.z = p1.z - p0.z

        line2 = Vector3()
        line2.x = p2.x - p0.x
        line2.y = p2.y - p0.y
        line2.z = p2.z - p0.z

        normal = line1.get_unit_normal_vector(line2)
        camera_to_triangle = distance_between(p0, camera_location)
        dot_product_result =camera_to_triangle.do_dot_product(normal)

        if (dot_product_result < 0):
            light_direction = Vector3(0,0,-1)
            unit_light_direction = light_direction.get_unit_vector()

            light_dot_product = normal.do_dot_product(light_direction)

            projectedTriangle = [p0.do_vector_matrix_multiplication(projectionMatrix),
                        p1.do_vector_matrix_multiplication(projectionMatrix),
                        p2.do_vector_matrix_multiplication(projectionMatrix)]

            # Scaling all values to screen size
            for p in projectedTriangle:
                p.x = int((p.x+1)*0.5*WIDTH)
                p.y = int((1-(p.y+1)*0.5)*HEIGHT)

            draw_triangle(projectedTriangle[0].x, projectedTriangle[0].y,
                projectedTriangle[1].x, projectedTriangle[1].y,
                projectedTriangle[2].x, projectedTriangle[2].y)

    # End of drawing stuff

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()