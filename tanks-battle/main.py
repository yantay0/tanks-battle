import pygame, time
from pygame import mixer
from classes import Player, Bullet

running = True

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
PLAYER_SPEED = 0.1
TANK_SIZE = 64
game_over_img = pygame.image.load("assets/png2/game_over.png")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 255)


# pygame.init()


def draw_health_bar(screen, player, color):
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


def isCollision(bullets_player, player_enemy, player_num, screen):
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
                    print(player_enemy.current_health)
                    print(f"Player {player_num} wins!")

                    running = False

                    screen.blit(game_over_img, (0, 100))
            except ValueError:
                pass
        else:
            bullet.draw(screen)


def main():
    # Initialize Pygame
    global running
    pygame.init()
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
    # Game loop
    while running:
        # screen color
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.blit(game_over_img, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                # time.sleep(100)
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
        isCollision(bullets_2, player_1, 2, screen)
        isCollision(bullets_1, player_2, 1, screen)
        draw_health_bar(screen, player_1, RED)
        draw_health_bar(screen, player_2, BLUE)
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
