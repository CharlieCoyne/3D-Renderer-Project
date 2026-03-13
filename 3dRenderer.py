# pygame is used to obtain inputs from the user and also display the rendering in a window 
import pygame
import sys
import math

pygame.init()

# Pygame Settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Renderer")
start_time = pygame.time.get_ticks()

# Temporary Cube
cubeTriangles = [
                # South Triangles
                [0,0,0,    0,1,0,   1,1,0],
                [0,0,0,    1,1,0,   1,0,0],
                
                # East Triangles
                [1,0,0,    1,1,0,    1,1,1],
                [1,0,0,    1,1,1,    1,0,0],
                
                # North Triangles
                [1,0,1,    1,1,1,    0,1,1],
                [1,0,1,    0,1,1,    0,0,1],
                
                # West Triangles
                [0,0,1,    0,1,1,    0,1,0],
                [0,0,1,    0,1,0,    0,0,0],
                
                # Top Triangles
                [0,1,0,    0,1,1,    1,1,1],
                [0,1,0,    1,1,1,    1,1,0],

                # Bottom Triangles
                [1,0,1,    0,0,1,    0,0,0],
                [1,0,1,    0,0,0,    1,0,0],]

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


def vector_matrix_multiplication(vector, m):
    outputVector = [0,0,0]
    outputVector[0] = vector[0] * m[0][0] + vector[1] * m[1][0] + vector[2] * m[2][0] + m[3][0]
    outputVector[1] = vector[0] * m[0][1] + vector[1] * m[1][1] + vector[2] * m[2][1] + m[3][1]
    outputVector[2] = vector[0] * m[0][2] + vector[1] * m[1][2] + vector[2] * m[2][2] + m[3][2]
    w               = vector[0] * m[0][3] + vector[1] * m[1][3] + vector[2] * m[2][3] + m[3][3]

    if w != 0:
        outputVector[0] = outputVector[0] / w
        outputVector[1] = outputVector[1] / w
        outputVector[2] = outputVector[2] / w 

    return outputVector


def draw_triangle(x1,y1,x2,y2,x3,y3, colour = (255,255,255)):
    pygame.draw.line(screen, colour, (x1,y1),(x2,y2))
    pygame.draw.line(screen, colour, (x2,y2),(x3,y3))
    pygame.draw.line(screen, colour, (x3,y3),(x1,y1))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # fill screen with black
    
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

    # Start of drawing stuff

    # Drawing Triangles
    for triangle in cubeTriangles:
        offset = 3 #Temporary offset so that cube isn't rendered inside of the "camera"

        p1 = [coord for coord in triangle[0:3]]
        p2 = [coord for coord in triangle[3:6]]
        p3 = [coord for coord in triangle[6:9]]

        # Applying Z Rotation
        p1 = vector_matrix_multiplication(p1, zRotationMatrix)
        p2 = vector_matrix_multiplication(p2, zRotationMatrix)
        p3 = vector_matrix_multiplication(p3, zRotationMatrix)

        # Applying X Rotation
        p1 = vector_matrix_multiplication(p1, xRotationMatrix)
        p2 = vector_matrix_multiplication(p2, xRotationMatrix)
        p3 = vector_matrix_multiplication(p3, xRotationMatrix)
        
        # Applying offset and projecting to screen
        p1[2] += offset
        p2[2] += offset
        p3[2] += offset
        
        projectedTriangle = [vector_matrix_multiplication(p1, projectionMatrix),
                     vector_matrix_multiplication(p2, projectionMatrix),
                     vector_matrix_multiplication(p3, projectionMatrix)]

        # Scaling all values to screen size
        for p in projectedTriangle:
            p[0] = int((p[0]+1)*0.5*WIDTH)
            p[1] = int((1-(p[1]+1)*0.5)*HEIGHT)

        draw_triangle(projectedTriangle[0][0], projectedTriangle[0][1],
              projectedTriangle[1][0], projectedTriangle[1][1],
              projectedTriangle[2][0], projectedTriangle[2][1])

    # End of drawing stuff

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()