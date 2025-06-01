import os
import csv
import pygame
import multiprocessing
from game.player import Player
from game.enemy import Enemy
from sklearn.linear_model import SGDClassifier
from ai.trainer import main as train_models
# --- Inicializações ---

def init_pygame(width=1000, height=1000):
    pygame.init()
    pygame.mixer.init()
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return win, clock

def load_sounds():
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    click_sound = pygame.mixer.Sound('sounds/click.mp3')
    return click_sound

def init_data_file(path='data/player_moves.csv'):
    os.makedirs('data', exist_ok=True)
    f = open(path, 'a', newline='')
    writer = csv.writer(f)
    if( os.stat(path).st_size == 0):  # Verifica se o arquivo está vazio
        writer.writerow(['x', 'y', 'vx', 'vy', 'timestamp'])
    return f, writer

def init_enemy_model():
    model = SGDClassifier()
    model.partial_fit([[0]], [0], classes=[0, 1])
    return model

# --- Desenho na tela ---

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_button(surface, rect, text, mouse_pos, font_size=30):
    if rect.collidepoint(mouse_pos):
        color = (150, 0, 0)
        text_color = (255, 255, 255)
    else:
        color = (100, 0, 0)
        text_color = (200, 200, 200)
    pygame.draw.rect(surface, color, rect, border_radius=8)
    font = pygame.font.SysFont("Arial", font_size)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def train_in_background():
    from ai.trainer import main as train_models
    train_models()

# --- Lógica do jogo ---

def handle_events(running, game_over, button_rect, click_sound, player, enemy, data_file, data_writer):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    click_sound.play()
                    player = Player(WIDTH // 8, HEIGHT // 6)
                    enemy = Enemy(WIDTH // 2, HEIGHT // 2)
                    start_time = pygame.time.get_ticks()

                    game_over = False
                    return running, game_over, player, enemy, data_file, data_writer, start_time
    return running, game_over, player, enemy, data_file, None, None

def update_game_state(player, enemy, data_writer, timestamp):
    for bullet in enemy.bullets:
        if bullet.rect.colliderect(player.rect):
            return True  # game_over
    player.update()
    enemy.update(player)
    data_writer.writerow([player.rect.x, player.rect.y, player.vx, player.vy, timestamp])
    return False

def draw_game(win, player, enemy, survival_time_sec, high_score):
    win.fill((30, 30, 30))
    player.draw(win)
    enemy.draw(win)
    draw_text(win, f"Survival Time: {survival_time_sec}s", 30, 10, 10)
    draw_text(win, f"High Score: {high_score}s", 30, 10, 40)

def draw_game_over(win, survival_time_sec, high_score, button_rect, mouse_pos):
    win.fill((50, 0, 0))
    draw_text(win, "GAME OVER", 60, WIDTH // 2 - 150, HEIGHT // 2 - 100, (255, 100, 100))
    draw_text(win, f"Survival Time: {survival_time_sec}s", 40, WIDTH // 2 - 130, HEIGHT // 2 - 30)
    draw_text(win, f"High Score: {high_score}s", 40, WIDTH // 2 - 130, HEIGHT // 2 + 10)
    draw_button(win, button_rect, "REINICIAR", mouse_pos)

# --- Função principal ---

def main():
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = 800, 600

    win, clock = init_pygame(WIDTH, HEIGHT)
    click_sound = load_sounds()
    data_file, data_writer = init_data_file()
    enemy_model = init_enemy_model()

    player = Player(WIDTH // 8, HEIGHT // 6)
    enemy = Enemy(WIDTH // 2, HEIGHT // 2)
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)

    start_time = pygame.time.get_ticks()
    high_score = 0
    game_over = False
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        timestamp = pygame.time.get_ticks() / 1000.0

        current_time = pygame.time.get_ticks()
        survival_time_ms = current_time - start_time
        survival_time_sec = survival_time_ms // 1000

        mouse_pos = pygame.mouse.get_pos()

        running, game_over, player, enemy, data_file, new_writer, new_start_time = handle_events(
            running, game_over, button_rect, click_sound, player, enemy, data_file, data_writer)

        if new_writer:
            data_writer = new_writer
        if new_start_time:
            start_time = new_start_time

        if not game_over:
            game_over = update_game_state(player, enemy, data_writer, timestamp)
            if game_over:
                if survival_time_sec > high_score:
                    high_score = survival_time_sec
                    print(f"🎉 Novo recorde: {high_score}s!")
                    data_file.flush()
                    multiprocessing.Process(target=train_in_background).start()
            draw_game(win, player, enemy, survival_time_sec, high_score)
        else:
            draw_game_over(win, survival_time_sec, high_score, button_rect, mouse_pos)

        pygame.display.flip()

    pygame.quit()
    data_file.close()

if __name__ == "__main__":
    main()
