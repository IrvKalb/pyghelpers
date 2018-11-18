#  1/18    by Irv Kalb
#
#  Added dialogs
#  Split program into scenes, uses Scene Manager
#  Added 'Goodies' (and Goodie Manager)
#  Changed the scoring mechanism and display.
#  Saves high scores to file.
#  Re-wrote to be object oriented, built Baddie Manager
#
#  Original version by Al Swiegart from his book "Invent With Python"
#    (concept, graphics, and sounds used by permission from Al Swiegart)

import pygame
from pygame.locals import *
import random
import sys
import pygwidgets
import pyghelpers
from Constants import *
from Player import *
from Baddies import *
from Goodies import *


def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (35, 250), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290), theText, \
                                width=WINDOW_WIDTH, justified='center', fontSize=36)
    oYesButton = pygwidgets.TextButton(theWindow, (340, 370), 'Go to high scores')
    oNoButton = pygwidgets.TextButton(theWindow, (110, 370), 'No thanks')
    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow, oDialogBackground, oPromptDisplayText, \
                                         oYesButton, oNoButton)
    return choiceAsBoolean



BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH, WINDOW_HEIGHT - GAME_HEIGHT)

class ScenePlay(pyghelpers.Scene):

    def __init__(self, window, sceneKey):
        # Save window and sceneKey in instance variables
        self.window = window
        self.sceneKey = sceneKey

        self.playBackground = pygwidgets.Image(self.window, (0, 0), 'images/playBackground.jpg')
        self.controlsBackground = pygwidgets.Image(self.window, (0, GAME_HEIGHT), 'images/controlsBackground.jpg')

        self.quitButton = pygwidgets.TextButton(self.window, (30, GAME_HEIGHT + 90), 'Quit', width=120)

        self.highScoresButton = pygwidgets.TextButton(self.window, (240, GAME_HEIGHT + 90), 'Show high scores')

        self.startButton = pygwidgets.TextButton(self.window, (450, GAME_HEIGHT + 90), 'Start New Game', width=120,
                                                 enterToActivate=True)

        self.soundCheckBox = pygwidgets.TextCheckBox(self.window, (430, GAME_HEIGHT + 17), 'Background music',
                                                     True, textColor=WHITE)

        self.gameOverImage = pygwidgets.Image(self.window, (140, 180), 'images/gameOver.png')

        self.titleText = pygwidgets.DisplayText(self.window, (70, GAME_HEIGHT + 17),
                                                'Score:                                 High Score:', \
                            fontSize=24, textColor=WHITE)
        self.scoreText = pygwidgets.DisplayText(self.window, (80, GAME_HEIGHT + 47), '', \
                            fontSize=36, textColor=WHITE, justified='right')

        self.highScoreText = pygwidgets.DisplayText(self.window, (270, GAME_HEIGHT + 47), '', \
                            fontSize=36, textColor=WHITE, justified='right')

        pygame.mixer.music.load('sounds/background.mid')
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameover.wav')

        # instantiate objects
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)
        self.oPlayer = Player(self.window)

        self.highScore = 0
        self.backgroundMusic = True

    def enter(self, data):  # no data passed in
        self.reset()

    def reset(self):   # Start a new game
        self.score = 0
        self.scoreText.setValue(str(self.score))

        # Ask the High Scores scene for a dict of high scores that looks like this:
        #  {'highest': highestScore, 'lowest': lowestScore}
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highScore = infoDict['highest']
        self.highScoreText.setValue(str(self.highScore))
        self.lowestHighScore = infoDict['lowest']

        # Tell the managers to reset themselves
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        self.startButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)
        self.playing = True


    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:

            if not self.playing:
                if self.startButton.handleEvent(event):
                    self.reset()
                    
                if self.highScoresButton.handleEvent(event):
                    self.goToScene(SCENE_HIGH_SCORES)

                if self.quitButton.handleEvent(event):
                    self.quit()
    
                if self.soundCheckBox.handleEvent(event):
                    self.backgroundMusic = self.soundCheckBox.getValue()

                    
    def update(self):
        if self.playing:
            playerRect = self.oPlayer.update()  # move the player
    
            # Tell the Baddie mgr to move all the baddies
            # It returns the number of baddies that fell off the bottom
            nPointsScored = self.oBaddieMgr.update()
            self.score = self.score + nPointsScored
    
            # Tell the Goodie mgr to move any goodies
            self.oGoodieMgr.update()

            # Check if the player has hit any of the goodies
            #print('In ScenePlay, self.oPlayer', self.oPlayer)
            if self.oGoodieMgr.hasPlayerHitGoodie(self.oPlayer):    # was:     self.oPlayer
                self.score = self.score + POINTS_FOR_GOODIE   # add points for each goodie.
                self.dingSound.play()
            self.scoreText.setValue(str(self.score))
    
            # Check if the player has hit any of the baddies
            if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
                pygame.mouse.set_visible(True)
                pygame.mixer.music.stop()

                self.gameOverSound.play()
                self.playing = False
                self.draw()  # force drawing of game over message

                if self.score > self.lowestHighScore:
                    scoreAsString = str(self.score)
                    if self.score > self.highScore:
                        dialogText = 'Congratulations: ' + scoreAsString + ' is a new high score!'
                    else:
                        dialogText = scoreAsString + ' gets you on the high scoresList.'

                    result = showCustomYesNoDialog(self.window, dialogText)

                    # Anternatively, this would build a basic text-button based dialog box
                    #result = textYEsNoDialog(self.window, (35, 250, DIALOG_BOX_WIDTH, 150), \
                    #                              dialogText', 'Go to high scores', 'No thanks)

                    if result:
                        self.goToScene(SCENE_HIGH_SCORES, self.score)  # send the new high score

                self.startButton.enable()
                self.highScoresButton.enable()
                self.soundCheckBox.enable()
                self.quitButton.enable()

    
    def draw(self):
        # Draw everything
        self.window.fill(BLACK)
        self.playBackground.draw()
    
        # Tell the managers to draw all the baddies & goodies
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
    
        # Draw the player
        self.oPlayer.draw()
    
        # Draw all the info at the bottom of the window
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.startButton.draw()

        if not self.playing:
            self.gameOverImage.draw()


    def leave(self):
        pygame.mixer.music.stop()
