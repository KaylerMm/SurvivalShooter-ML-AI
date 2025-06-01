import pygame
import math

class EnemyBullet:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 8, 8)
        self.speed = 5

        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        self.vel_x = self.speed * dx / distance
        self.vel_y = self.speed * dy / distance

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 0), self.rect)
