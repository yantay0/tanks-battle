import pygame
from player import Player


def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SPEED = 0.1
    TANK_SIZE = 64

    # Colors
    BLACK = (0, 0, 0)

    # Keys
    KEY_LEFT = pygame.K_LEFT
    KEY_RIGHT = pygame.K_RIGHT
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    KEY_A = pygame.K_a
    KEY_D = pygame.K_d
    KEY_S = pygame.K_s
    KEY_W = pygame.K_w

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load('assets/tank_icon.png')
    pygame.display.set_caption('Tanks Battle')
    pygame.display.set_icon(icon)

    # Create the players
    player_1 = Player('assets/PNG/Tanks/tank_1.png', 0, (SCREEN_HEIGHT - TANK_SIZE) / 2)
    player_2 = Player('assets/PNG/Tanks/tank_2.png', SCREEN_WIDTH - TANK_SIZE, (SCREEN_HEIGHT - TANK_SIZE) / 2)

    clock = pygame.time.Clock()
    speed = PLAYER_SPEED
    running = True

    # Game loop
    while running:
        # screen color
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # 1st Player
                if event.key == KEY_A:
                    player_1.x_change = -speed
                elif event.key == KEY_D:
                    player_1.x_change = speed
                elif event.key == KEY_S:
                    player_1.y_change = speed
                elif event.key == KEY_W:
                    player_1.y_change = -speed

                # 2nd Player
                elif event.key == KEY_LEFT:
                    player_2.x_change = -speed
                elif event.key == KEY_RIGHT:
                    player_2.x_change = speed
                elif event.key == KEY_UP:
                    player_2.y_change = -speed
                elif event.key == KEY_DOWN:
                    player_2.y_change = speed

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
        player_2.update(dt)
        player_1.update(dt)
        player_1.draw(screen)
        player_2.draw(screen)
        print(player_2.x, player_2.y)
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
