import pygame


class Ball:
    def __init__(self, x, y, radius, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.rect = pygame.Rect(x - radius / 2, y - radius / 2, radius * 1.5, radius * 1.5)

    def move(self, direction_x, direction_y):
        self.x += direction_x
        self.y += direction_y

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), [self.x, self.y], self.radius)
        self.rect = pygame.Rect(self.x - self.radius / 2, self.y - self.radius / 2, self.radius * 1.5, self.radius * 1.5)
        #pygame.draw.rect(self.screen, ((255, 0 ,0)), self.rect, 0)

    def collides_with_bat(self, bat):
        return self.rect.colliderect(bat.rect)


class Bat:
    def __init__(self, x, y, radius, screen, colour, length):
        self.x = x
        self.y = y
        self.length = length
        self.radius = radius
        self.screen = screen
        self.colour = colour
        self.rect = pygame.Rect(x, y, radius + length, radius)

    def move(self, direction):
        self.x += direction

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.radius + self.length, self.radius)
        pygame.draw.rect(self.screen, self.colour, self.rect, 0)

    def clamp(self, max_width):
        if self.x > max_width:
            self.x = max_width
        if self.x < 0:
            self.x = 0



