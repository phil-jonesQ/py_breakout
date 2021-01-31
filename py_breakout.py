""" Version 1.00 - breakout style..

Phil Jones - Jan 2021

Version 1.01 - Abandon grid method and use game objects to take advantage of pygame rectangle collision detection
Version 1.02 - Ball bounces around correctly, need to add initial direction randomise next
Version 1.03 - Working Game with basic level system
Version 1.04 - Add sound effects and improve bat clamp
"""


import pygame
import sys
import random
from game_objects import Ball, Bat, Brick


# Initialise Constants
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 0, 255)
CYAN = (0, 255, 255)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
HUD_AREA = 60

start = True
game_running = False

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


pygame.font.init()  # you have to call this at the start,
thefont = pygame.font.SysFont('Courier New', 20)

# Load Sound effects
pygame.mixer.init()
brick_break_sound = pygame.mixer.Sound("assets/click.wav")
bat_hit_sound = pygame.mixer.Sound("assets/bat_hit.wav")
lose_life_sound = pygame.mixer.Sound("assets/life_loss.wav")



def game_stats_display(state_string):
    score_string = "SCORE " + str(score)
    level_string = "LEVEL " + str(level)
    if state_string == "GAMEOVER":
        message_string = "GAME-OVER SPACE TO RESTART.."
        lives_string = "LIVES 0"
    else:
        message_string = "SPACE TO RESTART.."
        lives_string = "LIVES " + str(lives)

    textsurface1 = thefont.render(score_string, False, (0, 255, 0))
    textsurface2 = thefont.render(lives_string, False, (255, 255, 0))
    textsurface3 = thefont.render(message_string, False, (255, 0, 0))
    textsurface4 = thefont.render(level_string, False, (255, 0, 255))

    screen.blit(textsurface1, (15, 15))
    screen.blit(textsurface2, (205, 15))
    screen.blit(textsurface4, (305, 15))
    screen.blit(textsurface3, (WINDOW_WIDTH - 400, 15))
    pygame.display.update()
    pygame.display.flip()


def gen_mixer():
    mix = random.uniform(0.1, 4)
    return mix


def deflect_ball(direction):
    """ Method to set flags depending on direction string passed in"""
    global start, bottom_edge, top_edge, left_edge, right_edge, up, down, right, left
    if direction == "up":
        up = True
        down = False
        right = False
        left = False
        # Edge States
        bottom_edge = True
        top_edge = False
    if direction == "right":
        right = True
        left = False
        up = False
        down = False
        # Edge States
        left_edge = True
        right_edge = False
    if direction == "down":
        down = True
        up = False
        left = False
        right = False
        # Edge States
        top_edge = True
        bottom_edge = False
    if direction == "left":
        left = True
        down = False
        up = False
        right = False
        # Edge States
        right_edge = True
        left_edge = False


def move_ball():
    global start, bottom_edge, top_edge, left_edge, right_edge, mixer, up, down, right, left, hit_brick
    # If start is true ball falls
    if start:
        ball.move(0, ball_speed)
        mixer = gen_mixer()
    # If the ball is near an edge generate some random velocity
    if ball.x < 1 or ball.x > WINDOW_WIDTH - ball_size:
        mixer = gen_mixer()
    elif ball.y < HUD_AREA or ball.y > WINDOW_HEIGHT - bat_size:
        mixer = gen_mixer()
    # Set the hit_brick flag if the ball has collided with a brick
    # The collide_ball_brick method also iterates over every brick and removes
    # the one it has collided with
    hit_brick = collide_ball_to_brick(ball)

    # If down flag and coming from the top
    if down and top_edge:
        if right_edge:
            ball.move(-ball_speed - mixer, ball_speed + mixer)
        else:
            ball.move(ball_speed + mixer, ball_speed + mixer)

    # If up flag and coming from the bottom
    if up and bottom_edge:
        if right_edge:
            ball.move(-ball_speed - mixer, -ball_speed - mixer)
        if left_edge:
            ball.move(ball_speed + mixer, -ball_speed - mixer)

    # If right flag and coming from the left edge
    if right and left_edge:
        if bottom_edge:
            ball.move(ball_speed + mixer, -ball_speed - mixer)
        if top_edge:
            ball.move(ball_speed + mixer, ball_speed + mixer)

    # If left flag and coming from the right edge
    if left and right_edge:
        if bottom_edge:
            ball.move(-ball_speed + mixer, -ball_speed - mixer)
        if top_edge:
            ball.move(-ball_speed + mixer, ball_speed + mixer)

    # Constrain ball and update flags for the ball behaviour
    if ball.y > (WINDOW_HEIGHT - bat_size):
        if start:
            start = False
            # Mix deflection off from start
            if mixer > 2:
                right_edge = True
            else:
                left_edge = True
        pygame.mixer.Sound.play(bat_hit_sound)
        deflect_ball("up")

    if ball.x < 0:
        deflect_ball("right")

    if ball.y < HUD_AREA:
        deflect_ball("down")

    if ball.x > WINDOW_WIDTH - ball_size:
        deflect_ball("left")

    # Handle direction change when the ball has hit a brick
    if hit_brick:
        if up:
            deflect_ball("down")
            return
        if down:
            deflect_ball("up")
            return
        if left:
            deflect_ball("right")
            return
        if right:
            deflect_ball("left")
            return


def check_lose_life():
    global lives, game_over
    if not ball.collides_with_bat(bat) and ball.y > WINDOW_HEIGHT - bat_size:
        lives -= 1
        pygame.mixer.Sound.play(lose_life_sound)
        if lives < 0:
            game_over = True
        else:
            reset(True)


def generate_wall():
    global brick, brick_size, brick_length, bricks, wall_rows, level_target_bricks, score
    cols = WINDOW_WIDTH // brick_length
    pad = 30
    level_target_bricks = score
    for row in range(wall_rows):
        for col in range(cols):
            level_target_bricks += 1
            if row % 2 == 0:
                bricks.append(
                    Brick((col * brick_length), (row * brick_size) + HUD_AREA, 10, screen, YELLOW, brick_length - pad))
            else:
                bricks.append(
                    Brick((col * brick_length), (row * brick_size) + HUD_AREA, 10, screen, CYAN, brick_length - pad))


def draw_wall():
    for obj in range(len(bricks)):
        bricks[obj].draw()


def update_wall():
    for obj in range(len(bricks)):
        bricks[obj].draw()


def collide_ball_to_brick(ball):
    global up, down, left, right, score, level_complete, level_target_bricks
    brick_amount = len(bricks)
    count = -2
    for obj in range(brick_amount):
        count += 1
        if bricks[count].collides_with_ball(ball):
            if score == level_target_bricks - 1:
                level_complete = True
            if bricks[count]:
                bricks.pop(count)
                score += 1
                pygame.mixer.Sound.play(brick_break_sound)
            if count == -1:
                return 0, 0, 0, True
            return count, bricks[count].x, bricks[count].y, True


def main():
    pygame.init()
    clock = pygame.time.Clock()
    # Hard reset Game Vars
    reset(False)
    pygame.key.set_repeat(1, 50)
    while True:
        clock.tick(45)
        screen.fill(BLACK)
        ball.draw()
        bat.draw()
        update_wall()
        bat.clamp(WINDOW_WIDTH)
        if not game_over:
            move_ball()
            check_lose_life()
            game_stats_display("RUNNING")
        else:
            game_stats_display("GAMEOVER")
        # Spawn the next level
        if level_complete:
            reset(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                reset(False)
            if keys[pygame.K_RIGHT] and not game_over:
                bat.move(bat_speed)
            if keys[pygame.K_LEFT] and not game_over:
                bat.move(- bat_speed)
        if start or game_running:
            pass

        # Update Display
        pygame.display.update()
        pygame.display.flip()


def reset(soft):
    global screen, clock, start, ball_pos_x, ball_pos_y, bat_pos_x, bat_pos_y, ball, bat, brick, bricks
    global lives, score, game_running, bat_length, bat_size, ball_size, bat_speed, ball_speed, brick_size, brick_length
    global bottom_edge, top_edge, left_edge, right_edge, up, down, left, right, wall_rows, level_complete, level, game_over
    start = True
    top_edge = False
    bottom_edge = False
    left_edge = False
    right_edge = False
    up = False
    down = False
    right = False
    left = False
    bat_length = 125
    bat_size = WINDOW_HEIGHT / 30
    ball_size = 8
    brick_size = 20
    brick_length = 60
    bat_speed = 60
    ball_speed = 7
    ball_pos_x = WINDOW_WIDTH / 2
    ball_pos_y = HUD_AREA * 8
    bat_pos_x = (WINDOW_WIDTH - bat_length * 1.5) / 2
    bat_pos_y = WINDOW_HEIGHT - bat_size
    ball = Ball(ball_pos_x, ball_pos_y, ball_size, screen)
    bat = Bat(bat_pos_x, bat_pos_y, bat_size, screen, RED, bat_length)
    if not soft:
        level_complete = False
        game_over = False
        wall_rows = 4
        lives = 9
        score = 0
        level = 1
        bricks = []
        generate_wall()
        draw_wall()
    if level_complete:
        # Although this repeats a lot of variable allocation
        # It makes it easy to tweak things for power-ups or level-ups
        level += 1
        top_edge = False
        bottom_edge = False
        left_edge = False
        right_edge = False
        up = False
        down = False
        right = False
        left = False
        bat_length = 125
        bat_size = WINDOW_HEIGHT / 30
        ball_size = 8
        brick_size = 20
        brick_length = 60
        bat_speed = 60
        ball_speed += 0.5
        ball_pos_x = WINDOW_WIDTH / 2
        ball_pos_y = HUD_AREA * 8
        bat_pos_x = (WINDOW_WIDTH - bat_length * 1.5) / 2
        bat_pos_y = WINDOW_HEIGHT - bat_size
        ball = Ball(ball_pos_x, ball_pos_y, ball_size, screen)
        bat = Bat(bat_pos_x, bat_pos_y, bat_size, screen, RED, bat_length)
        level_complete = False
        wall_rows += 1
        # Clamp at 10 rows
        if wall_rows > 10:
            wall_rows = 10
        bricks = []
        generate_wall()
        draw_wall()


main()
