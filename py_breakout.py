""" Version 1.00 - breakout style.. Grid Based Game

Phil Jones - Jan 2021

Version 1.01 - Draws Grid And Can Exist
Version 1.02 -

"""


import pygame
import sys
import os
import random
from game_objects import Ball, Bat
from game_utils import collision
from random import randint

# Initialise Constants
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
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
    mix = random.uniform(0.1, 2)
    return mix


def move_ball():
    global start, bottom_edge, top_edge, left_edge, right_edge, mixer, up, down, right, left
    # If start is true ball falls
    if start:
        ball.move(0, ball_speed)
        mixer = 1
    # If the ball is near an edge generate some random velocity
    if ball.x < 1 or ball.x > WINDOW_WIDTH - ball_size:
        mixer = gen_mixer()
    elif ball.y < HUD_AREA or ball.y > WINDOW_HEIGHT - bat_size:
        mixer = gen_mixer()
    #print(mixer)
    # Move ball depending where it is
    if down and top_edge:
        if right_edge:
            #print("From the top Sending ball down and left")
            ball.move(-ball_speed + mixer, ball_speed + mixer)
        else:
            #print("From the top Sending ball down and right")
            ball.move(ball_speed + mixer, ball_speed + mixer)

    if up and bottom_edge:
        # Need to add logic to send other direction depending on part hit on bat
        #right_edge = True
        if right_edge:
            #print("From the bottom sending ball left and up")
            ball.move(-ball_speed + mixer, -ball_speed + mixer)
        if left_edge:
            #print("From the bottom sending ball right and up")
            ball.move(ball_speed + mixer, -ball_speed + mixer)

    if right and left_edge:
        if bottom_edge:
            #print("From the left sending ball right and up")
            ball.move(ball_speed + mixer, -ball_speed + mixer)
        if top_edge:
            #print("From the left sending ball right and down")
            ball.move(ball_speed + mixer, ball_speed + mixer)
    if left and right_edge:
        if bottom_edge:
            #print("From the right sending ball left and up")
            ball.move(-ball_speed + mixer, -ball_speed + mixer)
        if top_edge:
            #print("From the right sending ball left and down")
            ball.move(-ball_speed + mixer, ball_speed + mixer)

    # Constrain ball and update flags
    if ball.y > (WINDOW_HEIGHT - bat_size):
        if start:
            start = False
            # Depends which way from start
            right_edge = True
        up = True
        down = False
        right = False
        left = False
        # Edge States
        bottom_edge = True
        top_edge = False

    if ball.x < 0:
        right = True
        left = False
        up = False
        down = False
        # Edge States
        left_edge = True
        right_edge = False

    if ball.y < HUD_AREA:
        down = True
        up = False
        left = False
        right = False
        # Edge States
        top_edge = True
        bottom_edge = False

    if ball.x > WINDOW_WIDTH - ball_size:
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
    global screen, clock, start, ball_pos_x, ball_pos_y, bat_pos_x, bat_pos_y, ball, bat
    global lives, score, ball_velocity, game_running, bat_length, bat_size, ball_size, bat_speed, ball_speed
    global bottom_edge, top_edge, left_edge, right_edge, up, down, left, right
    if not soft:
        lives = 3
        score = 0
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
    bat_speed = 25
    ball_speed = 7
    ball_pos_x = WINDOW_WIDTH / 2
    ball_pos_y = HUD_AREA
    bat_pos_x = (WINDOW_WIDTH - bat_length * 1.5) / 2
    bat_pos_y = WINDOW_HEIGHT - bat_size
    ball = Ball(ball_pos_x, ball_pos_y, ball_size, screen)
    bat = Bat(bat_pos_x, bat_pos_y, bat_size, screen, RED, bat_length)


main()
