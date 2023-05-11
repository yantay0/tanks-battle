from idlelib import mainmenu

import pygame
import pygame_menu
from pygame import mixer
from pygame_menu import themes
from classes import Player, Bullet

pygame.init()
running = True

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
PLAYER_SPEED = 0.1
TANK_SIZE = 64

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 255)
BRICK = (255, 79, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('assets/png2/tank_icon.png')
pygame.display.set_caption('Tanks Battle')
pygame.display.set_icon(icon)

# Create the players
player_1 = Player('assets/PNG/Tanks/tankBlue.png', 0, (SCREEN_HEIGHT - TANK_SIZE) / 2,
                  "right", "assets/PNG/Tanks/barrelBlue_up.png",
                  "assets/PNG/Tanks/barrelBlue_left.png",
                  "assets/PNG/Tanks/barrelBlue_down.png",
                  "assets/PNG/Tanks/barrelBlue_right.png")
player_2 = Player('assets/PNG/Tanks/tankGreen.png', SCREEN_WIDTH - TANK_SIZE, (SCREEN_HEIGHT - TANK_SIZE) / 2,
                  "left", "assets/PNG/Tanks/barrelGreen_up.png",
                  "assets/PNG/Tanks/barrelGreen_left.png",
                  "assets/PNG/Tanks/barrelGreen_down.png",
                  "assets/PNG/Tanks/barrelGreen_right.png")

# Bullet
bullets_1 = []
bullets_2 = []

clock = pygame.time.Clock()
speed = PLAYER_SPEED


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)
        self.clicked = False

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(x, y, self.width, self.height)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, self.active_color, button_rect)
            if click[0] == 1 and not self.clicked:
                self.clicked = True
                button_snd = pygame.mixer.Sound("assets/Sounds/button-3.wav")
                button_snd.play()
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, button_rect)
            self.clicked = False

        print_text(message=message, x=x + 15, y=y + 10, font_size=font_size)


def game_over(winner):
    font = pygame.font.Font('freesansbold.ttf', 64)
    if winner is not None:
        text = font.render(f"{winner} wins!", True, BRICK)
    else:
        text = font.render("Game Over", True, BRICK)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(text, text_rect)
    pygame.display.update()


def draw_health_bar(player, color):
    font_obj = pygame.font.Font('freesansbold.ttf', 10)
    text_surface_obj = font_obj.render(f'{int(player.current_health / player.max_health * 100)}%',
                                       True, WHITE)
    x, y = player.rect.centerx, player.rect.centery - 40
    width, height = 70, 10
    border_width = 1
    bar_width = (width - border_width * 2) / player.max_health * player.current_health
    bar_rect = pygame.Rect(x - width / 2 + border_width, y - height / 2 + border_width - 10, bar_width,
                           height - border_width * 2)
    bar_percentage = pygame.Rect(x - width / 2 + border_width, y - height / 2 + border_width - 20, bar_width,
                                 height - border_width * 2)
    screen.blit(text_surface_obj, bar_percentage)
    pygame.draw.rect(screen, color, bar_rect)
    pygame.draw.rect(screen, GREEN, (x - width / 2, y - height / 2 - 10, width, height), border_width)


def isCollision(bullets_player, player_enemy, player_num):
    global running
    for bullet in bullets_player:
        bullet.update()
        if player_enemy.rect.colliderect(bullet.rect):
            touch_sound = pygame.mixer.Sound("assets/Sounds/Blast.wav")
            touch_sound.play()
            explosion_img = pygame.image.load("assets/png2/explosion.png")
            screen.blit(explosion_img, player_enemy.rect)
            player_enemy.current_health -= 1
            print(player_enemy.current_health)

            try:
                bullets_player.remove(bullet)
                if player_enemy.current_health <= 0:
                    if player_num == 1:
                        winner = "Player 1"
                    else:
                        winner = "Player 2"
                    game_over(winner)
                    running = False
            except ValueError:
                pass
        else:
            bullet.draw(screen)


def print_text(message, x, y, font_color=(0, 0, 0), font_type="freesansbold.ttf", font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)

    screen.blit(text, (x, y))


def show_menu():
    menu_bckgr = pygame.image.load("assets/png2/menu.png")

    start_btn = Button(300, 70)

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_bckgr, (0, 0))
        start_btn.draw(450, 200, "Start game", start_game(), 50)
        pygame.display.update()
        clock.tick(60)


def start_game():
    pass

def main_game_loop():
    # Initialize Pygame
    global running
    # Background sounds
    mixer.music.load('assets/Sounds/background.wav')
    mixer.music.play(-1)

    # Keys
    KEY_LEFT = pygame.K_LEFT
    KEY_RIGHT = pygame.K_RIGHT
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    KEY_SPACE = pygame.K_SPACE
    KEY_A = pygame.K_a
    KEY_D = pygame.K_d
    KEY_S = pygame.K_s
    KEY_W = pygame.K_w
    KEY_F = pygame.K_f

    # Load the image
    grass_image = pygame.image.load("assets/PNG/Environment/grass.png")
    # dirt, sand, grass
    # Create a game map surface and fill it with the grass image
    map_width, map_height = SCREEN_WIDTH, SCREEN_HEIGHT
    game_map = pygame.Surface((map_width, map_height))
    for x in range(0, map_width, grass_image.get_width()):
        for y in range(0, map_height, grass_image.get_height()):
            game_map.blit(grass_image, (x, y))

    show_menu()
    # Game loop
    while running:
        # screen color
        screen.fill(BLACK)
        # Draw the game map onto the screen
        screen.blit(game_map, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # 1st Player
                if event.key == KEY_A:
                    player_1.x_change = -speed
                    player_1.direction = "left"
                elif event.key == KEY_D:
                    player_1.x_change = speed
                    player_1.direction = "right"
                elif event.key == KEY_S:
                    player_1.y_change = speed
                    player_1.direction = "down"
                elif event.key == KEY_W:
                    player_1.y_change = -speed
                    player_1.direction = "up"

                # 2nd Player
                elif event.key == KEY_LEFT:
                    player_2.x_change = -speed
                    player_2.direction = "left"
                elif event.key == KEY_RIGHT:
                    player_2.x_change = speed
                    player_2.direction = "right"
                elif event.key == KEY_UP:
                    player_2.y_change = -speed
                    player_2.direction = "up"
                elif event.key == KEY_DOWN:
                    player_2.y_change = speed
                    player_2.direction = "down"
                elif event.key == KEY_F:
                    bullet = Bullet(player_1.direction)
                    bullet.fire(player_1.barrel_pos[0], player_1.barrel_pos[1], player_1.direction)
                    bullets_1.append(bullet)
                    # pass
                elif event.key == KEY_SPACE:
                    bullet = Bullet(player_2.direction)
                    bullet.fire(player_2.barrel_pos[0], player_2.barrel_pos[1], player_2.direction)
                    bullets_2.append(bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d or \
                        event.key == pygame.K_w or event.key == pygame.K_s:
                    player_1.x_change = 0
                    player_1.y_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_2.x_change = 0
                    player_2.y_change = 0

        # Update player position based on elapsed time
        dt = clock.tick(60) / 250.0
        player_1.update(dt)
        player_1.draw(screen)
        player_2.update(dt)
        player_2.draw(screen)
        # mouse_pos = pygame.mouse.get_pos()
        # print("Mouse position:", mouse_pos)
        # print(player_1.rect)

        # Check collision between players' bullets and current health for each
        isCollision(bullets_2, player_1, 2)
        isCollision(bullets_1, player_2, 1)
        draw_health_bar(player_1, RED)
        draw_health_bar(player_2, BLUE)
        pygame.display.update()

    # Add a delay before quitting the game
    pygame.time.delay(3000)
    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main_game_loop()
