# Modul
import pygame
import random

pygame.init()

# Screen settings
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Henky's home by Cyberchain")

# Game settings
player_start_lives = 3
player_speed = 16
eric_current_speed = 6
eric_speed_acceleration = 0.5
eric_behind_border = 100
score = 0
hankey_speed = 20

# Default Lives/Speed
player_lives = player_start_lives
eric_speed = eric_current_speed

# Fps
fps = 60
clock = pygame.time.Clock()

# Colors
black = pygame.Color("#0f0f0f")
green = pygame.Color("#338a4d")
blue = pygame.Color("#0cb3c2")
red = pygame.Color("#bd3939")
white = pygame.Color("#d5d5e8")

# Fonts
title_font = pygame.font.Font("fonts/orangejuice.ttf", 64)
secondary_font = pygame.font.Font("fonts/orangejuice.ttf", 32)

# Text Title
title_text = title_font.render("Henky's home", True, green)
title_text_rect = title_text.get_rect()
title_text_rect.midtop = (width//2, 5)

# Text Game over
game_over = title_font.render("Game Over!", True, blue)
game_over_rect = game_over.get_rect()
game_over_rect.center = (width//2, height//2)

# Text Continue
continue_text = secondary_font.render("Play again? Press any key...", True, red)
continue_text_rect = game_over.get_rect()
continue_text_rect.center = (width//2, height//2 + 60)

# Text Victory
victory_text = title_font.render("Victory!", True, blue)
victory_text_rect = victory_text.get_rect()
victory_text_rect.center = (width//2, height//2)

# Pictures Kenny
kenny_img = pygame.image.load("img/kenny.png")
kenny_img = pygame.transform.scale(kenny_img, (80, 80))
kenny_img_rect = kenny_img.get_rect()
kenny_img_rect.center = (45, height//2)

# Pictures Eric
eric_img = pygame.image.load("img/eric.png")
eric_img = pygame.transform.scale(eric_img, (50, 50))
eric_img_rect = eric_img.get_rect()
eric_img_rect.x = width + eric_behind_border
eric_img_rect.y = random.randint(70, height-50)

# Pictures Hankey
hankey_img = pygame.image.load("img/hankey.png")
hankey_img = pygame.transform.scale(hankey_img, (60, 65))
hankey_img_rect = hankey_img.get_rect()
hankey_img_rect.center = (775, 60)

# Pictures toliet
toilet_img = pygame.image.load("img/toilet.png")
toilet_img = pygame.transform.scale(toilet_img, (50, 50))
toilet_img_rect = toilet_img.get_rect()
toilet_img_rect.center = (35, 65)

# Pictures toliet close
close_img = pygame.image.load("img/toilet_close.png")
close_img = pygame.transform.scale(close_img, (50, 50))
close_img_rect = close_img.get_rect()
close_img_rect.center = (35, 60)

# Music game title
pygame.mixer.music.load("media/music_title.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(3)

# Sounds game
sound_crash = pygame.mixer.Sound("media/sound_crash.wav")
sound_crash.set_volume(0.2)

sound_take = pygame.mixer.Sound("media/sound_take.wav")
sound_take.set_volume(0.2)

sound_victory = pygame.mixer.Sound("media/victory.wav")
sound_gameover = pygame.mixer.Sound("media/gameover.wav")

# Main cycle
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # Move - Kenny
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and kenny_img_rect.top > 65:
        kenny_img_rect.y -= player_speed
    elif keys[pygame.K_DOWN] and kenny_img_rect.bottom < height:
        kenny_img_rect.y += player_speed

    # Move - Eric and Score
    if eric_img_rect.x < 0:
        player_lives -= 1
        eric_img_rect.x = width + eric_behind_border
        eric_img_rect.y = random.randint(65, height-50)
        sound_crash.play()
    else:
        eric_img_rect.x -= eric_current_speed

    # Victory - Check colision
    if hankey_img_rect.left <= 23:
        screen.blit(victory_text, victory_text_rect)
        screen.blit(continue_text, continue_text_rect)
        screen.blit(close_img, close_img_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        sound_victory.play()

        # Restart game
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    # Default lives
                    player_lives = player_start_lives
                    # Default speed
                    eric_current_speed = eric_speed
                    # Default Kenny/Hankey
                    hankey_img_rect.center = (775, 70)
                    kenny_img_rect.center = (45, height // 2)
                    pygame.mixer.music.play(3)
                    pause = False
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

    # Check colision - Kenny/Eric
    if kenny_img_rect.colliderect(eric_img_rect):
        score += 1
        sound_take.play()
        # Acceleration move
        eric_current_speed += eric_speed_acceleration
        # Edge Eric screen
        eric_img_rect.x = width + eric_behind_border
        eric_img_rect.y = random.randint(65, height-50)
        hankey_img_rect.x -= hankey_speed

    # Rendering
    screen.fill(black)

    # Shape Line
    pygame.draw.line(screen, white, (0, 65), (width, 65), 2)

    # Text Lives
    lives_text = secondary_font.render(f"Lives: {player_lives}", True, red)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.midright = 715, 35

    # Text Score
    score_text = secondary_font.render(f"Score: {score}", True, blue)
    score_text_rect = score_text.get_rect()
    score_text_rect.midleft = 80, 35

    # Blit
    screen.blit(title_text, title_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    screen.blit(kenny_img, kenny_img_rect)
    screen.blit(eric_img, eric_img_rect)
    screen.blit(hankey_img, hankey_img_rect)
    screen.blit(toilet_img, toilet_img_rect)

    # Game over - Check colision
    if player_lives == 0:
        screen.blit(game_over, game_over_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.mixer.music.stop()
        sound_gameover.play()

        # Update screen
        pygame.display.update()

        # Restart game
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    # Lives default
                    player_lives = player_start_lives
                    # Speed default
                    eric_current_speed = eric_speed
                    pygame.mixer.music.play(3)
                    hankey_img_rect.center = (775, 70)
                    kenny_img_rect.center = (45, height // 2)
                    pause = False
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

    # Update screen
    pygame.display.update()

    # Slow down cycle
    clock.tick(fps)

pygame.quit()
