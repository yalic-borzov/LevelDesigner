import pygame.transform
from pygame import Surface


class Button:
    def __init__(self, x: int, y: int, image: Surface, scale: int):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(
            image, (self.width * scale, self.height * scale)
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen: Surface):
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return self.clicked
