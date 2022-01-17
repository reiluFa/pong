import random

import pyglet
from pyglet import gl
from pyglet.window import key

WIDTH = 1200
HEIGHT = 800

BALL_SIZE = 20
BAD_THICKNESS = 10
BAD_WIDTH = 100
SPEED = 200
BAD_SPEED = SPEED * 1.5

MID_LINE_WIDTH = 20
FONT_SIZE = 42
FONT_PADDING = 30

bats_pozicions = [HEIGHT / 2, HEIGHT / 2]
ball_pozition = [0, 0]
ball_speed = [0, 0]
pressed_keyboards = set()
score = [0, 0]

def draw_rectangle(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    gl.glVertex2f(int(x1), int(y1))
    gl.glVertex2f(int(x1), int(y2))
    gl.glVertex2f(int(x2), int(y2))
    gl.glVertex2f(int(x2), int(y1))
    gl.glEnd()


def draw_game():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(1, 1, 1)

    draw_rectangle(
        ball_pozition[0] - BALL_SIZE / 2,
        ball_pozition[1] - BALL_SIZE / 2,
        ball_pozition[0] + BALL_SIZE / 2,
        ball_pozition[1] + BALL_SIZE / 2
    )

    draw_rectangle(
        - BAD_THICKNESS,
        bats_pozicions[0] - BAD_WIDTH / 2,
        BAD_THICKNESS,
        bats_pozicions[0] + BAD_WIDTH / 2
    )
    draw_rectangle(
        WIDTH - BAD_THICKNESS,
        bats_pozicions[1] - BAD_WIDTH / 2,
        WIDTH + BAD_THICKNESS,
        bats_pozicions[1] + BAD_WIDTH / 2
    )

    for y in range(MID_LINE_WIDTH // 2, HEIGHT, MID_LINE_WIDTH * 2):
        draw_rectangle(
            WIDTH // 2 - 1,
            y,
            WIDTH // 2 + 1,
            y + MID_LINE_WIDTH
        )

    draw_text(
        text=str(score[0]),
        x=60, y=HEIGHT - 60, pozice_x='left'
    )
    draw_text(
        text=str(score[1]),
        x=WIDTH - 60, y=HEIGHT - 60, pozice_x='right'
    )

def draw_text(text, x, y, pozice_x):
    vykresli = pyglet.text.Label(
        text,
        font_size=FONT_SIZE,
        x=x, y=y, anchor_x=pozice_x
    )
    vykresli.draw()


def key_press(symbol, modifikatory):
    if symbol == key.W:
        pressed_keyboards.add(('nahoru', 0))
    if symbol == key.S:
        pressed_keyboards.add(('dolu', 0))
    if symbol == key.UP:
        pressed_keyboards.add(('nahoru', 1))
    if symbol == key.DOWN:
        pressed_keyboards.add(('dolu', 1))


def key_release(symbol, modifikatory):
    if symbol == key.W:
        pressed_keyboards.discard(('nahoru', 0))
    if symbol == key.S:
        pressed_keyboards.discard(('dolu', 0))
    if symbol == key.UP:
        pressed_keyboards.discard(('nahoru', 1))
    if symbol == key.DOWN:
        pressed_keyboards.discard(('dolu', 1))


def obnov_stav(dt):
    for cislo_palky in (0, 1):
        if ('nahoru', cislo_palky) in pressed_keyboards:
            bats_pozicions[cislo_palky] += BAD_SPEED * dt
        if ('dolu', cislo_palky) in pressed_keyboards:
            bats_pozicions[cislo_palky] -= BAD_SPEED * dt

        if bats_pozicions[cislo_palky] < BAD_WIDTH / 2:
            bats_pozicions[cislo_palky] = BAD_WIDTH / 2
        if bats_pozicions[cislo_palky] > HEIGHT - BAD_WIDTH / 2:
            bats_pozicions[cislo_palky] = HEIGHT - BAD_WIDTH / 2

    ball_pozition[0] += ball_speed[0] * dt
    ball_pozition[1] += ball_speed[1] * dt

    if ball_pozition[1] < BALL_SIZE // 2:
        ball_speed[1] = abs(ball_speed[1])
    if ball_pozition[1] > HEIGHT - BALL_SIZE // 2:
        ball_speed[1] = -abs(ball_speed[1])

    palka_min = ball_pozition[1] - BALL_SIZE / 2 - BAD_WIDTH / 2
    palka_max = ball_pozition[1] + BALL_SIZE / 2 + BAD_WIDTH / 2

    if ball_pozition[0] < BAD_THICKNESS:
        if palka_min < bats_pozicions[0] < palka_max:
            ball_speed[0] = abs(ball_speed[0])
        else:
            score[1] += 1
            reset()

    if ball_pozition[0] > WIDTH - BAD_THICKNESS:
        if palka_min < bats_pozicions[1] < palka_max:
            ball_speed[0] = -ball_speed[0]
        else:
            score[0] += 1
            reset()


def reset():
    ball_pozition[0] = WIDTH / 2 - 10
    ball_pozition[1] = HEIGHT / 2 - 10

    if random.randrange(2) == 1:
        ball_speed[0] = SPEED
    else:
        ball_speed[0] = -SPEED

    if random.randrange(2) == 1:
        ball_speed[1] = SPEED
    else:
        ball_speed[1] = -SPEED
reset()

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
window.push_handlers(
    on_draw=draw_game,
    on_key_press=key_press,
    on_key_release=key_release, )
pyglet.clock.schedule(obnov_stav)
pyglet.app.run()
