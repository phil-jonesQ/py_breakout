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
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 900
WINDOW_GAME_DISPLAY = 100
SCALE = 20
ROWS = (WINDOW_HEIGHT - WINDOW_GAME_DISPLAY) // SCALE
COLS = WINDOW_WIDTH // SCALE

print(ROWS, COLS)


cell_sz = WINDOW_HEIGHT // ROWS


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
            rect = pygame.Rect(COL*cell_sz, ROW*cell_sz,
                               cell_sz, cell_sz)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def update_grid():
    #SCREEN.fill(BLACK)
    counter = 0
    for ROW in range(ROWS):
        for COL in range(COLS):
            counter += 1
            print(counter, tuple((ROW, COL)))
    pygame.display.update()
    pygame.display.flip()


def main():
    global SCREEN, CLOCK
    global TURNS
    global enabled
    global attempts
    global lives
    global score
    lives = 3
    score = 0
    TURNS = 2
    attempts = 0
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    reset()
    draw_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset()
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


def reset():
    lives = 3
    score = 0

main()
