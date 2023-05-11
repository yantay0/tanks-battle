import pygame
from pygame import mixer


class Block:
    blocks = []

    def __init__(self, x, y, size, img_path):
        self.blocks.append(self)
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.current_health = 1
        self.max_health = 1
        self.type = "block"

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def damage(self, value):
        self.blocks.remove(self)


class Map:
    def __init__(self, name, img_path, tile_img):
        self.name = name
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (350, 350))
        self.tile_img = pygame.image.load(tile_img)

    def create_game_map(self):
        # dirt, sand, grass
        # Create a game map surface and fill it with the grass image
        map_width, map_height = 1200, 600
        game_map = pygame.Surface((map_width, map_height))
        for x in range(0, map_width, self.tile_img.get_width()):
            for y in range(0, map_height, self.tile_img.get_height()):
                game_map.blit(self.tile_img, (x, y))
        return game_map


class Player:
    def __init__(self, img_path, x, y, direction, barrel_up_path, barrel_left_path, barrel_down_path,
                 barrel_right_path):
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = 0
        self.y_change = 0
        self.max_health = 5
        self.current_health = 5
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length
        self.direction = direction
        self.barrel_up = pygame.image.load(barrel_up_path)
        self.barrel_left = pygame.image.load(barrel_left_path)
        self.barrel_down = pygame.image.load(barrel_down_path)
        self.barrel_right = pygame.image.load(barrel_right_path)
        self.barrel_image = None
        self.barrel_pos = None
        self.type = "tank"

    def calculate_barrel_position(self):
        # Calculate the position to draw the barrel image
        if self.direction == "right":
            self.barrel_pos = (self.rect.centerx, self.rect.centery - 10)
            self.barrel_image = self.barrel_right
        elif self.direction == "left":
            self.barrel_pos = (self.rect.centerx - 50, self.rect.centery - 10)
            self.barrel_image = self.barrel_left
        elif self.direction == "up":
            self.barrel_pos = (self.rect.centerx - 10, self.rect.centery - 50)
            self.barrel_image = self.barrel_up
        elif self.direction == "down":
            self.barrel_pos = (self.rect.centerx - 10, self.rect.centery)
            self.barrel_image = self.barrel_down

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def draw_health(self, screen, color):
        pygame.draw.rect(screen, color, (10, 10, self.current_health * self.health_ratio, 25))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Draw the barrel image
        self.calculate_barrel_position()
        screen.blit(self.barrel_image, self.barrel_pos)

    def check_borders(self):
        # Check borders
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width > 1200:
            self.rect.x = 1200 - self.rect.width

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y + self.rect.height > 600:
            self.rect.y = 600 - self.rect.height

    def update(self, dt):
        # move the tank by a fixed amount of pixels per block
        block_size = 16  # set block size to be 16 pixels
        self.rect.x += self.x_change * block_size
        self.rect.y += self.y_change * block_size
        self.check_borders()


class HealthBonus:
    def __init__(self, x, y, size, img_path):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.current_health = 1
        self.max_health = 1
        self.type = "bonus"

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply(self, player):
        if player.current_health == player.max_health:
            pass
        else:
            player.current_health += 1


class Bullet:
    def __init__(self, direction):
        self.image = None  # will be set when firing the bullet
        self.rect = None  # will be set when firing the bullet
        self.direction = direction
        self.speed = 10
        self.state = "ready"
        self.set_image_direction(direction)
        self.type = "bullet"

    def set_image_direction(self, direction):
        if direction == "right":
            self.image = pygame.image.load("assets/png2/bullet_right.png")
            self.rect = self.image.get_rect()
        elif direction == "left":
            self.image = pygame.image.load("assets/png2/bullet_left.png")
            self.rect = self.image.get_rect()
        elif direction == "up":
            self.image = pygame.image.load("assets/png2/bullet_up.png")
            self.rect = self.image.get_rect()
        elif direction == "down":
            self.image = pygame.image.load("assets/png2/bullet_down.png")
            self.rect = self.image.get_rect()

    def fire(self, x, y, direction):
        bullet_shot = mixer.Sound("assets/Sounds/Shot.wav")
        bullet_shot.play()
        if self.state == "ready":
            self.set_image_direction(direction)
            self.rect.x = x - 10
            self.rect.y = y - 10
            self.direction = direction
            self.state = "fire"

    def update(self):
        if self.state == "fire":
            if self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            # Check if bullet is off the screen
            if self.rect.right < 0 or self.rect.left > 1200 or self.rect.bottom < 0 or self.rect.top > 600:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, self.rect)
