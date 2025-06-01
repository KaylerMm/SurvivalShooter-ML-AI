import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vx = 0
        self.vy = 0
        self.speed = 200

    def update(self):
        keys = pygame.key.get_pressed()
        self.vx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        self.vy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed
        self.rect.x += self.vx * 0.016
        self.rect.y += self.vy * 0.016

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.rect)
