### PLAYER
import pygame
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.halfHeight = self.height / 2
        self.width = self.rect.width
        self.halfWidth = self.width / 2
        self.maxX = WINDOW_WIDTH - self.rect.width
        self.maxY = GAME_HEIGHT - self.rect.height

    # Every frame, move the player icon to the mouse position
    # Limits the position to the game area of the window
    def update(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.halfWidth
        if self.x < 0:
            self.x = 0
        elif self.x > self.maxX:
            self.x = self.maxX
        self.y = mouseY - self.halfHeight
        if self.y < 0:
            self.y = 0
        elif self.y > self.maxY:
            self.y = self.maxY
        self.rect.left = self.x
        self.rect.top = self.y
        theRect = pygame.Rect(self.x, self.y, self.height, self.width)
        return self.rect

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))