import pygame


class Ball:
    def __init__(self, x, y, radius, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen

    def move(self, direction_x, direction_y):
        self.x += direction_x
        self.y += direction_y

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), [self.x, self.y], self.radius)


class Bat:
    def __init__(self, x, y, radius, screen, colour, length):
        self.x = x
        self.y = y
        self.length = length
        self.radius = radius
        self.screen = screen
        self.colour = colour

    def move(self, direction):
        self.x += direction

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.radius + self.length, self.radius)
        pygame.draw.rect(self.screen, self.colour, rect, 0)

    def clamp(self, max_width):
        if self.x > max_width:
            self.x = max_width
        if self.x < 0:
            self.x = 0



