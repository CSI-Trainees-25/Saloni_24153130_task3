import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('kya.jpg').convert_alpha()
background.set_alpha(150)

mixer.music.load('backgroung.mp3')
mixer.music.play(-1)

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaces.png')
playerX = 370
playerY = 480
playerX_change = 0

enamyImg = []
enamyX = []
enamyY = []
enamyX_change = []
enamyY_change = []
num_of_enamy = 6

for i in range(num_of_enamy):
    enamyImg.append(pygame.image.load('alien.png'))
    enamyX.append(random.randint(0, 736))
    enamyY.append(random.randint(50, 150))
    enamyX_change.append(0.3)
    enamyY_change.append(40)

bulletImg = pygame.image.load('bullet.jpg')
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

score_value = 0
highest_score = 0
level = 1
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
game_font = pygame.font.Font('freesansbold.ttf', 64)

game_over_state = False

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    high = font.render('High Score: ' + str(highest_score), True, (255, 255, 0))
    screen.blit(score, (x, y))
    screen.blit(high, (x+550, y))

def show_level(x, y):
    lvl = font.render('Level: ' + str(level), True, (0, 255, 0))
    screen.blit(lvl, (x, y))

def game_over():
    over_text = game_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text ,(200,120))

    final_score = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(final_score, (280, 220))

    high_score_text = font.render("High Score: " + str(highest_score), True, (255, 255, 0))
    screen.blit(high_score_text, (280, 270))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enamy(x, y, i):
    screen.blit(enamyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < 27

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    btn_text = font.render(text, True, (0, 0, 0))
    screen.blit(btn_text, (x + (w - btn_text.get_width()) // 2, y + (h - btn_text.get_height()) // 2))

def game_loop():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state
    global score_value, enamyX, enamyY, enamyX_change, enamyY_change, game_over_state, level, highest_score

    playerX = 370
    playerY = 480
    playerX_change = 0
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    level = 1
    game_over_state = False

    enamyX[:] = [random.randint(0, 736) for _ in range(num_of_enamy)]
    enamyY[:] = [random.randint(50, 150) for _ in range(num_of_enamy)]
    enamyX_change[:] = [0.3] * num_of_enamy
    enamyY_change[:] = [40] * num_of_enamy

    run = True
    while run:
        screen.fill((0,0,0))
        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not game_over_state:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -0.5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 0.5
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bullet_Sound = mixer.Sound('gun.mp3')
                            bullet_Sound.play()
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0

        if not game_over_state:
            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            level = max(1, score_value // 5 + 1)

            base_speed = 0.3
            speed_increment = 0.02

            for i in range(num_of_enamy):
                if enamyY[i] > 400:
                    game_over_state = True
                    break

                enamyX[i] += enamyX_change[i]

                if enamyX[i] <= 0:
                    enamyX_change[i] = base_speed + (level-1) * speed_increment
                    enamyY[i] += enamyY_change[i]
                elif enamyX[i] >= 736:
                    enamyX_change[i] = -(base_speed + (level-1) * speed_increment)
                    enamyY[i] += enamyY_change[i]

                if isCollision(enamyX[i], enamyY[i], bulletX, bulletY):
                    collision_Sound = mixer.Sound('explosion.mp3')
                    collision_Sound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    if score_value > highest_score:
                        highest_score = score_value

                    enamyX[i] = random.randint(0, 736)
                    enamyY[i] = random.randint(50, 150)

                enamy(enamyX[i], enamyY[i], i)

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, textY)
            show_level(10,50)

        else:
            game_over()

            def restart():
                game_loop()

            draw_button("Play Again", 300, 400, 200, 50, (0, 255, 0), (0, 200, 0), restart)

        pygame.display.update()

def main_menu():
    menu = True
    while menu:
        screen.fill((50, 60, 70))
        title = game_font.render("Space Invaders", True, (255, 255, 0))
        screen.blit(title, (200, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        def start_game():
            nonlocal menu
            menu = False
            game_loop()

        draw_button("Start", 300, 300, 200, 50, (0, 255, 0), (0, 200, 0), start_game)

        pygame.display.update()

main_menu()