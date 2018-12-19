import pygame
from pygame.locals import *
import pygwidgets
import sys
import time



# Timer classes:
#    Timer (simple)
#    CountUpTimer
#    CountDownTimer

#
# Timer class - Simple
#
class Timer():
    def __init__(self, timeInSeconds, framesPerSecond):
        self.framesPerSecond = framesPerSecond
        self.nFramesElapsed = 0
        self.running = False
        self.nFramesToWait = (timeInSeconds * self.framesPerSecond)

    def start(self):
        self.running = True
        self.nFramesElapsed = 0

    def isRunning(self):
        return self.running

    def update(self):
        if not self.running:
            return False
        self.nFramesElapsed = self.nFramesElapsed + 1
        if self.nFramesElapsed >= self.nFramesToWait:
            self.running = False
            return True  # True here means that the timer has ended


#
# CountUpTimer class
#
class CountUpTimer():
    NSECONDS_PER_HOUR = 60 * 60
    NSECONDS_PER_MINUTE = 60

    def __init__(self):
        self.running = False
        self.savedSecondsElapsed = 0

    def start(self):
        self.secondsStart = time.time()  # get the current seconds, and save it away
        self.running = True
        self.savedSecondsElapsed = 0

    def getTime(self):
        if self.running:
            secondsNow = time.time()
            secondsElapsed = secondsNow - self.secondsStart
        else:
            secondsElapsed = self.savedSecondsElapsed
        return secondsElapsed  # returns a float

    def getTimeInSeconds(self):
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        return nSeconds

    def getTimeInHHMMSS(self):
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        output = ''
        if nSeconds > CountDownTimer.NSECONDS_PER_HOUR:
            nHours = nSeconds // CountDownTimer.NSECONDS_PER_HOUR
            nSeconds = nSeconds - (nHours * CountDownTimer.NSECONDS_PER_HOUR)
            output = str(nSeconds) + ":"
        if nSeconds > CountDownTimer.NSECONDS_PER_MINUTE:
            nMinutes = nSeconds // CountDownTimer.NSECONDS_PER_MINUTE
            nSeconds = nSeconds - (nMinutes * CountDownTimer.NSECONDS_PER_MINUTE)
            if (output != '') and (nMinutes < 10):
                output = output + '0' + str(nMinutes) + ":"
            else:
                output = output + str(nMinutes) + ":"
        if (output != '') and (nSeconds < 10):
            output = output + '0' + str(nSeconds)
        else:
            output = output + str(nSeconds)
        return output

    def stop(self):
        self.running = False
        secondsNow = time.time()
        self.savedSecondsElapsed = secondsNow - self.secondsStart


#
# CountDownTimer class
#
class CountDownTimer():
    NSECONDS_PER_HOUR = 60 * 60
    NSECONDS_PER_MINUTE = 60

    def __init__(self, nStartingSeconds, stopAtZero=True):
        self.running = False
        self.secondsSavedRemaining = 0
        self.nStartingSeconds = nStartingSeconds
        self.stopAtZero = stopAtZero

    def start(self):
        secondsNow = time.time()
        self.secondsEnd = secondsNow + self.nStartingSeconds
        self.reachedZero = False
        self.running = True

    def getTime(self):
        if self.running:
            secondsNow = time.time()
            secondsRemaining = self.secondsEnd - secondsNow
            if self.stopAtZero and (secondsRemaining <= 0):
                secondsRemaining = 0
                self.running = False
                self.reachedZero = True
        else:
            secondsRemaining = self.secondsSavedRemaining
        return secondsRemaining  # returns a float

    def getTimeInSeconds(self):
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        return nSeconds

    def getTimeInHHMMSS(self):
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        output = ''
        if nSeconds > CountDownTimer.NSECONDS_PER_HOUR:
            nHours = nSeconds // CountDownTimer.NSECONDS_PER_HOUR
            nSeconds = nSeconds - (nHours * CountDownTimer.NSECONDS_PER_HOUR)
            output = str(nSeconds) + ":"
        if nSeconds > CountDownTimer.NSECONDS_PER_MINUTE:
            nMinutes = nSeconds // CountDownTimer.NSECONDS_PER_MINUTE
            nSeconds = nSeconds - (nMinutes * CountDownTimer.NSECONDS_PER_MINUTE)
            if (output != '') and (nMinutes < 10):
                output = output + '0' + str(nMinutes) + ":"
            else:
                output = output + str(nMinutes) + ":"
        if (output != '') and (nSeconds < 10):
            output = output + '0' + str(nSeconds)
        else:
            output = output + str(nSeconds)
        return output

    def stop(self):
        self.running = False
        secondsNow = time.time()
        self.secondsSavedRemaining = self.secondsEnd - secondsNow

    def ended(self):
        return self.reachedZero


# Scene Manager.    Irv Kalb
#
# Allows you to build a program with multiple scene files
# Includes the Scene class (as a base class) for building scenes.

#
# Based on a concept of a "Scene Manager" by Blake O'Hare of Nerd Paradise (nerdparadise.com)
#


class SceneMgr():

    def __init__(self, scenesDict, startingSceneKey, fps):
        """
        Initialization of the Scene Manager.
        scenesDict is a dictionary that consists of:
          {<sceneKey>:<sceneObject>, <sceneKey:<sceneObject>, ...}
              where each sceneKey is a unique string identifying the scene
              and each sceneObject is an object instantiated from a scene class
          (For details on Scenes, see the Scene class below)
        startingSceneKey is the string identifying which scene to start with
        fps is the frames per second at which the program should run
        """
        self.scenesDict = scenesDict
        if startingSceneKey not in self.scenesDict:
            raise Exception("The starting scene '" + startingSceneKey + \
                            "' is not a key in the dictionary of scenes.")
        self.currentSceneKey = startingSceneKey
        self.oCurrentScene = self.scenesDict[startingSceneKey]
        self.framesPerSecond = fps

        # Give each scene a reference back to the SceneMgr.
        # This allows any scene to do a goToScene, request,
        # and send back to the Scene Manager
        for key in self.scenesDict:
            oScene = self.scenesDict[key]
            oScene._setRefToSceneMgr(self)

    def run(self):
        """
        This is the main pygame loop
        It calls standard methods in the current scene
        """
        clock = pygame.time.Clock()

        # 6 - Loop forever
        while True:

            keysDownList = pygame.key.get_pressed()

            # 7 - Check for and handle events
            eventsList = []
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or \
                        ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    self.oCurrentScene.leave()  # tell current scene we are leaving
                    pygame.quit()
                    sys.exit()

                eventsList.append(event)

            # Here, we let the current scene process all events,
            # do any 'per frame' actions in its update method,
            # and draw everything that needs to be drawn.
            self.oCurrentScene.handleInputs(eventsList, keysDownList)
            self.oCurrentScene.update()
            self.oCurrentScene.draw()

            # 11 - Update the screen
            pygame.display.update()

            # 12 - Slow things down a bit
            clock.tick(self.framesPerSecond)
            

    def _goToScene(self, nextSceneKey, dataForNextScene):
        """
        This method tells the SceneMgr to go to another scene
        (From the Scene's point of view, it just needs to call its own goToScene method)
        This method:
        - Tells the current scene that it is leaving, calls leave method
        - Gets any data the leaving scene wants to send to the new scene
        - Tells the new scene that it is entering, calls enter method
        """
        if nextSceneKey is None:  # meaning, exit
            pygame.quit()
            sys.exit()
        else:
            # Call the leave method of the old scene to allow it to clean up
            # Look up the new scene (based on the key),
            # Call the enter method of the new scene.
            self.oCurrentScene.leave()
            if nextSceneKey not in self.scenesDict:
                raise Exception("Trying to go to unknown scene '" + nextSceneKey + \
                            "' but that key is not in the dictionary of scenes.")
            self.oCurrentScene = self.scenesDict[nextSceneKey]
            self.oCurrentScene.enter(dataForNextScene)


    def _request_respond(self, targetSceneKey, infoRequested):
        """
        This method allows the SceneMgr to query another scene for information.
        (From the Scene's point of view, it just needs to call its own request method)
        The target scene must implement a method named "respond"
        """
        oTargetScene = self.scenesDict[targetSceneKey]
        info = oTargetScene.respond(infoRequested)
        return info


    def _send_receive(self, targetSceneKey, infoType, info):
        """
        This method allows the Scene Manager to send information to another scene
        (From the sending scene's point of view, it just needs to call its own send method)
        The target scene must implement a method named "receive"
        """
        oTargetScene = self.scenesDict[targetSceneKey]
        oTargetScene.receive(infoType, info)


    def _sendAll_receive(self, oSenderScene, infoType, info):
        """
        This method allows the Scene Manager to send information to all scenes (other than itself)
        (From the sending scene's point of view, it just needs to call its own sendAll method)
        All scenes must implement a method named "receive"
        """
        for sceneKey in self.scenesDict:
            oTargetScene = self.scenesDict[sceneKey]
            if oTargetScene != oSenderScene:
                oTargetScene.receive(infoType, info)





"""
The Scene class is an abstract class.  It is meant to be used as a base class
for any scenes that you want to create in your program.
Each scene must have a key (which is a unique string) to identify itself. 

In the __init__ method of your subclass, you will be passed in a window and a sceneKey.
You should copy those into instance variables by starting your __init__ method like this:

def __init__(self, window, sceneKey):
    self.window = window
    self.sceneKey = sceneKey
    # Now add any initialization you want to here.

The following methods are called from the main loop when your scene is active.
Your code can/should override the methods shown here:
    enter
    handleInputs   (must be overridden)
    update
    draw           (must be overridden)
    leave

When you want to go to a new scene:
    call goToScene and pass in the sceneKey of the scene you want to go to,
    and optionally, pass any data you want to next scene to receive in its enter method.

If you want to quit the program from your scene, call:
    self.quit()

"""
class Scene():

    def __del__(self):
        self.oSceneMgr = None  # eliminate the reference to the SceneMgr

    def _setRefToSceneMgr(self, oSceneMgr):
        """
        Internal method to save  a reference to the SceneMgr object
        so each class built from this base class can call methods in the Scene Manager
        That reference is used by the goToScene, request, and send methods in each Scene
        Do not change or override this method
        """
        self.oSceneMgr = oSceneMgr

    def enter(self, data):
        """
        This method is called whenever the user enters a scene
        The data can be of any type agreed to by the old and new scenes
        Add any code you need to start or re-start the scene
        """
        pass


    def handleInputs(self, events, keyPressedList):
        """
        This method is called in every frame of the scene
        to handle events and key presses
        """
        raise NotImplementedError('Your scene subclass must implement the method: handleInput')

    def update(self):
        """
        This method is called in every frame of the scene
        do any processing you need to do here
        """
        pass

    def draw(self):
        """
        This method is called in every frame of the scene
        to draw anything that needs to be drawn
        """
        raise NotImplementedError('Your scene subclass must implement the method: draw')

    def leave(self):
        """
        This method is called whenever the user leaves a scene
        Add any code you want to clean up scene before leaving
        """
        pass

    def quit(self):
        """
        Call this method if you want to quit, from inside a scene
        """
        self.goToScene(None)


    def goToScene(self, nextSceneKey, data=None):
        """
        Call this method whenever you want to go to a new scene
        Pass in the scene key (string) of the scene you want to go to
        and any data you want sent to the next scene
        (The data can be a single value, a list, dictionary, object, etc.)
        """
        self.oSceneMgr._goToScene(nextSceneKey, data)


    def request(self, targetSceneKey, infoRequested):
        """
        Call this method if you need information from another scene
        The target scene must implement a method named: respond,
        it can return any info in any way the two scenes agree upon
        """
        info = self.oSceneMgr._request_respond(targetSceneKey, infoRequested)
        return info

    def send(self, targetSceneKey, infoType, info):
        """
        Call this method if you need to send information to  another scene
        The other scene must implement a method named:  receive.
        You can pass any info the two scenes agree upon
        """
        self.oSceneMgr._send_receive(targetSceneKey, infoType, info)

    def sendAll(self, infoType, info):
        """
        Call this method if you need to send information to all other scenes
        The other scenes must implement a method named:  receive.
        You can pass any info that the sender and all other scenes agree upon
        """
        self.oSceneMgr._sendAll_receive(self, infoType, info)  # pass in self to identify sender

    def respond(self, infoRequested):
        """
        You must override this method if your scene expects to handle
        requests for information from other scenes via calls to:  request
        """
        raise NotImplementedError('Your scene subclass must implement the method: respond')

    def receive(self, targetSceneKey, infoRequested):
        """
        You must override this method if your scene expects to respond to
        other scenes sending information via calls to:  send
        """
        raise NotImplementedError('Your scene subclass must implement the method: receive')


#
#  DIALOG Functions
#
DIALOG_GRAY = (150, 150, 150)
DIALOG_BLACK = (0, 0, 0)

def textYesNoDialog(theWindow, theRect, prompt, trueButtonText='OK', falseButtonText='Cancel'):
    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    frameRect = pygame.Rect(dialogLeft + 1, dialogTop + 1, dialogWidth - 2, dialogHeight - 2)
    INSET = 30 # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center')

    # Create buttons, fix locations after finding out the size of the button(s)
    falseButton = pygwidgets.TextButton(theWindow, (0, 0), falseButtonText)
    trueButton = pygwidgets.TextButton(theWindow, (0, 0), trueButtonText)

    trueButtonRect = trueButton.getRect()
    trueButtonHeight = trueButtonRect[3]
    trueButtonWidth = trueButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - trueButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - trueButtonHeight - 20
    falseButton.setLoc((dialogLeft + INSET, buttonsY))
    trueButton.setLoc((xPos, buttonsY))


    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if falseButton.handleEvent(event):
                return False

            if trueButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again
        pygame.draw.rect(theWindow, DIALOG_GRAY, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, frameRect, 1)

        # 10 - Draw the screen elements
        promptText.draw()
        falseButton.draw()
        trueButton.draw()

        # 11 - Update the screen
        pygame.display.update(theRect)

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customYesNoDialog(theWindow, oDialogImage, oPromptText, oTrueButton, oFalseButton):

    dialogImageRect = oDialogImage.getRect()

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if oFalseButton.handleEvent(event):
                return False

            if oTrueButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again

        # 10 - Draw the screen elements
        oDialogImage.draw()
        oPromptText.draw()
        oFalseButton.draw()
        oTrueButton.draw()

        # 11 - Update the screen
        pygame.display.update(dialogImageRect)

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def textAnswerDialog(theWindow, theRect, prompt, trueButtonText='OK', falseButtonText='Cancel'):
    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    frameRect = pygame.Rect(dialogLeft + 1, dialogTop + 1, dialogWidth - 2, dialogHeight - 2)
    INSET = 30 # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center')

    inputWidth = dialogWidth - (2 * INSET)
    inputText = pygwidgets.InputText(theWindow, (dialogLeft + INSET, dialogTop + 80),
                                     width=inputWidth, initialFocus=True)

    falseButton = pygwidgets.TextButton(theWindow, (0, 0), falseButtonText)
    trueButton = pygwidgets.TextButton(theWindow, (0, 0), trueButtonText)

    trueButtonRect = trueButton.getRect()
    trueButtonHeight = trueButtonRect[3]
    trueButtonWidth = trueButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - trueButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - trueButtonHeight - 20
    falseButton.setLoc((dialogLeft + INSET, buttonsY))
    trueButton.setLoc((xPos, buttonsY))


    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if inputText.handleEvent(event):
                theAnswer = inputText.getValue()
                return True, theAnswer

            if trueButton.handleEvent(event):
                theAnswer = inputText.getValue()
                return True, theAnswer

            if falseButton.handleEvent(event):
                return False, None

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again
        pygame.draw.rect(theWindow, DIALOG_GRAY, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, theRect, 1)

        # 10 - Draw the screen elements
        promptText.draw()
        inputText.draw()
        falseButton.draw()
        trueButton.draw()

        # 11 - Update the screen
        pygame.display.update(theRect)

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customAnswerDialog(theWindow, oDialogImage, oPromptText, oAnswerText, oTrueButton, oFalseButton):
    dialogImageRect = oDialogImage.getRect()

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if oAnswerText.handleEvent(event):
                name = oAnswerText.getValue()
                return True, name

            if oTrueButton.handleEvent(event):
                name = oAnswerText.getValue()
                return True, name

            if oFalseButton.handleEvent(event):
                return False, None

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again

        # 10 - Draw the screen elements
        oDialogImage.draw()
        oAnswerText.draw()
        oPromptText.draw()
        oFalseButton.draw()
        oTrueButton.draw()

        # 11 - Update the screen
        pygame.display.update(dialogImageRect)

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this
