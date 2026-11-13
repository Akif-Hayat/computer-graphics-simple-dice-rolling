import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluNewQuadric, gluPerspective, gluSphere, gluDeleteQuadric


WIDTH = 480
HEIGHT = 360
HALF = 1.12
DOT = 0.105


def draw_face(vertices, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    for vertex in vertices:
        glVertex3f(*vertex)
    glEnd()


def draw_pips(positions, quadric):
    for position in positions:
        glPushMatrix()
        glTranslatef(*position)
        glColor3f(0.08, 0.14, 0.14)
        gluSphere(quadric, DOT, 10, 8)
        glPopMatrix()


def draw_die(quadric):
    cream = (0.94, 0.92, 0.84)
    h = HALF
    d = 0.43

    draw_face(((-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)), cream)
    draw_pips(((-d, -d, h + 0.02), (d, d, h + 0.02)), quadric)

    draw_face(((h, -h, -h), (-h, -h, -h), (-h, h, -h), (h, h, -h)), cream)
    draw_pips(((-d, -d, -h - 0.02), (-d, d, -h - 0.02), (d, -d, -h - 0.02),
               (d, d, -h - 0.02), (0, 0, -h - 0.02)), quadric)

    draw_face(((h, -h, h), (h, -h, -h), (h, h, -h), (h, h, h)), cream)
    draw_pips(((h + 0.02, -d, -d), (h + 0.02, d, d), (h + 0.02, 0, 0)), quadric)

    draw_face(((-h, -h, -h), (-h, -h, h), (-h, h, h), (-h, h, -h)), cream)
    draw_pips(((-h - 0.02, -d, -d), (-h - 0.02, -d, d),
               (-h - 0.02, d, -d), (-h - 0.02, d, d)), quadric)

    draw_face(((-h, h, h), (h, h, h), (h, h, -h), (-h, h, -h)), cream)
    draw_pips(((0, h + 0.02, 0),), quadric)

    draw_face(((-h, -h, -h), (h, -h, -h), (h, -h, h), (-h, -h, h)), cream)
    draw_pips(((-d, -h - 0.02, -d), (-d, -h - 0.02, 0), (-d, -h - 0.02, d),
               (d, -h - 0.02, -d), (d, -h - 0.02, 0), (d, -h - 0.02, d)), quadric)


def next_angle(current, face_angle):
    while face_angle <= current:
        face_angle += 360
    return face_angle + 360 * random.randint(1, 3)


def start_roll():
    global rolling, roll_time, start_x, start_y, start_z, target_x, target_y, target_z
    if rolling:
        return

    result = random.randint(1, 6)
    face_x, face_y, face_z = 0, 0, 0
    if result == 2:
        face_x = -90
    elif result == 3:
        face_z = 90
    elif result == 4:
        face_z = -90
    elif result == 5:
        face_x = 90
    elif result == 6:
        face_x = 180

    start_x, start_y, start_z = angle_x, angle_y, angle_z
    target_x = next_angle(angle_x, face_x)
    target_y = next_angle(angle_y, face_y)
    target_z = next_angle(angle_z, face_z)
    rolling = True
    roll_time = 0


def update(dt):
    global angle_x, angle_y, angle_z, camera_y, roll_time, rolling
    camera_target = 1.65 if rolling else 4.8
    camera_y += (camera_target - camera_y) * min(1, dt * 4.5)
    if not rolling:
        return

    roll_time = min(roll_time + dt, 2.25)
    progress = roll_time / 2.25
    progress = progress * progress * (3 - 2 * progress)
    angle_x = start_x + (target_x - start_x) * progress
    angle_y = start_y + (target_y - start_y) * progress
    angle_z = start_z + (target_z - start_z) * progress
    if roll_time >= 2.25:
        angle_x, angle_y, angle_z = target_x, target_y, target_z
        rolling = False


def main():
    global angle_x, angle_y, angle_z, camera_y, rolling
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    quadric = gluNewQuadric()
    clock = pygame.time.Clock()

    angle_x = angle_y = angle_z = 0
    camera_y = 4.8
    rolling = False
    running = True

    while running:
        dt = min(clock.tick(120) / 1000, 1 / 30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_roll()

        update(dt)
        glClearColor(0.025, 0.12, 0.125, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, WIDTH, HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(43, WIDTH / HEIGHT, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, camera_y, 5.7, 0, 0, 0, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_x, 1, 0, 0)
        draw_die(quadric)
        pygame.display.flip()

    gluDeleteQuadric(quadric)
    pygame.quit()


if __name__ == "__main__":
    main()
