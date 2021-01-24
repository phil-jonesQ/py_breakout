""" Version 1.00 - breakout style..

Phil Jones - Jan 2021

Version 1.01 - Abandon grid method and use game objects to take advantage of pygame rectangle collision detection
Version 1.02 - Ball bounces around correctly, need to add initial direction randomise next

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
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
HUD_AREA = 60

lives = 3
score = 0
start = True
game_running = False
bottom_edge = False
top_edge = False
left_edge = False
right_edge = False
down = True
up = False
right = False
left = False

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


pygame.font.init()  # you have to call this at the start,
thefont = pygame.font.SysFont('Courier New', 20)


def game_stats_display():
    score_string = "SCORE " + str(score)
    lives_string = "LIVES " + str(lives)
    message_string = "SPACE TO RESTART.."

    textsurface1 = thefont.render(score_string, False, (0, 255, 0))
    textsurface2 = thefont.render(lives_string, False, (255, 255, 0))
    textsurface3 = thefont.render(message_string, False, (255, 0, 0))

    screen.blit(textsurface1, (15, 15))
    screen.blit(textsurface2, (205, 15))
    screen.blit(textsurface3, (WINDOW_WIDTH - 400, 15))
    pygame.display.update()
    pygame.display.flip()


def gen_mixer():
    mix = random.uniform(0.1, 4)
    return mix


def move_ball():
    global start, bottom_edge, top_edge, left_edge, right_edge, mixer, up, down, right, left
    # If start is true ball falls
    if start:
        ball.move(0, ball_speed)
        mixer = gen_mixer()
    # If the ball is near an edge generate some random velocity
    if ball.x < 1 or ball.x > WINDOW_WIDTH - ball_size:
        mixer = gen_mixer()
    elif ball.y < HUD_AREA or ball.y > WINDOW_HEIGHT - bat_size:
        mixer = gen_mixer()
    #print(mixer)
    # Move ball depending where it is
    hit_brick = collide_ball_to_brick(ball)

    if down and top_edge:
        if right_edge:
            #print("From the top Sending ball down and left")
            ball.move(-ball_speed - mixer, ball_speed + mixer)
        else:
            #print("From the top Sending ball down and right")
            ball.move(ball_speed + mixer, ball_speed + mixer)

    if up and bottom_edge:
        # Need to add logic to send other direction depending on part hit on bat
        if right_edge:
            #print("From the bottom sending ball left and up")
            ball.move(-ball_speed - mixer, -ball_speed - mixer)
        if left_edge:
            #print("From the bottom sending ball right and up")
            ball.move(ball_speed + mixer, -ball_speed - mixer)

    if right and left_edge:
        if bottom_edge:
            #print("From the left sending ball right and up")
            ball.move(ball_speed + mixer, -ball_speed - mixer)
        if top_edge:
            #print("From the left sending ball right and down")
            ball.move(ball_speed + mixer, ball_speed + mixer)
    if left and right_edge:
        if bottom_edge:
            #print("From the right sending ball left and up")
            ball.move(-ball_speed + mixer, -ball_speed - mixer)
        if top_edge:
            #print("From the right sending ball left and down")
            ball.move(-ball_speed + mixer, ball_speed + mixer)

    # Constrain ball and update flags
    if ball.y > (WINDOW_HEIGHT - bat_size) or hit_brick:
        if start:
            start = False
            # Mix deflection off from start
            if mixer > 2:
                right_edge = True
            else:
                left_edge = True
        up = True
        down = False
        right = False
        left = False
        # Edge States
        bottom_edge = True
        top_edge = False

    if ball.x < 0 or hit_brick:
        right = True
        left = False
        up = False
        down = False
        # Edge States
        left_edge = True
        right_edge = False

    if ball.y < HUD_AREA or hit_brick:
        down = True
        up = False
        left = False
        right = False
        # Edge States
        top_edge = True
        bottom_edge = False

    if ball.x > WINDOW_WIDTH - ball_size or hit_brick:
        left = True
        down = False
        up = False
        right = False
        # Edge States
        right_edge = True
        left_edge = False


def check_lose_life():
    global lives
    if not ball.collides_with_bat(bat) and ball.y > WINDOW_HEIGHT - bat_size:
        print("Dead!!")
        lives -= 1
        reset(True)


def generate_wall():
    global brick, brick_size, brick_length, bricks, wall_rows
    cols = WINDOW_WIDTH // brick_length
    pad = 30
    print ("There are cols", cols)
    for row in range(wall_rows):
        for col in range(cols):
            bricks.append(
                    Brick((col * brick_length), (row * brick_size) + HUD_AREA, 15, screen, YELLOW, brick_length - pad))

    #brick = Brick(0, HUD_AREA, brick_size, screen, YELLOW, brick_length)


def draw_wall():
    for obj in range(len(bricks)):
        bricks[obj].draw()
        #print(bricks[obj].x, bricks[obj].y, bricks[obj].colour)


def update_wall():
    for obj in range(len(bricks)):
        bricks[obj].draw()
        #print(bricks[obj].x, bricks[obj].y, bricks[obj].colour)


def collide_ball_to_brick(ball):
    brick_amount = len(bricks)
    count = -2
    print("The amount of bricks is", str(brick_amount))
    for obj in range(brick_amount):
        count += 1
        if bricks[count].collides_with_ball(ball):
            print("Hit Brick Number", count)
            if bricks[count]:
                bricks.pop(count)
            if count == -1:
                return 0, 0, 0, True
            return count, bricks[count].x, bricks[count].y, True



def main():
    pygame.init()
    clock = pygame.time.Clock()
    reset(False)
    pygame.key.set_repeat(1, 50)
    while True:
        clock.tick(60)
        screen.fill(BLACK)
        ball.draw()
        bat.draw()
        # Testing
        update_wall()
        bat.clamp(WINDOW_WIDTH - bat_length)
        move_ball()
        check_lose_life()
        game_stats_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                reset(False)
            if keys[pygame.K_RIGHT]:
                bat.move(bat_speed)
            if keys[pygame.K_LEFT]:
                bat.move(- bat_speed)
        if start or game_running:
            pass

        # Update Display
        pygame.display.update()
        pygame.display.flip()


def reset(soft):
    global screen, clock, start, ball_pos_x, ball_pos_y, bat_pos_x, bat_pos_y, ball, bat, brick, bricks
    global lives, score, game_running, bat_length, bat_size, ball_size, bat_speed, ball_speed, brick_size, brick_length
    global bottom_edge, top_edge, left_edge, right_edge, up, down, left, right, wall_rows
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
    bat_size = WINDOW_HEIGHT / 20
    ball_size = 15
    brick_size = 20
    brick_length = 60
    bat_speed = 40
    ball_speed = 7
    wall_rows = 4
    ball_pos_x = WINDOW_WIDTH / 2
    ball_pos_y = HUD_AREA * wall_rows
    bat_pos_x = (WINDOW_WIDTH - bat_length * 1.5) / 2
    bat_pos_y = WINDOW_HEIGHT - bat_size
    ball = Ball(ball_pos_x, ball_pos_y, ball_size, screen)
    bat = Bat(bat_pos_x, bat_pos_y, bat_size, screen, RED, bat_length)
    if not soft:
        lives = 3
        score = 0
        bricks = []
        generate_wall()
        draw_wall()




main()
