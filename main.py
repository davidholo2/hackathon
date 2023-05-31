import pygame
from fighter import Fighter

pygame.init()

# game window
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FIGHT GAME")

# set framerate
clock = pygame.time.Clock()


# colours
red = (255, 0, 0)
blue = (0, 255, 255)
white = (255, 255, 255)

# game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
round_over_cooldown = 2000

# variables player
warrior_size = 162
warrior_scale = 4
warrior_offset = [72, 56]
warrior_data = [warrior_size, warrior_scale, warrior_offset]
wizard_size = 250
wizard_scale = 3
wizard_offset = [112, 107]
wizard_data = [wizard_size, wizard_scale, wizard_offset]


# bg
bg_image = pygame.image.load(
    "assets/images/background/bg.jpg").convert_alpha()

# spritesheets
warrior_sheet = pygame.image.load(
    "assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/images/wizard/Sprites/wizard.png").convert_alpha()

# victory image
victory_img = pygame.image.load(
    "assets/images/icons/victory.png").convert_alpha()

# number of steps in each animation
warrior_animation_steps = [10, 8, 1, 7, 7, 3, 7]
wizard_animation_steps = [8, 8, 1, 8, 8, 3, 7]

# font
count_font = pygame.font.Font("assets/fonts/Blazed.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Blazed.ttf", 30)

# drawing text


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# drawing background


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))

# drawing fighter health bars


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, white, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, red, (x, y, 400, 30))
    pygame.draw.rect(screen, blue, (x, y, 400 * ratio, 30))


# two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, warrior_data,
                    warrior_sheet, warrior_animation_steps)
fighter_2 = Fighter(2, 700, 310, True, wizard_data,
                    wizard_sheet, wizard_animation_steps)

# game loop
run = True
while run:

    clock.tick(60)

    # background
    draw_bg()

    # player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("Player1: " + str(score[0]), score_font, red, 20, 60)
    draw_text("Player2: " + str(score[1]), score_font, red, 580, 60)

    # update countdown
    if intro_count <= 0:
        # move
        fighter_1.move(screen_width, screen_height,
                       screen, fighter_2, round_over)
        fighter_2.move(screen_width, screen_height,
                       screen, fighter_1, round_over)
    else:
        # count timer
        draw_text(str(intro_count), count_font, red,
                  screen_width / 2-50, screen_height / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, warrior_data,
                                warrior_sheet, warrior_animation_steps)
            fighter_2 = Fighter(2, 700, 310, True, wizard_data,
                                wizard_sheet, wizard_animation_steps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
