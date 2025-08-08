import pygame
import random

pygame.init()


pygame.mixer.music.load("space-invaders-classic-arcade-game-116826.mp3")

game_over_music = "game-over-arcade-6435.mp3"

pygame.mixer.music.set_volume(0.6)

pygame.mixer.music.play(-1)


Screen_Width = 1920

Screen_Height = 1080

screen = pygame.display.set_mode((Screen_Width, Screen_Height))


heart_img = pygame.image.load("hearts_better.png").convert_alpha()

heart_img = pygame.transform.scale(heart_img, (80, 80))


player_img = pygame.image.load("Player_Tank.png").convert_alpha()

player_img = pygame.transform.scale(player_img, (80, 80))


enemy_img = pygame.image.load("enemy_spimg.png").convert_alpha()

enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bg = pygame.image.load("background.png").convert_alpha()

bg = pygame.transform.scale(bg, (Screen_Width, Screen_Height))


shoot_sound = pygame.mixer.Sound("shoot.wav")

enemy_hit_sound = pygame.mixer.Sound("invaderkilled.wav")

player_hit_sound = pygame.mixer.Sound("explosion.wav")

shoot_sound.set_volume(0.2)

enemy_hit_sound.set_volume(0.3)

player_hit_sound.set_volume(0.4)


player = pygame.Rect((600, 900, 100, 100))
class Enemy:
    def __init__(self, x, y, speed, direction, color, length, width):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.color = color
        self.length = length
        self.width = width

    def update_enemy(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw_enemy(self, screen):
        screen.blit(enemy_img, (int(self.x), int(self.y)))

class Bullet:
    def __init__(self, x, y, speed, direction, color, length, width):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.color = color
        self.length = length
        self.width = width

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.length))

def player_movement():
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-3, 0)
    if key[pygame.K_d]:
        player.move_ip(3, 0)

def reset_game(wave=1):
    global bullets, enemy_bullets, enemies, player_hearts, game_over, player, last_enemy_shot_time, last_shot_time, player_score, enemy_shot_delay, start_x, start_y, spacing_x, spacing_y, row, col, x, y, game_over_music_played

    bullets = []
    enemy_bullets = []
    enemies = []

    start_x = 100
    start_y = 100
    spacing_x = 130
    spacing_y = 80

    rows = min(3 + wave // 2, 6)
    enemy_speed = 2 + wave * 0.3
    enemy_shot_delay = max(300, 1500 - wave * 100)

    for row in range(rows):
        for col in range(10):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            enemies.append(Enemy(x, y, enemy_speed, (-1, 0), (255, 255, 255), 35, 35))

    player_hearts = 3
    player_score = 0 if wave == 1 else player_score
    game_over = False
    player = pygame.Rect((600, 900, 100, 100))
    last_enemy_shot_time = pygame.time.get_ticks()
    last_shot_time = pygame.time.get_ticks()

    pygame.mixer.music.load("space-invaders-classic-arcade-game-116826.mp3")
    pygame.mixer.music.play(-1)

bullets = []

enemy_bullets = []

enemies = []

start_x = 100

start_y = 100

spacing_x = 130

spacing_y = 80

for row in range(3):  # 3 rows
    for col in range(10):  # 10 enemies per row
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        enemies.append(Enemy(x, y, 1, (-1, 0), (255, 255, 255), 35, 35))


last_enemy_shot_time = pygame.time.get_ticks()

last_shot_time = pygame.time.get_ticks()

player_hearts = 3

player_score = 0

wave = 1

enemy_shot_delay = 1500

base_enemy_speed = 2

initial_enemy_shot_delay = 1500

game_over = False

game_over_music_played = False

run = True
while run:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                if pygame.time.get_ticks() - last_shot_time >= 500:
                    new_bullet = Bullet(player.centerx, player.top, 10, (0, -1), (255, 255, 255), 20, 5)
                    bullets.append(new_bullet)
                    shoot_sound.play()
                    last_shot_time = pygame.time.get_ticks()

            if game_over:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_r:
                    wave = 1
                    reset_game(wave)
                    game_over_music_played = False

    if not game_over:
        screen.blit(player_img, (player.x, player.y))

        for i in range(player_hearts):
            screen.blit(heart_img, (45 + i * 90, 40))

        edge_reached = False
        for enemy in enemies:
            enemy.update_enemy()
            if enemy.x <= 0 or enemy.x + enemy.width >= Screen_Width:
                edge_reached = True
            enemy.draw_enemy(screen)

        if len(enemies) == 0:
            wave += 1
            reset_game(wave)

        if edge_reached:
            for enemy in enemies:
                enemy.direction = (-enemy.direction[0], enemy.direction[1])
                enemy.y += 35

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shot_time >= enemy_shot_delay:
            for enemy in enemies:
                if random.randint(1, 10) >= 10:
                    new_enemy_bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.length, 4, (0, 1),
                                              (255, 0, 255), 20, 5)
                    enemy_bullets.append(new_enemy_bullet)
            last_enemy_shot_time = current_time

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.update()
            enemy_bullet.draw(screen)
            if enemy_bullet.y > Screen_Height:
                enemy_bullets.remove(enemy_bullet)

        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.y + bullet.length < 0:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            rect_bullet = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.length)

            for enemy in enemies[:]:
                rect_enemy = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.length)

                if rect_bullet.colliderect(rect_enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    player_score += 100
                    enemy_hit_sound.play()
                    break

        for enemy_bullet in enemy_bullets[:]:
            enemy_rect_bullet = pygame.Rect(enemy_bullet.x, enemy_bullet.y, enemy_bullet.width, enemy_bullet.length)

            if enemy_rect_bullet.colliderect(player):
                enemy_bullets.remove(enemy_bullet)
                player_hearts -= 1
                player_hit_sound.play()
                break

        for enemy in enemies[:]:
            if enemy.y + enemy.length >= 800:
                game_over = True

        if player_hearts == 0:
            game_over = True

        font = pygame.font.SysFont(None, 50)
        text = font.render(f"Score: {player_score} ", True, (255, 255, 255))
        screen.blit(text, ((Screen_Width // 2 + 500) - text.get_width() // 2, Screen_Height // 2 - 500))

        text_wave = font.render(f"Wave {wave}", True, (255, 255, 255))
        screen.blit(text_wave, ((Screen_Width // 2) - text.get_width() // 2, Screen_Height // 2 - 500))

        player_movement()


    else:
        if not game_over_music_played:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(game_over_music)
            pygame.mixer.music.play()
            game_over_music_played = True

        font = pygame.font.SysFont(None, 100)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (Screen_Width // 2 - text.get_width() // 2, Screen_Height // 2))
        subtext = pygame.font.SysFont(None, 50).render("Press R to Restart or ESC to Quit", True, (200, 200, 200))
        screen.blit(subtext, (Screen_Width // 2 - subtext.get_width() // 2, Screen_Height // 2 + 100))

    pygame.display.update()

pygame.quit()
