### GOODIE
import pygame
import random
from Constants import *

class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 41  # max plus one
    MIN_SPEED = 1
    MAX_SPEED = 9  # max plus one
    IMAGE = pygame.image.load('images/goodie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE)
        zeroOrOne = random.randrange(0, 2)
        if zeroOrOne == 0:
            self.direction = Goodie.RIGHT
            self.rect = pygame.Rect(0 - size, random.randrange(0, GAME_HEIGHT - size), size,
                                    size)  # start to the left of  the window
            self.speed = random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED)
        else:
            self.direction = Goodie.LEFT
            self.rect = pygame.Rect(WINDOW_WIDTH, random.randrange(0, GAME_HEIGHT - size), size,
                                    size)  # start to the left of  the window
            self.speed = - random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED)
            self.minLeft = - size
        self.image = pygame.transform.scale(Goodie.IMAGE, (size, size))

    def update(self):
        self.rect.left = self.rect.left + self.speed
        if self.direction == Goodie.RIGHT:
            if self.rect.left > WINDOW_WIDTH:
                return True  # needs to be deleted
            else:
                return False  # stays in window
        else:  # moving left
            if self.rect.left < self.minLeft:
                return True  # needs to be deleted
            else:
                return False  # stays in window

    def draw(self):
        self.window.blit(self.image, self.rect)

    def collidesWith(self, playerRect):
        if self.rect.colliderect(playerRect):
            return True
        else:
            return False


# GOODIEMGR
class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 111

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):  # Called when starting a new game
        self.goodiesList = []
        self.frameCounter = 0
        self.createGoodieMax = GoodieMgr.GOODIE_RATE_HI

    def update(self):
        # If the correct amount of frames have passed,
        # add a new goodie at the left or right of the window

        self.frameCounter = self.frameCounter + 1
        if self.frameCounter == self.createGoodieMax:
            # Time to add a new goodie (and reset the counter)
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            self.frameCounter = 0
            # add a new goodie every createGoodieMax frames
            self.createGoodieMax = random.randrange(GoodieMgr.GOODIE_RATE_LO, GoodieMgr.GOODIE_RATE_HI)

        # Tell each goodie to update itself.
        # If a goodie goes off an edge, remove it
        for goodie in self.goodiesList:
            deleteMe = goodie.update()
            if deleteMe:
                self.goodiesList.remove(goodie)         

    def draw(self):
        for goodie in self.goodiesList:
            goodie.draw()

    def hasPlayerHitGoodie(self, playerRect):
        for goodie in self.goodiesList:
            if goodie.collidesWith(playerRect):
                print('player collided with Goodie')
                self.goodiesList.remove(goodie)  # remove this goodie from the list
                return True

        return False
