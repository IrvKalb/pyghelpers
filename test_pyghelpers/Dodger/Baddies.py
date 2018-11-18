### BADDIE
import pygame
import random
from Constants import *

class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 41  # max plus one
    MIN_SPEED = 1
    MAX_SPEED = 9  # max plus one
    IMAGE = pygame.image.load('images/baddie.png')

    def __init__(self, window):
        self.window = window

        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE)
        self.rect = pygame.Rect(random.randrange(0, WINDOW_WIDTH - size),
                            (0 - size), size, size)  # start above the window
        self.speed = random.randrange(Baddie.MIN_SPEED, Baddie.MAX_SPEED)
        # Set the size of the baddie
        self.image = pygame.transform.scale(Baddie.IMAGE, (size, size))

    def update(self):   # Move the baddie down
        self.rect.top = self.rect.top + self.speed
        if self.rect.top > GAME_HEIGHT:
            return True  # needs to be deleted
        else:
            return False  # stays on window

    def draw(self):
        self.window.blit(self.image, self.rect)

    def collidesWith(self, playerRect):
        if self.rect.colliderect(playerRect):
            return True
        else:
            return False


# BADDIEMGR
class BaddieMgr():
    ADD_NEW_BADDIE_RATE = 8  # add a new baddie every 8 frames

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.baddiesList = []
        self.frameCounter = 0  # add a new baddie every ADD_NEW_BADDIE_RATE frames

    def update(self):
        # If the correct amount of frames have passed,
        # add a new baddie
        self.frameCounter = self.frameCounter + 1
        if self.frameCounter == BaddieMgr.ADD_NEW_BADDIE_RATE:
            # Time to add a new baddie (and reset the counter)
            oBaddie = Baddie(self.window)
            self.baddiesList.append(oBaddie)
            self.frameCounter = 0

        # Tell each baddie to update itself
        # Count how many baddies have fallen off the bottom.
        # Return that count (so score can increase for each one that falls off).
        nBaddiesRemoved = 0
        for baddie in reversed(self.baddiesList):
            deleteMe = baddie.update()
            if deleteMe:
                self.baddiesList.remove(baddie)
                nBaddiesRemoved = nBaddiesRemoved + 1

        return nBaddiesRemoved         


    def draw(self):
        for baddie in self.baddiesList:
            baddie.draw()

    def hasPlayerHitBaddie(self, playerRect):
        for baddie in self.baddiesList:
            if baddie.collidesWith(playerRect):
                return True

        return False
