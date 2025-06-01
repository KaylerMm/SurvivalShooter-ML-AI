import pygame
import numpy as np
import pandas as pd
from joblib import load
import os
from game.enemy_bullet import EnemyBullet

class Enemy:
    def __init__(self, x, y, model=None):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.model_x = None
        self.model_y = None
        self.predicted_pos = None
        self.bullets = []
        self.last_shot = 0
        self.shoot_delay = 1000  # ms

        # Carrega modelos
        model_path_x = "ai/models/model_x.joblib"
        model_path_y = "ai/models/model_y.joblib"
        if os.path.exists(model_path_x) and os.path.exists(model_path_y):
            self.model_x = load(model_path_x)
            self.model_y = load(model_path_y)
            print("Modelos de IA carregados com sucesso!")

    def update(self, player):
        now = pygame.time.get_ticks()

        if self.model_x and self.model_y:
            features = pd.DataFrame([{
                'x': player.rect.x,
                'y': player.rect.y,
                'vx': player.vx,
                'vy': player.vy,
                'timestamp': now / 1000
            }])

            pred_x = self.model_x.predict(features)[0]
            pred_y = self.model_y.predict(features)[0]
            self.predicted_pos = (int(pred_x), int(pred_y))

            # Tiro com delay
            if now - self.last_shot > self.shoot_delay:
                bullet = EnemyBullet(
                    self.rect.centerx,
                    self.rect.centery,
                    pred_x,
                    pred_y
                )
                self.bullets.append(bullet)
                self.last_shot = now

        # Atualiza projéteis
        for bullet in self.bullets:
            bullet.update()

        # Remove balas fora da tela
        self.bullets = [b for b in self.bullets if 0 <= b.rect.x <= 800 and 0 <= b.rect.y <= 600]

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.rect)

        if self.predicted_pos:
            pygame.draw.circle(win, (255, 255, 0), self.predicted_pos, 8, 2)

        for bullet in self.bullets:
            bullet.draw(win)
