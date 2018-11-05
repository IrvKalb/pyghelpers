#
# This the Splash Scene
#

import pygame
from pygame.locals import *
import pygwidgets
import pyghelpers
from Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        self.backgroundImage = pygwidgets.Image(self.window, (0, 0), "images/splashBackground.jpg")
        self.startButton = pygwidgets.TextButton(self.window, (250, 500), 'Start', enterToActivate=True)
        self.quitButton = pygwidgets.TextButton(self.window, (30, 650), 'Quit')
        self.highScoresButton = pygwidgets.TextButton(self.window, (450, 650), 'Show high scores')

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.quitButton.handleEvent(event):
                self.quit()

            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def draw(self):
        self.backgroundImage.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()


