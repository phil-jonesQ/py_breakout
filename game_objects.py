import pygame


class Ball:
    def __init__(self, x, y, radius, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.rect = pygame.Rect(x - radius / 2, y - radius / 2, radius, radius)

    def move(self, direction_x, direction_y):
        self.x += direction_x
        self.y += direction_y

    def draw(self):
        pygame.draw.circle(self.screen, (0, 0, 255), [self.x, self.y], self.radius)
        # Tweak size of Rect to how accurate the collision detection is needed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2.5, self.radius * 2.5)
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

        if self.x + (self.length + 50) > max_width:
            self.x = max_width - (self.length + 20)
            return True
        if self.x < 0:
            self.x = 0
            return True
        return False


class Brick:
    def __init__(self, x, y, radius, screen, colour, length):
        self.x = x
        self.y = y
        self.length = length
        self.radius = radius
        self.screen = screen
        self.colour = colour
        self.rect = pygame.Rect(x, y, radius + length, radius)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.radius + self.length, self.radius)
        pygame.draw.rect(self.screen, self.colour, self.rect, 0)

    def collides_with_ball(self, ball):
        collides = self.rect.colliderect(ball.rect)
        if collides != 0:
            return True
        else:
            return False



