from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Camera-related variables
camera_angle = 90
camera_radius = 300
camera_height = 500

camera_rotation_speed = 2
camera_height_speed = 10


camera_pos = (0, 300, 500)
fovY = 120  # Field of view
aspectRatio = WINDOW_WIDTH/WINDOW_HEIGHT
zNear = 0.1
zFar = 1500
GRID_LENGTH = 600  # Length of grid lines

# game status bar
life = 5
score = 0
missed_bullets = 0

# checker board floor and boundary info
tile_size = 60
side = 13  # num of tiles per side
tile_colour1 = (1, 1, 1)  # white
tile_colour2 = (0.7, 0.5, 0.95)  # lavender
boundary_height = 50
right_boundary_color = (0, 1, 0)
left_boundary_color = (0, 0, 1)
top_boundary_color = (0, 1, 1)
bottom_boundary_color = (1, 1, 1)


def draw_floor_and_boundary():
    global tile_size, side, tile_colour1, tile_colour2
    global boundary_height
    # floor
    start = -(side*tile_size)/2
    for row in range(side):
        for col in range(side):
            x1 = start + col * tile_size
            y1 = start + row * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size

            if (row+col) % 2 == 0:
                glColor3f(*tile_colour1)
            else:
                glColor3f(*tile_colour2)
            glBegin(GL_QUADS)

            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)

            glEnd()
    # boundary
    floor_side_len = side * tile_size
    floor_half_side_len = floor_side_len/2

    # Right boundary
    glColor3f(*right_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(-floor_half_side_len,  floor_half_side_len, 0)
    glVertex3f(-floor_half_side_len, -floor_half_side_len, 0)
    glVertex3f(-floor_half_side_len, -floor_half_side_len, boundary_height)
    glVertex3f(-floor_half_side_len,  floor_half_side_len, boundary_height)
    glEnd()

    # Left boundary
    glColor3f(*left_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(floor_half_side_len, -floor_half_side_len, 0)
    glVertex3f(floor_half_side_len,  floor_half_side_len, 0)
    glVertex3f(floor_half_side_len,  floor_half_side_len, boundary_height)
    glVertex3f(floor_half_side_len, -floor_half_side_len, boundary_height)
    glEnd()

    # Top boundary
    glColor3f(*top_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(floor_half_side_len, -floor_half_side_len, 0)
    glVertex3f(-floor_half_side_len, -floor_half_side_len, 0)
    glVertex3f(-floor_half_side_len, -floor_half_side_len, boundary_height)
    glVertex3f(floor_half_side_len, -floor_half_side_len, boundary_height)
    glEnd()

    # Bottom boundary
    glColor3f(*bottom_boundary_color)
    glBegin(GL_QUADS)
    glVertex3f(-floor_half_side_len, floor_half_side_len, 0)
    glVertex3f(floor_half_side_len, floor_half_side_len, 0)
    glVertex3f(floor_half_side_len, floor_half_side_len, boundary_height)
    glVertex3f(-floor_half_side_len, floor_half_side_len, boundary_height)
    glEnd()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():

    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)
    glutSolidCube(60)  # Take cube size as the parameter
    glTranslatef(0, 0, 100)
    glColor3f(0, 1, 0)
    glutSolidCube(60)

    glColor3f(1, 1, 0)
    glScalef(2, 2, 2)
    # parameters are: quadric, base radius, top radius, height, slices, stacks
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)
    glTranslatef(100, 0, 100)
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100)
    # parameters are: quadric, radius, slices, stacks
    gluSphere(gluNewQuadric(), 80, 10, 10)

    glPopMatrix()  # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, camera_angle, camera_height

    if key == GLUT_KEY_UP:
        camera_height += camera_height_speed

    if key == GLUT_KEY_DOWN:
        camera_height -= camera_height_speed

    if key == GLUT_KEY_LEFT:
        camera_angle -= camera_rotation_speed

    if key == GLUT_KEY_RIGHT:
        camera_angle += camera_rotation_speed

    angle = math.radians(camera_angle)

    camera_x = camera_radius * math.cos(angle)
    camera_y = camera_radius * math.sin(angle)

    camera_pos = (camera_x, camera_y, camera_height)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

    # # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    # (fovY, aspect ratio, zNear, zFar))
    gluPerspective(fovY, aspectRatio, zNear, zFar)
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw checkerboard floor and boundary
    draw_floor_and_boundary()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Player Life Remaining: {life}")
    draw_text(10, 740, f"Game Score : {score}")
    draw_text(10, 710, f"Player Bullet Missed: {missed_bullets}")

    draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    # Double buffering, RGB color, depth test
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    # Register the idle function to move the bullet automatically
    glutIdleFunc(idle)

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
