import pygame


class Player:
    def __init__(self, img_path, x, y):
        self.image = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_borders(self):
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

    def update(self, dt):
        # move the tank by a fixed amount of pixels per block
        block_size = 16  # set block size to be 50 pixels
        self.x += self.x_change * block_size
        self.y += self.y_change * block_size
        self.check_borders()
