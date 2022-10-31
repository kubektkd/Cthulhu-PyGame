from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType


# button class
class Button:
    def __init__(self, surface, x: int, y: int, image: Union[Surface, SurfaceType], dimensions: (int, int)):
        self.image = Surface()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.set_image(image, dimensions)

    def set_image(self, image: Union[Surface, SurfaceType], dimensions: (int, int)):
        self.image = pygame.transform.scale(image, dimensions)

    def set_text(self, text):
        pass

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
