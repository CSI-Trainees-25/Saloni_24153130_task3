import pygame
import random
import math
from pygame import mixer
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

background = pygame.image.load('background.jpg').convert_alpha()
background.set_alpha(150)
mixer.music.load('backgroung.mp3')
mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf', 32)
game_font = pygame.font.Font('freesansbold.ttf', 64)
level_up_font = pygame.font.Font('freesansbold.ttf', 48)

playerImg = pygame.image.load('spaces.png')
playerX = 370
playerY = 480

bulletImg = pygame.image.load('bullet.jpg')
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"
bullet_Sound = mixer.Sound('gun.mp3')

num_of_enemy = 6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

bombImg = pygame.image.load("bomb.png")
bombX = random.randint(0, 736)
bombY = random.randint(50, 150)
bombX_change = 0.3
bombY_change = 40

bossImg = pygame.image.load("boss.png")
bossX = 200
bossY = 50
boss_health = 10
boss_active = False
bossX_change = 0.2

explosion_Sound = mixer.Sound('explosion.mp3')

bullet_channel = mixer.Channel(1)
explosion_channel = mixer.Channel(2)

score_value = 0
highest_score = 0
level = 1
current_level = 1
show_levelup_timer = 0
lives = 3
game_over_state = False
game_state = "menu"

try:
    with open("highscore.txt", "r") as f:
        highest_score = int(f.read())
except:
    highest_score = 0

def save_highscore():
    global highest_score
    with open("highscore.txt", "w") as f:
        f.write(str(highest_score))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def boss_draw(x, y):
    screen.blit(bossImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(objX, objY, bulletX, bulletY, threshold=27):
    distance = math.sqrt((objX - bulletX) ** 2 + (objY - bulletY) ** 2)
    return distance < threshold

def isPlayerCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((enemyX - playerX) ** 2 + (enemyY - playerY) ** 2)
    return distance < 40

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    high = font.render('High Score: ' + str(highest_score), True, (255, 255, 0))
    screen.blit(score, (x, y))
    screen.blit(high, (x + 400, y))

def show_level(x, y):
    lvl = font.render('Level: ' + str(level), True, (0, 255, 0))
    screen.blit(lvl, (x, y))

def show_lives(x, y):
    live_text = font.render("Lives: " + str(lives), True, (255, 0, 0))
    screen.blit(live_text, (x, y))

def show_levelup():
    global show_levelup_timer
    if show_levelup_timer > 0:
        text = level_up_font.render("LEVEL UP!", True, (0, 255, 255))
        screen.blit(text, (280, 300))
        show_levelup_timer -= 1

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, (200, 200, 200), (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, (150, 150, 150), (x, y, w, h))
    btn_text = font.render(text, True, (0, 0, 0))
    screen.blit(btn_text, (x + (w - btn_text.get_width()) // 2, y + (h - btn_text.get_height()) // 2))

def reset_game():
    global playerX, playerY, bulletX, bulletY, bullet_state
    global enemyX, enemyY, enemyX_change, enemyY_change
    global score_value, level, current_level, lives, game_over_state
    global bombX, bombY, bombX_change, bombY_change
    global boss_health, boss_active, bossX, bossY

    playerX = 370
    playerY = 480
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    level = 1
    current_level = 1
    lives = 3
    game_over_state = False

    enemyX[:] = [random.randint(0, 736) for _ in range(num_of_enemy)]
    enemyY[:] = [random.randint(50, 150) for _ in range(num_of_enemy)]
    enemyX_change[:] = [0.3] * num_of_enemy
    enemyY_change[:] = [40] * num_of_enemy

    bombX = random.randint(0, 736)
    bombY = random.randint(50, 150)
    bombX_change = 0.3
    bombY_change = 40

    boss_health = 10
    boss_active = False
    bossX = 200
    bossY = 50

def quit_to_menu():
    global game_state
    game_state = "menu"

def restart_game():
    reset_game()
    global game_state
    game_state = "playing"

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highscore()
            pygame.quit()
            sys.exit()

    if game_state == "menu":
        title = game_font.render("SPACE INVADERS", True, (255, 255, 0))
        screen.blit(title, (180, 150))
        draw_button("START GAME", 250, 300, 300, 60, restart_game)
        draw_button("QUIT", 250, 400, 300, 60, lambda: sys.exit())

    elif game_state == "playing":
        if not game_over_state:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                playerX -= 0.5
            if keys[pygame.K_RIGHT]:
                playerX += 0.5
            playerX = max(0, min(playerX, 736))

            if keys[pygame.K_SPACE] and bullet_state == "ready":
                bulletX = playerX
                bulletY = playerY
                bullet_state = "fire"
                bullet_channel.play(bullet_Sound)

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change
                if bulletY <= 0:
                    bulletY = playerY
                    bullet_state = "ready"

            for i in range(num_of_enemy):
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = abs(enemyX_change[i])
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -abs(enemyX_change[i])
                    enemyY[i] += enemyY_change[i]

                if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                    bulletY = playerY
                    bullet_state = "ready"
                    score_value += 1
                    explosion_channel.play(explosion_Sound)
                    if score_value > highest_score:
                        highest_score = score_value
                        save_highscore()
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

                if isPlayerCollision(enemyX[i], enemyY[i], playerX, playerY):
                    lives -= 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                    explosion_channel.play(explosion_Sound)
                    if lives <= 0:
                        game_over_state = True

                enemy(enemyX[i], enemyY[i], i)

            bombX += bombX_change
            if bombX <= 0 or bombX >= 736:
                bombX_change *= -1
                bombY += bombY_change

            if isCollision(bombX, bombY, bulletX, bulletY):
                bulletY = playerY
                bullet_state = "ready"
                lives -= 1
                explosion_channel.play(explosion_Sound)
                if lives <= 0:
                    game_over_state = True
                bombX = random.randint(0, 736)
                bombY = random.randint(50, 150)

            screen.blit(bombImg, (bombX, bombY))
            player(playerX, playerY)
            show_score(10, 10)
            show_level(10, 50)
            show_lives(650, 10)
            show_levelup()

            if not boss_active and current_level >= 3 and current_level % 3 == 0:
                boss_active = True
                boss_health = 10
                bossX = 200
                bossY = 50

            if boss_active:
                bossX += bossX_change
                if bossX <= 0 or bossX >= 736:
                    bossX_change *= -1
                boss_draw(bossX, bossY)
                if isCollision(bossX, bossY, bulletX, bulletY, threshold=40):
                    bulletY = playerY
                    bullet_state = "ready"
                    boss_health -= 1
                    explosion_channel.play(explosion_Sound)
                    if boss_health <= 0:
                        score_value += 5
                        boss_active = False
                        boss_health = 10

            new_level = max(1, score_value // 5 + 1)
            if new_level > current_level:
                current_level = new_level
                level = current_level
                show_levelup_timer = 300

        else:
            over_text = game_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(over_text, (200, 120))
            final_score = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
            screen.blit(final_score, (280, 220))
            high_score_text = font.render("High Score: " + str(highest_score), True, (255, 255, 0))
            screen.blit(high_score_text, (280, 270))
            draw_button("PLAY AGAIN", 250, 350, 300, 60, restart_game)
            draw_button("MENU", 250, 450, 300, 60, quit_to_menu)

    pygame.display.update()