"""
pyghelpers is a collection of classes and functions written in Python for use with Pygame.

pyghelpers is pronounced "pig helpers".

Developed by Irv Kalb  -  Irv at furrypants.com

Full documentation at:   https://pyghelpers.readthedocs.io/en/latest/


pyghelpers contains the following classes:

- Timer - a simple timer
- CountUpTimer - a timer that counts up from zero
- CountDownTimer - a timer that counts down from a starting point
- SceneMgr - allows for a Pygame program with multiple scenes
- Scene - base class for a scene managed by the SceneMgr

pyghelpers also contains the following functions:

- textYesNoDialog - a text-based dialog box allowing for one or two answers (yes/no, or just OK)
- customYesNoDialog - a dialog box with custom graphics (yes/no, or just OK)
- textAnswerDialog - a text-based dialog box allowing the user to enter a string
- customAnswerDialog - a dialog box with custom graphics that allows the user to enter a string
- fileExists - find out if a file at a given path exists
- readFile - reads from a (text) file
- writeFile - writes to a (text) file
- openFileForWriting - opens a (text) file for writing line by line
- writeALine - writes a line of text to an open file
- openFileForReading - opens a text file for reading line by line
- readALine - reads a line of text from an open file
- closeFile - closes an open file

"""


import pygame
from pygame.locals import *
import pygwidgets
import sys
import time

PYGHELPERS_NSECONDS_PER_HOUR = 60 * 60
PYGHELPERS_NSECONDS_PER_MINUTE = 60

# Timer classes:
#    Timer (simple)
#    CountUpTimer
#    CountDownTimer


#
#  Timer
#
class Timer():
    """
    This class is used to create a very simple Timer.

    Typical use:

    1)  Create a Timer object:

        myTimer = pyghelpers.Timer(10)

    2)  When you want the timer to start running, make this call:

        myTimer.start()

    3)  In your big loop, check to see if the timer has finished:

        finished = myTimer.update()

    Parameters:
        | timeInSeconds - the duration of the timer, in seconds (integer or float)

    Optional keyword parameters:
        | nickname - an internal name to associate with this timer
        | callback - a function or object.method to be called back when the timer is finished
        |            The nickname of the timer will be passed in when the callback is made


    """
    def __init__(self, timeInSeconds, nickname=None, callBack=None):
        self.timeInSeconds = timeInSeconds
        self.nickname = nickname
        self.callBack = callBack
        self.running = False

    def start(self):
        """Start the timer running (starts at zero)"""
        self.running = True
        self.startTime = time.time()

    def update(self):
        """Call this in every frame to update the timer

        Returns:
           |   False - most of the time
           |   True - when the timer is finished
           |          (you can use this indication, or set up a callback)

        """
        if not self.running:
            return False
        timeElapsed = time.time() - self.startTime
        if timeElapsed < self.timeInSeconds:
            return False  # running but not reached limit

        else:  # Timer has finished
            self.running = False
            if self.callBack is not None:
                self.callBack(self.nickname)

            return True  # True here means that the timer has ended

#
# CountUpTimer class
#
class CountUpTimer():
    """
    This class is used to create a Timer that counts up (starting at zero).

    Its intended use is where you want to continuously display the time on screen (using a DisplayText object).

    Typical use:

    1)  Create a CountUpTimer object:

        myTimer = pyghelpers.CountUpTimer()

    2)  When you want the timer to start running, make this call:

        myTimer.start()

        This method can also be called to restart the timer.

    3)  Whenever you want to get the current time (in seconds since start), you can call any of:

        theTime = pyghelpers.getTime() # gets time as a float

        theTime = pyghelpers.getTimeInSeconds() # gets the time as an integer number of seconds

        theTime = pyghelpers.getTimeInHHMMSS() # gets the time in HH:MM:SS string format

        One of the above should be called every time through your main loop.

    4)  If you want to stop the timer, call:

        myTimer.stop()


    Parameters:
        | none

    """

    def __init__(self):
        self.running = False
        self.savedSecondsElapsed = '0'
        self.secondsStart = 0  # safeguard

    def start(self):
        """Start the timer running (starts at zero).  Can be called to restart the timer, for example to play a game multiple times"""
        self.secondsStart = time.time()  # get the current seconds, and save it away
        self.running = True
        self.savedSecondsElapsed = '0'

    def getTime(self):
        """Returns the time elapsed as a float"""
        if not self.running:
            return self.savedSecondsElapsed  # do nothing
        
        secondsNow = time.time()
        secondsElapsed = secondsNow - self.secondsStart
        self.savedSecondsElapsed = secondsElapsed
        return secondsElapsed  # returns a float

    def getTimeInSeconds(self):
        """Returns the time elapsed as an integer number of seconds"""
        if not self.running:
            return self.savedSecondsElapsed  # do nothing
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        self.savedSecondsElapsed = nSeconds
        return nSeconds

    def getTimeInHHMMSS(self, nMillisecondsDigits=0):
        """Returns the elapsed time as a HH:MM:SS formatted string

        Parameters:

        Optional keyword parameters:
            | nMillisecondsDigits - number of milliseconds digits to include (defaults to 0)
            |    If specified, returned string will look like:    HH:MM:SS.mmmm

        """
        if not self.running:
            return self.savedSecondsElapsed  # do nothing
        
        nSeconds = self.getTime()
        if nMillisecondsDigits > 0:
            millisecondsDigits = nSeconds % 1
            millisecondsDigitsAsInteger = int(millisecondsDigits * (10 ** nMillisecondsDigits))

        nSeconds = int(nSeconds)
        output = ''
        if nSeconds > PYGHELPERS_NSECONDS_PER_HOUR:
            showingHours = True
            nHours = nSeconds // PYGHELPERS_NSECONDS_PER_HOUR
            nSeconds = nSeconds - (nHours * PYGHELPERS_NSECONDS_PER_HOUR)
            output = str(nHours) + ":"
        else:
            showingHours = False
        if showingHours or (nSeconds > PYGHELPERS_NSECONDS_PER_MINUTE):
            nMinutes = nSeconds // PYGHELPERS_NSECONDS_PER_MINUTE
            nSeconds = nSeconds - (nMinutes * PYGHELPERS_NSECONDS_PER_MINUTE)
            if showingHours and (nMinutes < 10):
                output = output + '0' + str(nMinutes) + ":"
            else:
                output = output + str(nMinutes) + ":"
            showingMinutes = True
        else:
            showingMinutes = False
        if showingMinutes and (nSeconds < 10):
            output = output + '0' + str(nSeconds)
        else:
            output = output + str(nSeconds)

        if nMillisecondsDigits > 0:
            output = output + "." + str(millisecondsDigitsAsInteger)

        self.savedSecondsElapsed = output
        return output
    
    def stop(self):
        """Stops the timer from running"""
        self.running = False


#
# CountDownTimer class
#
class CountDownTimer():
    """
    This class is used to create a Timer that counts down from a given starting number of seconds.

    Its intended use is where you want to continuously display the time on screen (using a DisplayText object).


    Typical use:

    1)  Create a CountDownTimer object:

        myTimer = pyghelpers.CountDownTimer(60)   # start the timer at 60 seconds

    2)  When you want the timer to start running, make this call:

        myTimer.start()

        This method also be used to restart the timer.

    3)  Whenever you want to get the current time (in seconds since start), you can call any of:

        theTime = pyghelpers.getTime() # gets time as a float

        theTime = pyghelpers.getTimeInSeconds() # gets the time as an integer number of seconds

        theTime = pyghelpers.getTimeInHHMMSS() # gets the time in HH:MM:SS string format

    4)  If you want to stop the timer, call:

        myTimer.stop()


    Parameters:
        | nStartingSeconds - the starting point for the timer, in seconds (integer or float)

    Optional keyword parameters:
        | stopAtZero - should the timer stop when it reaches zero (defaults to True)
        | nickname - an internal name used to refer to this timer (defaults to None)
        | callback - a function or object.method to be called back when the timer is finished
        |            The nickname of the timer will be passed in when the callback is made


    """

    def __init__(self, nStartingSeconds, stopAtZero=True, nickname=None, callBack=None):
        self.nStartingSeconds = nStartingSeconds
        self.stopAtZero = stopAtZero
        self.nickname = nickname
        self.callBack = callBack

        self.running = False
        self.secondsSavedRemaining = '0'
        self.reachedZero = False

    def start(self):
        """Start the timer running (starts at nStartingSeconds)"""
        secondsNow = time.time()
        self.secondsEnd = secondsNow + self.nStartingSeconds
        self.reachedZero = False
        self.running = True

    def getTime(self):
        """Returns the elapsed time as a float number of seconds"""
        if not self.running:
            return self.secondsSavedRemaining
        
        secondsNow = time.time()
        secondsRemaining = self.secondsEnd - secondsNow
        if self.stopAtZero and (secondsRemaining <= 0):
            secondsRemaining = 0
            self.running = False
            self.reachedZero = True

        self.secondsSavedRemaining = secondsRemaining
        return secondsRemaining  # returns a float

    def getTimeInSeconds(self):
        """Returns the elapsed time as an integer number of seconds"""
        if not self.running:
            return self.secondsSavedRemaining
        
        nSeconds = self.getTime()
        nSeconds = int(nSeconds)
        self.secondsSavedRemaining = nSeconds
        return nSeconds

    def getTimeInHHMMSS(self, nMillisecondsDigits=0):
        """Returns the elapsed time as a HH:MM:SS formatted string

        Parameters:

        Optional keyword parameters:
            | nMillisecondsDigits - number of milliseconds digits to include (defaults to 0)
            |    If specified, returned string will look like:    HH:MM:SS.mmmm

        """

        if not self.running:
            return self.secondsSavedRemaining
        
        nSeconds = self.getTime()
        if nMillisecondsDigits > 0:
            millisecondsDigits = nSeconds % 1
            millisecondsDigitsAsInteger = int(millisecondsDigits * (10 ** nMillisecondsDigits))

        nSeconds = int(nSeconds)
        output = ''
        if nSeconds > PYGHELPERS_NSECONDS_PER_HOUR:
            showingHours = True
            nHours = nSeconds // PYGHELPERS_NSECONDS_PER_HOUR
            nSeconds = nSeconds - (nHours * PYGHELPERS_NSECONDS_PER_HOUR)
            output = str(nHours) + ":"
        else:
            showingHours = False
        if showingHours or (nSeconds > PYGHELPERS_NSECONDS_PER_MINUTE):
            nMinutes = nSeconds // PYGHELPERS_NSECONDS_PER_MINUTE
            nSeconds = nSeconds - (nMinutes * PYGHELPERS_NSECONDS_PER_MINUTE)
            if showingHours and (nMinutes < 10):
                output = output + '0' + str(nMinutes) + ":"
            else:
                output = output + str(nMinutes) + ":"
            showingMinutes = True
        else:
            showingMinutes = False
        if showingMinutes and (nSeconds < 10):
            output = output + '0' + str(nSeconds)
        else:
            output = output + str(nSeconds)

        if nMillisecondsDigits > 0:
            output = output + "." + str(millisecondsDigitsAsInteger)

        self.secondsSavedRemaining = output
        return output


    def stop(self):
        """Stops the timer from running"""
        self.running = False

        # could use the following for a pause/continue later
        #secondsNow = time.time()
        #self.secondsSavedRemaining = self.secondsEnd - secondsNow

    def ended(self):
        """Call to see if the timer has reached zero. Should be called every time through the loop"""
        if self.reachedZero:
            if self.callBack is not None:
                self.callBack(self.nickname)
        return self.reachedZero


#
#
# Scene Manager
#
#
class SceneMgr():
    """SceneMgr (Scene Manager)  allows you to build a program with multiple scenes.

    The SceneMgr manages any number of scenes built as subclasses of the "Scene" class.
    
    For more details, see the "Scene" class.

    Typical use:

    1) Instantiate as many Scenes as you want:
        |
        |  oScene1 = Scene("StartingScene")
        |  oScene2 = Scene("MainScene")
        |  oScene3 = Scene('SometherScene")

    2) Build a dictionary of these scenes with unique keys:

        mySceneDict = {'Splash': oScene1, 'Main': oScene2, 'Other': oScene3}

    3) Instantiate *one* SceneMgr (a singleton):

        oSceneMgr = SceneMgr(mySceneDict, 'Splash', 30)

    4) Call the run method to start the SceneMgr running:

        oSceneMgr.run()


    Parameters:
        | scenesDict - is a dictionary that consists of:
        |    {<sceneKey>:<sceneObject>, <sceneKey:<sceneObject>, ...}
        |      where each sceneKey is a unique string identifying the scene
        |      and each sceneObject is an object instantiated from a scene class
        |      (For details on Scenes, see the Scene class)
        | startingSceneKey - is the string identifying which scene is the starting scene
        | fps - is the frames per second at which the program should run

    Based on a concept of a "Scene Manager" by Blake O'Hare of Nerd Paradise (nerdparadise.com)

    """

    def __init__(self, scenesDict, startingSceneKey, fps):

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
        """ This method implements the main pygame loop.

        It should typically be called as the last line of your main program.

        It is designed to call a standardized set of methods in the current scene.
        Therefore, all scenes must implement these methods (polymorphism):

           |    handleInputs  # called in every frame
           |    draw          # called in every frame


        The following methods can be implemented in a scene.  If they are not
        implemented, then the default version in the Scene subclass will be used.
        (Those methods do not do anything):

           |    enter          # called once whenever the scene is entered
           |    update         # called in every frame
           |    leave          # called once whenever the scene is left

        
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
        """Internal method, called by a Scene tells the SceneMgr to go to another scene

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
        """Internal method, called by a Scene tells SceneMgr to query another scene for information.

        (From the Scene's point of view, it just needs to call its own request method)
        The target scene must implement a method named "respond"

        """
        oTargetScene = self.scenesDict[targetSceneKey]
        info = oTargetScene.respond(infoRequested)
        return info


    def _send_receive(self, targetSceneKey, infoType, info):
        """TInternal method, called by a Scene tells the Scene Manager to send information to another scene

        (From the sending scene's point of view, it just needs to call its own send method)
        The target scene must implement a method named "receive"

        """
        oTargetScene = self.scenesDict[targetSceneKey]
        oTargetScene.receive(infoType, info)


    def _sendAll_receive(self, oSenderScene, infoType, info):
        """Internal method, called by a Scene tells the Scene Manager to send information to all scenes (other than itself)

        (From the sending scene's point of view, it just needs to call its own sendAll method)
        All scenes must implement a method named "receive"

        """
        for sceneKey in self.scenesDict:
            oTargetScene = self.scenesDict[sceneKey]
            if oTargetScene != oSenderScene:
                oTargetScene.receive(infoType, info)



class Scene():
    """The Scene class is an abstract class to be used as a base class for any scenes that you want to create.

    Each scene must be created with a key (which is a unique string) to identify itself.

    The code creating a scene does so by instantiating a scene object from your scene subclass.
    That code must pass in a windows to draw into, and a unique key to identify the scene.
    In the __init__ method of your scene subclass, you will receive a window and a sceneKey.
    You must copy those into instance variables by starting your __init__ method like this:

        |    def __init__(self, window, sceneKey):
        |        self.window = window
        |        self.sceneKey = sceneKey
        |        # Add any initialization you want to do here.

        When your scene is active, the SceneManager calls a standard set of methods in the current scene.
        Therefore, all scenes must implement these methods (polymorphism):

           |    handleInputs  # called in every frame
           |    draw          # called in every frame


        The following methods can optionally be implemented in a scene.  If they are not
        implemented, then the default version in the Scene subclass will be used.
        (The Scene class' default versions do not do anything, they just return):

           |    enter          # called once whenever the scene is entered
           |    update         # called in every frame
           |    leave          # called once whenever the scene is left


    When you want to go to a new scene:

        |    Call self.goToScene and pass in the sceneKey of the scene you want to go to,
        |    and optionally, pass any data you want the next scene to receive in its enter method.

    If you want to quit the program from your scene, call:

        |    self.quit()

    """
    def __del__(self):
        """Internal method, called when the scene is about to die."""
        self.oSceneMgr = None  # eliminate the reference to the SceneMgr

    def _setRefToSceneMgr(self, oSceneMgr):
        """Internal method to save  a reference to the SceneMgr object

        This exists so each class built from this base class can call methods in the Scene Manager
        That reference is used by the goToScene, request, and send methods in each Scene
        Do not change or override this method

        """
        self.oSceneMgr = oSceneMgr

    def enter(self, data):
        """This method is called whenever the user enters a scene

        Should be overridden if you expect data when your scene is entered.
        Add any code you need to start or re-start the scene

        Parameters:
            |    data - can be of any type agreed to by the old and new scenes

        """
        pass


    def handleInputs(self, events, keyPressedList):
        """This method is called in every frame of the scene to handle events and key presses

        Your code MUST override this method.

        Parameters:
            |    events - a list of events your method should handle
            |    keyPressedList - a list of keys that are pressed (a Boolean for each key).

        """
        raise NotImplementedError('Your scene subclass must implement the method: handleInput')

    def update(self):
        """This method is called in every frame of the scene do any processing you need to do here"""
        pass

    def draw(self):
        """This method is called in every frame of the scene to draw anything that needs to be drawn

        Your code must override this method.

        """
        raise NotImplementedError('Your scene subclass must implement the method: draw')

    def leave(self):
        """This method is called whenever the user leaves a scene

        Override this method, and add any code you need to clean up the scene before leaving

        """
        pass

    def quit(self):
        """Call this method if you want to quit, from inside a scene"""
        self.goToScene(None)


    def goToScene(self, nextSceneKey, data=None):
        """Call this method whenever you want to go to a new scene

        Parameters:
            |    nextSceneKey - the scene key (string) of the scene to go to
            |    data - any data you want sent to the next scene (defaults to None)
            |          (The data can be a single value, a list, dictionary, object, etc.)

        """
        self.oSceneMgr._goToScene(nextSceneKey, data)


    def request(self, targetSceneKey, infoRequested):
        """Call this method to get information from another scene

        The target scene must implement a method named: respond,
        it can return any info in any way the two scenes agree upon

        Parameters:
            |    targetSceneKey - the scene key (string) to ask for data
            |    infoRequested - the data you want from the target scene (typically a string)

        """
        info = self.oSceneMgr._request_respond(targetSceneKey, infoRequested)
        return info

    def send(self, targetSceneKey, infoType, info):
        """Call this method to send information to  another scene

        The other scene must implement a method named:  receive.
        You can pass any info the two scenes agree upon

        Parameters:
            |    targetSceneKey - the scene key (string) to ask for data
            |    infoType - the type of data you are sending the target scene (typically a string)
            |    info - the actual data to send (can be any type)


        """
        self.oSceneMgr._send_receive(targetSceneKey, infoType, info)

    def sendAll(self, infoType, info):
        """Call this method to send information to all other scenes

        The other scenes must implement a method named:  receive.
        You can pass any info that the sender and all other scenes agree upon

        Parameters:
            |    infoType - the type of data you are sending the target scene (typically a string)
            |    info - the actual data to send (can be any type)

        """
        self.oSceneMgr._sendAll_receive(self, infoType, info)  # pass in self to identify sender

    def respond(self, infoRequested):
        """Respond to a request for information from some other scene

        You must override this method if your scene expects to handle
        requests for information from other scenes via calls to:  request

        Parameters:
            |    infoRequested - the actual data to be sent back to the caller

        """
        raise NotImplementedError('Your scene subclass must implement the method: respond')

    def receive(self, infoType, info):
        """Receives information from another scene.

        You must override this method if your scene expects to respond to
        other scenes sending information via calls to:  send

        Parameters:
            |    infoType - an identifier for what type of information is being received
            |    info - the information sent from another scene

        """
        raise NotImplementedError('Your scene subclass must implement the method: receive')


#
#  DIALOG Functions
#
DIALOG_BACKGROUND_COLOR = (0, 200, 200)
DIALOG_BLACK = (0, 0, 0)


def textYesNoDialog(theWindow, theRect, prompt, trueButtonText='OK', \
                    falseButtonText='Cancel', backgroundColor=DIALOG_BACKGROUND_COLOR):
    """Puts up a text-based two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (typically with an OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    trueButtonText - text on the True button (defaults to 'OK')
        |    falseButtonText - text on the False button (defaults to 'Cancel')
        |       Note:  If falseButtonText is None or the empty string, the false button will not be drawn
        |              This way, you can present an "alert" box with only an 'OK' button
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))

    Returns:
        |    trueOrFalse - True means true button was pressed, False means false button was pressed

    """
    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    frameRect = pygame.Rect(dialogLeft + 1, dialogTop + 1, dialogWidth - 2, dialogHeight - 2)
    INSET = 30 # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center')

    # Create buttons, fix locations after finding out the size of the button(s)
    hideFalseButton = (falseButtonText is None) or (falseButtonText == '')
    showFalseButton = not hideFalseButton
    if showFalseButton:
        falseButton = pygwidgets.TextButton(theWindow, (0, 0), falseButtonText)
    trueButton = pygwidgets.TextButton(theWindow, (0, 0), trueButtonText)

    trueButtonRect = trueButton.getRect()
    trueButtonHeight = trueButtonRect[3]
    trueButtonWidth = trueButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - trueButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - trueButtonHeight - 20
    if showFalseButton:
        falseButton.setLoc((dialogLeft + INSET, buttonsY))
    trueButton.setLoc((xPos, buttonsY))

    #print('In dialogYesNo')
    #print('theRect is', theRect)
    #print('frameRect is', frameRect)

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if showFalseButton:
                if falseButton.handleEvent(event):
                    return False

            if trueButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, frameRect, 1)

        # 10 - Draw the screen elements
        promptText.draw()
        if showFalseButton:
            falseButton.draw()
        trueButton.draw()

        # 11 - Update the screen
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customYesNoDialog(theWindow, oDialogImage, oPromptText, oTrueButton, oFalseButton):
    """Puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (with a typcial OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) with the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oTrueButton - a CustomButton object (from pygwidgets) representing True or OK, etc.
        |    oFalseButton - a CustomButton object (from pygwidgets) representing False or Cancel, etc.
        |       Note:  If oFalseButton is None or the empty string, the false button will not be drawn
        |              This way, you can present an "alert" box with only an 'OK' button
    Returns:
        |    trueOrFalse - True means true button was pressed, False means false button was pressed

    """
    dialogImageRect = oDialogImage.getRect()
    hideFalseButton = (oFalseButton is None) or (oFalseButton == '')
    showFalseButton = not hideFalseButton

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if showFalseButton:
                if oFalseButton.handleEvent(event):
                    return False

            if oTrueButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the screen area before drawing it again

        # 10 - Draw the screen elements
        oDialogImage.draw()
        oPromptText.draw()
        if showFalseButton:
            oFalseButton.draw()
        oTrueButton.draw()

        # 11 - Update the screen
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def textAnswerDialog(theWindow, theRect, prompt, trueButtonText='OK',\
                    falseButtonText='Cancel', backgroundColor=DIALOG_BACKGROUND_COLOR):
    """Puts up a text-based two-button answerable modal dialog (typically Yes/No or OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    trueButtonText - text on the True button (defaults to 'OK')
        |    falseButtonText - text on the False button (defaults to 'Cancel')
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))

    Returns:
        |    trueOrFalse - True means true button was pressed, False means false button was pressed
        |    userText - if above is True, then this contains the text that the user typed.

    """

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
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, theRect, 1)

        # 10 - Draw the screen elements
        promptText.draw()
        inputText.draw()
        falseButton.draw()
        trueButton.draw()

        # 11 - Update the screen
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customAnswerDialog(theWindow, oDialogImage, oPromptText, oAnswerText, oTrueButton, oFalseButton):
    """Puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) containing the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oAnswerText - an InputDisplay object (from pygwidgets) where the user types their answer
        |    oTrueButton - a CustomButton object (from pygwidgets) representing True or OK, etc.
        |    oFalseButton - a CustomButton object (from pygwidgets) representing False or Cancel, etc.

    Returns:
        |    trueOrFalse - True means true button was pressed, False means false button was pressed
        |    userText - if trueOrFalse above is True, then this contains the text that the user typed.

    """
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
                userResponse = oAnswerText.getValue()
                return True, userResponse

            if oTrueButton.handleEvent(event):
                userResponse = oAnswerText.getValue()
                return True, userResponse

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
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this



#
# File input output functions
#

# Originally:  FileReadWrite.py
import os


# Functions for checking if a file exists, read from a file, write to a file

def fileExists(filePath):
    """Check if a file at a given path exists

    Parameters:
        |    filePath - a path to a file (typically a relative path)
    Returns:
        |    trueOrFalse - True if the file exists, False if the file does not exist

    """
    exists = os.path.exists(filePath)
    return exists


def writeFile(filePath, textToWrite):
    """Writes a string to a file

    The text can contain newline characters which will indicate separate lines

    Parameters:
        |    filePath - a path to a file (typically a relative path)
        |    textToWrite - a string to be written out

    """

    fileHandle = open(filePath, 'w')
    fileHandle.write(textToWrite)
    fileHandle.close()


def readFile(filePath):
    """Read the contents of a text file into a string

    Parameters:
        |    filePath - a path to a file (typically a relative path)
    Returns:
        |    textRead - a string contaning the contents of the file
        |    Note: If the file does not exist, you will get an error message printed
        |          and the function will return the empty string

    """

    if not fileExists(filePath):
        print('The file, ' + filePath + ' does not exist - cannot read it.')
        return ''

    fileHandle = open(filePath, 'r')
    data = fileHandle.read()
    fileHandle.close()
    return data


#  Functions for opening a file, writing & reading a line at a time, and closing the file

def openFileForWriting(filePath):
    """Opens a file for writing

    Parameters:
        |    filePath - a path to a file (typically a relative path)
    Returns:
        |    fileHandle - a file handle for the file that was opened
        |                 (this should be used in subsequent calls to writeALine and closeFile)

    """

    fileHandle = open(filePath, 'w')
    return fileHandle


def writeALine(fileHandle, lineToWrite):
    """Writes a line of text to the already opened file

    Parameters:
        |    fileHandle - a fileHandle to an already opened file (from openFileForWriting)
        |    lineToWrite - a line of text to be written out

    """
    #  Add a newline character '\n' at the end and write the line
    lineToWrite = lineToWrite + '\n'
    fileHandle.write(lineToWrite)


def openFileForReading(filePath):
    """Opens a file for reading

    Parameters:
        |    filePath - a path to a file (typically a relative path)
    Returns:
        |    fileHandle - a file handle for the file that was opened
        |                 (this should be used in sutsequent calls to readALine and closeFile)

    """
    if not fileExists(filePath):
        print('The file, ' + filePath + ' does not exist - cannot read it.')
        return ''

    fileHandle = open(filePath, 'r')
    return fileHandle


def readALine(fileHandle):
    """Writes a line of text to the already opened file

    Parameters:
        |    fileHandle - a fileHandle to an already opened file (from openFileForReading)
    Returns:
        |    lineOrFalse - if a line is available, returns the next line of text in the file
        |                  Otherwise, returns False to indicate end of file has been reached.

    """

    theLine = fileHandle.readline()

    # This is a special check for attempting to read past the end of the file (EOF).
    # If this occurs, let's return something unusual: False (which is not a string)
    # If the caller wishes to check, their code can easily detect the end of the file like this:
    # if returnedValue is False:  # reached EOF

    if theLine == '':  # found End Of File, return False
        return False

    #  If the line ends with a newline character '\n', then strip that off the end
    if theLine.endswith('\n'):
        theLine = theLine.rstrip('\n')

    return theLine


def closeFile(fileHandle):
    """Close a file that was opened earlier with openFileForWriting or openFileForReading

    Parameter:
        |    fileHandle - a handle to an already opened file

    """
    fileHandle.close()


