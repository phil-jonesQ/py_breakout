""" Version 1.00 - breakout style.. Grid Based Game

Phil Jones - Jan 2021

Version 1.01 - Draws Grid And Can Exist
Version 1.02 -

"""


import pygame
import sys
import os
import random
from random import randint


# Initialise Constants

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
SCALE = 30
ROWS = WINDOW_HEIGHT // SCALE
COLS = WINDOW_WIDTH // SCALE
cell_sz = WINDOW_HEIGHT // ROWS
BAT_LENGTH = 4

print(COLS, ROWS)

pygame.font.init()  # you have to call this at the start,
thefont = pygame.font.SysFont('Courier New', 20)

images = {
                    'ace of clubs': 'AC.png',
                    'ace of diamonds': 'AD.png',

}

# Load Image set
# Store in a dictionary so we can map the image to name
card_images = {}
path = "assets/"
for name, file_name in images.items():
    image = pygame.transform.scale(pygame.image.load(path + os.sep + file_name), (70, 90))
    card_images[name] = image

# Track the game state by storing each cell's card and if it's been revealed (True|False)
cell_tracker = {}
compare_tracker = {}
matched_cells_tracker = []


def game_stats_display():
    score_string = "SCORE " + str(score)
    lives_string = "LIVES " + str(lives)
    message_string = "SPACE TO RESTART.."

    textsurface1 = thefont.render(score_string, False, (0, 255, 0))
    textsurface2 = thefont.render(lives_string, False, (255, 255, 0))
    textsurface3 = thefont.render(message_string, False, (255, 0, 0))

    SCREEN.blit(textsurface1, (15, 15))
    SCREEN.blit(textsurface2, (205, 15))
    SCREEN.blit(textsurface3, (WINDOW_WIDTH - 400, 15))
    pygame.display.update()
    pygame.display.flip()


def draw_grid():
    SCREEN.fill(BLACK)
    for ROW in range(2, ROWS):
        for COL in range(COLS):
            rect = pygame.Rect(COL * cell_sz, ROW * cell_sz,
                               cell_sz, cell_sz)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def draw_bat(col, row):
    rect = pygame.Rect(col * cell_sz, row * cell_sz,
                       cell_sz + BAT_LENGTH * cell_sz, cell_sz)
    pygame.draw.rect(SCREEN, RED, rect, 0)


def update_grid():
    #SCREEN.fill(BLACK)
    counter = 0
    for ROW in range(ROWS):
        for COL in range(COLS):
            counter += 1
            #print(counter, tuple((ROW, COL)))
    pygame.display.update()
    pygame.display.flip()


def main():
    global SCREEN, clock
    global enabled, lives, score, bat_pos
    lives = 3
    score = 0
    bat_pos_row = ROWS - 1
    bat_pos_col = (COLS // 2) - (BAT_LENGTH / 2)
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    reset()
    draw_grid()
    pygame.key.set_repeat(1, 50)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                bat_pos_col += 2
                if (bat_pos_col + (BAT_LENGTH // 2)) > ((COLS - 1) - (BAT_LENGTH // 2)):
                    bat_pos_col = ((COLS - 1) - BAT_LENGTH)
            if keys[pygame.K_LEFT]:
                bat_pos_col -= 2
                print(bat_pos_col, "edge", COLS)
                if (bat_pos_col - (BAT_LENGTH // 2)) < - 1:
                    bat_pos_col = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                enabled = True
                # Set the x, y positions of the mouse click
                x, y = event.pos
                # Translate x, y pos to grid coord
                clicked_col = (event.pos[0] // cell_sz) + 1
                clicked_row = (event.pos[1] // cell_sz) + 1
                # Translate col_row coord to a cell number
        game_stats_display()
        update_grid()
        draw_grid()
        draw_bat(bat_pos_col, bat_pos_row)


def reset():
    lives = 3
    score = 0

main()
