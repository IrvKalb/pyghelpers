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


Many helpers allow the use of a callback (a function or method to be called when an action happens)
    Any widget that uses a callback should be set up like this: 
    def <callbackMethodName>(self, nickName):
    When the appropriate action happens, the callback method will be called and the nickName will be passed.
    If you don't need the nickname, you can just ignore that parameter

"""
"""
************************************************************************************************

Simplified BSD License:

Copyright 2017 Irv Kalb. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Irv Kalb ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Irv Kalb OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Irv Kalb.

******************************************************************************************


History:

11/21  Version 1.0.3
    Cleaned up some documentation of parameters
    Removed all FileIO functions
    Added __all__ to define what gets imported when you import *
    Change the SceneMgr so you pass in list of Scenes objects instead of a dictionary.
       Each scene must implement getSceenKey to define the scene key.
       First scene in the list is the starting scene.
    Use ABC for abstract base class and abstract methods
    Updated code using f strings in Timer's getTimeHHMMSS, and clean up of timers
    Turn off key repeating when going to a new scene
    Changed SceneMgr _goToScene method to goToScene

5/26/20  Version 1.0.2
    Added __version__  and function  getVersion()

Version 1.0     01/13/20

"""

__all__ = [
    'CountDownTimer',
    'CountUpTimer',
    'DIALOG_BACKGROUND_COLOR',
    'DIALOG_BLACK',
    'Scene',
    'SceneMgr',
    'Timer',
    'customAnswerDialog',
    'customYesNoDialog',
    'textAnswerDialog',
    'textYesNoDialog',
]

import pygame
from pygame.locals import *
import pygwidgets
import sys
import time
from abc import ABC, abstractmethod

__version__ = "1.0.3"


def getVersion():
    """Returns the current version number of the pyghelpers package"""
    return __version__


# Timer classes:
#    Timer (simple)
#    CountUpTimer
#    CountDownTimer


#  Timer

class Timer():
    """
    This class is used to create a very simple Timer.

    Typical use:

    1)  Create a Timer object:

        myTimer = pyghelpers.Timer(10)

    2)  When you want the timer to start running, make this call:

        myTimer.start()

        You can also call this method to restart the timer after it finishes.

    3)  In your big loop, check to see if the timer has finished:

        finished = myTimer.update()

        Normally returns False, but returns True when the timer is finished

    Parameters:
        | timeInSeconds - the duration of the timer, in seconds (integer or float)

    Optional keyword parameters:
        | nickname - an internal name to associate with this timer (defaults to None)
        | callback - a function or object.method to be called back when the timer is finished
        |            The nickname of the timer will be passed in when the callback is made (defaults to None)


    """
    def __init__(self, timeInSeconds, nickname=None, callBack=None):
        self.timeInSeconds = timeInSeconds
        self.nickname = nickname
        self.callBack = callBack
        self.savedSecondsElapsed = 0.0
        self.running = False

    def start(self, newTimeInSeconds=None):
        """Start the timer running (starts at zero).
        Allows you to optionally specify a different amount of time.
        
        """
        if newTimeInSeconds is not None:
            self.timeInSeconds = newTimeInSeconds
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
        self.savedSecondsElapsed = time.time() - self.startTime
        if self.savedSecondsElapsed < self.timeInSeconds:
            return False  # running but hasn't reached limit

        else:  # timer has finished
            self.running = False
            if self.callBack is not None:
                self.callBack(self.nickname)

            return True  # True here means that the timer has ended

    def getTime(self):
        """ Call this if you want to know how much has elapsed

        Returns:
           |   0 - if the Timer is not running
           |   seconds elapsed since start, as a float

        """
        if self.running:
            self.savedSecondsElapsed = time.time() - self.startTime
            
        return self.savedSecondsElapsed

    def stop(self):
        """Stops the timer"""
        self.getTime()   # remembers final self.savedSecondsElapsed
        self.running = False


# CountUpTimer class

class CountUpTimer():
    """
    This class is used to create a Timer that counts up (starting at zero).

    Its intended use is where you want to continuously display the time in a window (using a DisplayText object).

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
        self.savedSecondsElapsed = 0.0
        self.secondsStart = 0  # safeguard

    def start(self):
        """Start the timer running (starts at zero).  Can be called to restart the timer, for example to play a game multiple times"""
        self.secondsStart = time.time()  # get the current seconds and save the value
        self.running = True
        self.savedSecondsElapsed = 0.0

    def getTime(self):
        """Returns the time elapsed as a float"""
        if not self.running:
            return self.savedSecondsElapsed  # do nothing
        
        self.savedSecondsElapsed = time.time() - self.secondsStart
        return self.savedSecondsElapsed  # returns a float

    def getTimeInSeconds(self):
        """Returns the time elapsed as an integer number of seconds"""
        nSeconds = int(self.getTime())
        return nSeconds

    # Updated version using fStrings
    def getTimeInHHMMSS(self, nMillisecondsDigits=0):
        """Returns the elapsed time as a HH:MM:SS.mmm formatted string

        Parameters:

        Optional keyword parameters:
            | nMillisecondsDigits - number of milliseconds digits to include (defaults to 0)
            |    If specified, returned string will look like:    HH:MM:SS.mmm

        """
        nSeconds = self.getTime()
        mins, secs = divmod(nSeconds, 60)
        hours, mins = divmod(int(mins), 60)

        if nMillisecondsDigits > 0:
            secondsWidth = nMillisecondsDigits + 3
        else:
            secondsWidth = 2

        if hours > 0:
            output = f'{hours:d}:{mins:02d}:{secs:0{secondsWidth}.{nMillisecondsDigits}f}'
        elif mins > 0:
            output = f'{mins:d}:{secs:0{secondsWidth}.{nMillisecondsDigits}f}'
        else:
            output = f'{secs:.{nMillisecondsDigits}f}'

        return output
    
    def stop(self):
        """Stops the timer"""
        self.getTime()   # remembers final self.savedSecondsElapsed
        self.running = False

    # To do:  Would be nice to add both pause and continue methods



#
# CountDownTimer class
#
class CountDownTimer():
    """
    This class is used to create a Timer that counts down from a given starting number of seconds.

    Its intended use is where you want to continuously display the time in a window (using a DisplayText object).


    Typical use:

    1)  Create a CountDownTimer object:

        myTimer = pyghelpers.CountDownTimer(60)   # start the timer at 60 seconds

    2)  When you want the timer to start running, make this call:

        myTimer.start()

        This method can also be used to restart the timer.

    3)  Whenever you want to get the remaining time (in seconds since start), you can call any of:

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
        |            The nickname of the timer will be passed in when the callback is made (defaults to None)


    """

    def __init__(self, nStartingSeconds, stopAtZero=True, nickname=None, callBack=None):
        self.nStartingSeconds = nStartingSeconds
        self.stopAtZero = stopAtZero
        self.nickname = nickname
        self.callBack = callBack

        self.running = False
        self.secondsSavedRemaining = 0.0
        self.reachedZero = False

    def start(self, newStartingSeconds=None):
        """Start the timer running starting at nStartingSeconds (or optional different setting)"""
        secondsNow = time.time()
        if newStartingSeconds is not None:
            self.nStartingSeconds = newStartingSeconds
        self.secondsEnd = secondsNow + self.nStartingSeconds
        self.reachedZero = False
        self.running = True

    def getTime(self):
        """Returns the remaining time as a float number of seconds"""
        if not self.running:
            return self.secondsSavedRemaining
        
        self.secondsSavedRemaining = self.secondsEnd - time.time()
        if self.stopAtZero and (self.secondsSavedRemaining <= 0):
            self.secondsSavedRemaining = 0.0
            self.running = False
            self.reachedZero = True

        return self.secondsSavedRemaining  # returns a float

    def getTimeInSeconds(self):
        """Returns the remaining time as an integer number of seconds"""
        nSeconds = int(self.getTime())
        return nSeconds

    # Updated version using fStrings
    def getTimeInHHMMSS(self, nMillisecondsDigits=0):
        """Returns the remaining time as a HH:MM:SS.mmm formatted string

        Parameters:

        Optional keyword parameters:
            | nMillisecondsDigits - number of milliseconds digits to include (defaults to 0)
            |    If specified, returned string will look like:    HH:MM:SS.mmm

        """
        nSeconds = self.getTime()
        mins, secs = divmod(nSeconds, 60)
        hours, mins = divmod(int(mins), 60)

        if nMillisecondsDigits > 0:
            secondsWidth = nMillisecondsDigits + 3
        else:
            secondsWidth = 2

        if hours > 0:
            output = f'{hours:d}:{mins:02d}:{secs:0{secondsWidth}.{nMillisecondsDigits}f}'
        elif mins > 0:
            output = f'{mins:d}:{secs:0{secondsWidth}.{nMillisecondsDigits}f}'
        else:
            output = f'{secs:.{nMillisecondsDigits}f}'

        self.savedSecondsElapsed = output
        return output


    def stop(self):
        """Stops the timer """
        self.getTime()   # remembers final self.savedSecondsElapsed
        self.running = False
        

    def ended(self):
        """Call to see if the timer has reached zero. Should be called every time through the loop"""
        if self.reachedZero:
            self.reachedZero = False  # reset
            if self.callBack is not None:
                self.callBack(self.nickname)
            return True
        else:
            return False

    # To do:  Would be nice to add both pause and continue methods


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
        |  oScene1 = StartingScene(window)
        |  oScene2 = MainScene(window)
        |  oScene3 = SometherScene(window)

    2) Build a list of these scenes:

        myScenesList = [oScene1, oScene2, oScene3]

    3) Instantiate *one* SceneMgr (a singleton):

        oSceneMgr = SceneMgr(myScenesList, 30) # First scene in the list is the starting scene

    4) Call the run method to start the SceneMgr running:

        oSceneMgr.run()  # First scene in the list is the starting scene


    Parameters:
        | scenesList - is a list that consists of:
        |    [<sceneObject>, <sceneObject>, ...]
        |      where each sceneObject is an object instantiated from a scene class
        |      (For details on Scenes, see the Scene class)
        | fps - is the frames per second at which the program should run

    Based on the concept of a "Scene Manager" by Blake O'Hare of Nerd Paradise (nerdparadise.com)

    """
    def __init__(self, scenesList, fps):

        # Build a dictionary, each entry of which is a scene key : scene object
        self.scenesDict = {}
        for oScene in scenesList:
            key = oScene.getSceneKey()  # Each scene must return a unique key to identify itself
            self.scenesDict[key] = oScene

        # The first element in the list is the used as the starting scene
        self.oCurrentScene = scenesList[0]
        self.framesPerSecond = fps

        # Give each scene a reference back to the SceneMgr.
        # This allows any scene to do a goToScene, request, send,
        # or sendAll, which gets forwarded to the scene manager.
        for key, oScene in self.scenesDict.items():
            oScene._setRefToSceneMgr(self)

    def run(self):
        """ This method implements the main pygame loop.

        It should typically be called as the last line of your main program.

        It is designed to call a standardized set of methods in the current scene.
        
        All scenes must implement the following methods (polymorphism):

           |    handleInputs  # called in every frame
           |    draw          # called in every frame


        The following methods can be implemented in a scene.  If they are not
        implemented, then the default version in the Scene base class will be used.
        (Those methods do not do anything):

           |    enter          # called once whenever the scene is entered
           |    update       # called in every frame
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
                        ((event.type == pygame.KEYDOWN) and
                        (event.key == pygame.K_ESCAPE)):
                    # Tell current scene we're leaving
                    self.oCurrentScene.leave()  
                    pygame.quit()
                    sys.exit()

                eventsList.append(event)

            # Here, we let the current scene process all events,
            # do any "per frame" actions in its update method,
            # and draw everything that needs to be drawn.
            self.oCurrentScene.handleInputs(eventsList, keysDownList)
            self.oCurrentScene.update()
            self.oCurrentScene.draw()

            # 11 - Update the window
            pygame.display.update()

            # 12 - Slow things down a bit
            clock.tick(self.framesPerSecond)
            

    def _goToScene(self, nextSceneKey, dataForNextScene):
        """Called by a Scene, tells the SceneMgr to go to another scene

        (From the Scene's point of view, it just needs to call its own goToScene method)
        This method:
        - Tells the current scene that it is leaving, calls leave method
        - Gets any data the leaving scene wants to send to the new scene
        - Tells the new scene that it is entering, calls enter method

        Raises:
        - KeyError if the nextSceneKey is not valid

        """
        if nextSceneKey is None:  # meaning, exit
            pygame.quit()
            sys.exit()

        # Call the leave method of the old scene to allow it to clean up.
        # Set the new scene (based on the key) and
        # call the enter method of the new scene.
        self.oCurrentScene.leave()
        pygame.key.set_repeat(0) # turn off repeating characters
        try:
            self.oCurrentScene = self.scenesDict[nextSceneKey]
        except KeyError:
            raise KeyError("Trying to go to scene '" + nextSceneKey +
                "' but that key is not in the dictionary of scenes.")
        self.oCurrentScene.enter(dataForNextScene)


    def _request_respond(self, targetSceneKey, requestID):
        """Internal method, called by a Scene tells SceneMgr to query another scene for information.

        (From the Scene's point of view, it just needs to call its own request method)
        The target scene must implement a method named "respond"

        """
        oTargetScene = self.scenesDict[targetSceneKey]
        info = oTargetScene.respond(requestID)
        return info


    def _send_receive(self, targetSceneKey, sendID, info):
        """Internal method, called by a Scene, tells the Scene Manager to send information to another scene

        (From the sending scene's point of view, it just needs to call its own send method)
        The target scene must implement a method named "receive"

        """
        oTargetScene = self.scenesDict[targetSceneKey]
        oTargetScene.receive(sendID, info)


    def _sendAll_receive(self, oSenderScene, sendID, info):
        """Internal method, called by a Scene tells the Scene Manager to send information to all scenes (other than itself)

        (From the sending scene's point of view, it just needs to call its own sendAll method)
        All scenes must implement a method named "receive"

        """
        for sceneKey in self.scenesDict:
            oTargetScene = self.scenesDict[sceneKey]
            if oTargetScene != oSenderScene:
                oTargetScene.receive(sendID, info)



class Scene(ABC):
    """The Scene class is an abstract class to be used as a base class for any scenes that you want to create.

    At startup, you create an instance of each of your scenes, and pass a list of these scenes objects
    when you instantiate the scene manager.

    In the __init__ method of your scene subclass, you will receive a window reference.
    You should copy this into an instance variable like this:

        |    def __init__(self, window):
        |        self.window = window
        |        # Add any initialization you want to do here.

    You also need to write a getSceneKey() method that returns a string
    or constant that uniquely identifies the scene.  It is recommended that you
    build and import a Constants.py file that contains constants for each scene,
    and use the key associated with the current scene here.

        |    def getSceneKey(self):
        |        return <string or CONSTANT that identifies this scene>

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

        |    Call self.goToScene() and pass in the sceneKey of the scene you want to go to,
        |    and optionally, pass any data you want the next scene to receive in its enter() method.

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
        Do not change or override this method.

        """
        self.oSceneMgr = oSceneMgr

    def enter(self, data):
        """This method is called whenever the user enters a scene.

        Should be overridden if you expect data when your scene is entered.
        Add any code you need to start or re-start the scene

        Parameters:
            |    data - can be of any type agreed to by the old and new scenes

        """
        pass

    @abstractmethod
    def getSceneKey(self):
        """This method must return the scene key for this scene
        """
        raise NotImplementedError

    @abstractmethod
    def handleInputs(self, events, keyPressedList):
        """This method is called in every frame of the scene to handle events and key presses

        Your code MUST override this method.

        Parameters:
            |    events - a list of events your method should handle.
            |    keyPressedList - a list of keys that are pressed (a Boolean for each key).

        """
        raise NotImplementedError

    def update(self):
        """This method is called in every frame of the scene do any processing you need to do here"""
        pass

    @abstractmethod
    def draw(self):
        """This method is called in every frame of the scene to draw anything that needs to be drawn

        Your code must override this method.

        """
        raise NotImplementedError

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


    def request(self, targetSceneKey, requestID):
        """Call this method to get information from another scene

        The target scene must implement a method named: respond,
        it can return any info in any way the two scenes agree upon

        Parameters:
            |    targetSceneKey - the scene key (string) of the scene to ask for data
            |    requestID - the data you want from the target scene (typically a string)

        """
        info = self.oSceneMgr._request_respond(targetSceneKey, requestID)
        return info

    def send(self, targetSceneKey, sendID, info):
        """Call this method to send information to  another scene

        The other scene must implement a method named:  receive().
        You can pass any info the two scenes agree upon

        Parameters:
            |    targetSceneKey - the scene key (string) of the scene to ask for data
            |    sendID - the type of data you are sending the target scene (typically a string)
            |    info - the actual data to send (can be any type)


        """
        self.oSceneMgr._send_receive(targetSceneKey, sendID, info)

    def sendAll(self, sendID, info):
        """Call this method to send information to all other scenes

        The other scenes must implement a method named:  receive().
        You can pass any info that the sender and all other scenes agree upon

        Parameters:
            |    sendID - the type of data you are sending the target scene (typically a string)
            |    info - the actual data to send (can be any type)

        """
        self.oSceneMgr._sendAll_receive(self, sendID, info)  # pass in self to identify sender

    def respond(self, requestID):
        """Respond to a request for information from some other scene

        You must override this method if your scene expects to handle
        requests for information from other scenes via calls to:  request()

        Parameters:
            |    requestID - identifier of what data to be sent back to the caller

        """
        raise NotImplementedError

    def receive(self, receiveID, info):
        """Receives information from another scene.

        You must override this method if your scene expects to receive information from
        other scenes sending information via calls to:  send

        Parameters:
            |    receiveID - an identifier for what type of information is being received
            |    info - the information sent from another scene

        """
        raise NotImplementedError


#
#  Dialog functions
#
DIALOG_BACKGROUND_COLOR = (0, 200, 200)
DIALOG_BLACK = (0, 0, 0)

def textYesNoDialog(theWindow, theRect, prompt, yesButtonText='Yes', 
                    noButtonText='No', backgroundColor=DIALOG_BACKGROUND_COLOR,
                    textColor=DIALOG_BLACK):
    """A function that puts up a text-based two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (typically with an OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle (or tuple) of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    yesButtonText - text on the Yes button (defaults to 'Yes')
        |    noButtonText - text on the No button (defaults to 'No')
        |       Note:  If noButtonText is None, the nothing will be drawn for the No button
        |              This way, you can present an "alert" box with only an 'OK' button
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))
        |    textColor - rgb color for the prompt text (defaults to black)

    Returns:
        |    True - meaning the Yes button was pressed
        |        or
        |    False - meaning the No button was pressed
        |
        |   (With an alert dialog, you can ignore the returned value, as it will always be True.)


    """
    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    frameRect = pygame.Rect(dialogLeft + 1, dialogTop + 1, dialogWidth - 2, dialogHeight - 2)
    INSET = 30 # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center', textColor=textColor)

    # Create buttons, fix locations after finding out the size of the button(s)
    showNoButton = not (noButtonText is None)
    if showNoButton:
        noButton = pygwidgets.TextButton(theWindow, (0, 0), noButtonText)
    yesButton = pygwidgets.TextButton(theWindow, (0, 0), yesButtonText)

    yesButtonRect = yesButton.getRect()
    yesButtonHeight = yesButtonRect[3]
    yesButtonWidth = yesButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - yesButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - yesButtonHeight - 20
    if showNoButton:
        noButton.setLoc((dialogLeft + INSET, buttonsY))
    yesButton.setLoc((xPos, buttonsY))

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

            if showNoButton:
                if noButton.handleEvent(event):
                    return False

            if yesButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, frameRect, 1)

        # 10 - Draw the window elements
        promptText.draw()
        if showNoButton:
            noButton.draw()
        yesButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customYesNoDialog(theWindow, oDialogImage, oPromptText, oYesButton, oNoButton):
    """A function that puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (with a typcial OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) with the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oYesButton - a CustomButton object (from pygwidgets) representing Yes or OK, etc.
        |    oNoButton - a CustomButton object (from pygwidgets) representing No or Cancel, etc.
        |       Note:  If oNoButton is None, the No button will not be drawn
        |              This way, you can present an "alert" box with only a single button, like 'OK' 
    Returns:
        |    True - meaning the Yes button was pressed
        |        or
        |    False - meaning the No button was pressed
        |
        |   (With an alert dialog, you can ignore the returned value, as it will always be True.)

    """

    showNoButton = not (oNoButton is None)

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if showNoButton:
                if oNoButton.handleEvent(event):
                    return False

            if oYesButton.handleEvent(event):
                return True

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again

        # 10 - Draw the window elements
        oDialogImage.draw()
        oPromptText.draw()
        if showNoButton:
            oNoButton.draw()
        oYesButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def textAnswerDialog(theWindow, theRect, prompt, okButtonText='OK',
                    cancelButtonText='Cancel', backgroundColor=DIALOG_BACKGROUND_COLOR,
                    promptTextColor=DIALOG_BLACK, inputTextColor=DIALOG_BLACK):
    """A function that puts up a text-based two-button answerable modal dialog (typically OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle (or tuple) of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    okButtonText - text on the OK button (defaults to 'OK')
        |    cancelButtonText - text on the Cancel button (defaults to 'Cancel')
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))
        |    promptTextColor - rgb color of the prompt text (defaults to black)
        |    inputTextColor - rgb color of the input text (defaults to black)

    Returns:
         |   userAnswer - If user presses OK, returns the text the user typed. Otherwise returns None

    """

    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    INSET = 30 # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center',
                                        textColor=promptTextColor)

    inputWidth = dialogWidth - (2 * INSET)
    inputText = pygwidgets.InputText(theWindow, (dialogLeft + INSET, dialogTop + 80),
                                     width=inputWidth, initialFocus=True, textColor=inputTextColor)

    cancelButton = pygwidgets.TextButton(theWindow, (0, 0), cancelButtonText)
    okButton = pygwidgets.TextButton(theWindow, (0, 0), okButtonText)

    okButtonRect = okButton.getRect()
    okButtonHeight = okButtonRect[3]
    okButtonWidth = okButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - okButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - okButtonHeight - 20
    cancelButton.setLoc((dialogLeft + INSET, buttonsY))
    okButton.setLoc((xPos, buttonsY))

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if inputText.handleEvent(event) or okButton.handleEvent(event):
                theAnswer = inputText.getValue()
                return theAnswer

            if cancelButton.handleEvent(event):
                return None

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, theRect, 1)

        # 10 - Draw the window elements
        promptText.draw()
        inputText.draw()
        cancelButton.draw()
        okButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customAnswerDialog(theWindow, oDialogImage, oPromptText, oAnswerText, oOKButton, oCancelButton):
    """A function that puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) containing the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oAnswerText - an InputText object (from pygwidgets) where the user types their answer
        |    oOKButton - a CustomButton object (from pygwidgets) representing OK, etc.
        |    oCancelButton - a CustomButton object (from pygwidgets) representing Cancel, etc.

    Returns:
         |    userAnswer - If user presse OK, returns the text the user typed. Otherwise returns None

    """

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if oAnswerText.handleEvent(event) or oOKButton.handleEvent(event):
                userResponse = oAnswerText.getValue()
                return userResponse

            if oCancelButton.handleEvent(event):
                return None

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again

        # 10 - Draw the window elements
        oDialogImage.draw()
        oAnswerText.draw()
        oPromptText.draw()
        oCancelButton.draw()
        oOKButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this
