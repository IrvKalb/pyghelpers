"""
pygwidgets module by Irv Kalb      Irv@furrypants.com


The pygwidgets module (pronounced as: "pig wijits") allows programmers to easily create 
user interface widgets in Python with pygame.  Each of the button widgets come in two varieties:
a basic "default" widget that is drawn using the Python drawing tools, and a "Custom" version where
the programmer supplies their own graphics for the widget. For example, "TextButton" below builds a button
from a user-supplied string, whereas "CustomButton" is built to work with user-supplied graphics.  

Design notes:
  1) The way that you use the objects instantiated from all these classes is very similar:  
     - Instantiate before the big loop starts.
     - Call the "handleEvent" method every time through the loop, which returns True when something 
       exciting happens (for example, user clicks on a button).
     - Call the "draw" method (with no arguments) to draw each widget.
  2) I have tried to make consistent names across classes for keyword parameters. 
  3) I have also tried to make consistent names for methods across classes.
     For example "getValue" and "setValue" are available in most classes.  
  4) When instantiating objects from these classes, you typically only need to specify a few parameters. 
     The rest will use reasonable default values, but you can change them using keyword arguments.  
 
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
 
pygwidgets contains the following classes:

- TextButton - a button built on the fly from a user-supplied label (string).
- CustomButton - a button where you use your own images

- TextCheckBox - a checkbox built on the fly from a user-supplied label (string).
- CustomCheckBox - a checkbox where you use your images 

- TextRadioButton - a radio button built on the fly from a user-supplied label (string).
- CustomRadioButton - a radio button where you use your images

- DisplayText - a text field used just for output (display)

- InputText - a text field intended for user input

- Dragger - gives the ability to drag any screen object with the mouse

- Image - simple display of an image at a location




History:
5/18   Added Image object.  Allows you to set a loc and window at the instantiation.
    That way, all you need to do to show the image is to call its draw method.

1/18   Changed Button->TexButton, CheckBox->TextCheckBox, RadioButton->TextRadioButton
    Changed SetVisible->show, setInVisible->hide
    Created PygWidget base class, and have all classes inherit from it
        initializes and contains: label, visible, isEnabled

11/17  Added Dragger, changed main "surface" to "window"  Irv Kalb
    Changed 'caption' in the Button class to 'label', made it a positional parameter (instead of optional keyword param)
    Added 'label' and getLabel method to most classes
    Modified Button to grow to fit very long labels - defaults to minimum of 100 pixels.
    Added setPos to DisplayText 

4/17  Version 1.1 by Irv Kalb
    Renamed a few classes and methods, simplified the return of handleEvent in all classes
    to be just True or False.

3/17  Version 1.0 by Irv Kalb
    Combined Buttons, CheckBoxes, RadioButtons, and Text into a single file

1/17  Major rewrite by Irv Kalb
    Split the code into Button class and CustomButton class (with a common superclass: PygWidgetsButton).
    Added appropriate parameters with reasonable defaults so each is easier to instantiate.
    Added soundOnClick

12/16  Modified by Irv Kalb
     Add a default surface, so it is passed in once
     at creation.  That way, calls to draw do not need to pass it in again.

8/14   Modified by Irv Kalb
     Added a disabled state to all buttons
     
The code of the Button and CustomButton are based on the origial "pygbutton" code
developed by Al Sweigart.  I kept the good stuff (and there was plenty of that!), 
added features (most importantly a disabled state), and removed some features that
I didn't feel were needed for the students in my classes.
     

**************************************************************************************
ORIGINAL COMMENTS FROM AL SWEIGART ABOUT PYGBUTTON:

PygButton v0.1.0

PygButton (pronounced "pig button") is a module that implements UI buttons for Pygame.
PygButton requires Pygame to be installed. Pygame can be downloaded from http://pygame.org
PygButton was developed by Al Sweigart (al@inventwithpython.com)
https://github.com/asweigart/pygbutton


Simplified BSD License:

Copyright 2012 Al Sweigart. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Al Sweigart ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Al Sweigart OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Al Sweigart.
"""

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)
GRAY = (128, 128, 128)
DOWN_GRAY = (140, 140, 140)
NORMAL_GRAY = (170, 170, 170)
OVER_GRAY = (210, 210, 210)
DISABLED_GRAY = (220, 220, 220)

pygame.font.init()

class PygWidget():
    """
    This is the base class (superclass) of ALL pygwidgets.  It provides common functionality:
    - ability to show or hide any widget
    - ability to enable or disable any widget
    - save and retrieve a label (name) associated with the widget
    - ability to get and set the loc, and get the rect of any widget
    """
    def __init__(self, label):
        self.visible = True
        self.isEnabled = True
        self.label = label  # any label (name) you want to associate with this widget

    def show(self):
        """ Make this widget visible """
        self.visible = True

    def hide(self):
        """ Make this widget invisible """
        self.visible = False

    def getVisible(self):
        """ Returns the visible state """
        return self.visible

    def enable(self):
        """ Set this widget enabled"""
        self.isEnabled = True

    def disable(self):
        """ Disable the current widget"""
        self.isEnabled = False

    def getEnabled(self):
        """ Returns the enabled state """
        return self.isEnabled

    def getLabel(self):
        """ Get the label associated with this widget """
        return self.label

    def setLoc(self, loc):   # loc must be a tuple or list of x,y coordinates
        """ Sets a new location (and changes the rect loc) for this widget """
        self.loc = loc
        self.rect[0] = self.loc[0]
        self.rect[1] = self.loc[1]

    def getLoc(self):
        """ Returns the location for this widget """
        return self.loc

    def getRect(self):
        return self.rect


#
#
# BUTTON
# 
#
class PygWidgetsButton(PygWidget):
    """
    This is the base class of TextButton (button built on the fly from a given text label)
    and CustomButton (one where you supply custom graphics).  Details are in comments for those classes below.
    You should never instantiate from this class.
    Instead, instantiate a TextButton or CustomButton, then use the rest of the methods provided here.
    This code handles showing all the appropriate states of the button (up, down, over, disabled),
    based on user actions and method calls.


    Typical use:
    
    1) Create a button.  Your choice between two different types:

    Either a TextButton (giving a loc (left, top) and a label):

        myButton = pygwidgets.TextButton(window, (500, 430), 'Some Text Label')

        There are many optional parameters, including width and height that have good defaults.    
        
    Or a CustomButton - giving a location tuple - as (left, top) and up to four images:

        myButton = pygwidgets.CustomButton(window, (500, 430), \
                                up='images/ButtonUp.png',
                                down='images/ButtonDown.png',
                                over='images/ButtonOver.png',
                                disabled='images/ButtonDisabled.png')


    2) In your big loop, check for the button being clicked by calling its handleEvent method:

        if myButton.handleEvent(event):  # When the button is clicked, this returns True
            #  the button was clicked,
            #  do whatever you want here

    3) At the bottom of your big loop, draw the button:

        myButton.draw()
        
    """
        
    def __init__(self, window, loc, surfaceUp, surfaceOver, surfaceDown, \
                 surfaceDisabled, theRect, soundOnClick, label, enterToActivate):

        if type(self) is PygWidgetsButton:
            raise Exception('You need to instantiate a TextButton or CustomButton (not PygWidgetsButton directly)')

        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.surfaceUp = surfaceUp
        self.surfaceOver = surfaceOver
        self.surfaceDown = surfaceDown
        self.surfaceDisabled = surfaceDisabled
        self.rect = theRect
        self.soundOnClick = soundOnClick
        self.enterToActivate = enterToActivate

        # used to track the state of the button
        self.buttonDown = False # is the button currently pushed down?
        self.mouseOverButton = False # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Tracks clicks.)
        if self.soundOnClick is not None:
            self.playSoundOnClick = True
            if type(self.soundOnClick) is str:  # user specified sound path, load it here
                pygame.mixer.init()
                self.soundOnClick = pygame.mixer.Sound(self.soundOnClick)  # save in same instance variable
        else:
            self.playSoundOnClick = False

        self.mouseIsDown = False


    def handleEvent(self, eventObj):
        """
        This method should be called every time through the main loop.  It handles showing the
        up, over, and down states of the button.  When the user clicks down and later up
        on the button, this method will return True to signal that the user has clicked on it.
        Normally returns False.
        """

        if self.enterToActivate:
            if eventObj.type == pygame.KEYDOWN:

                # Return or Enter key
                if eventObj.key == pygame.K_RETURN:
                    return True

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self.visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return False

        if not self.isEnabled:
            return False

        clicked = False

        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)
        if (not self.mouseOverButton) and eventPointInButtonRect:
            # if mouse has entered the button:
            self.mouseOverButton = True

        elif self.mouseOverButton and (not eventPointInButtonRect):
            # if mouse has exited the button:
            self.mouseOverButton = False

        if eventPointInButtonRect:

            if eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True

        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        if eventObj.type == MOUSEBUTTONDOWN:
            self.mouseIsDown = True
            
        # mouse up is handled whether or not it was over the button
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            self.mouseIsDown = False
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False

            if doMouseClick:
                self.buttonDown = False
                clicked = True
                self.mouseOverButton = False  # forces redraw of up state after click
                
                if self.playSoundOnClick:
                    self.soundOnClick.play()

        return clicked

    def draw(self):
        """ Draws the button """
        if not self.visible:
            return

        # Blit the button's current appearance to the surface.
        if self.isEnabled:
            if self.mouseIsDown:
                if self.mouseOverButton and self.lastMouseDownOverButton:
                    self.window.blit(self.surfaceDown, self.loc)
                else:
                    self.window.blit(self.surfaceUp, self.loc)
            else:  # mouse is up
                if self.mouseOverButton:
                    self.window.blit(self.surfaceOver, self.loc)
                else:
                    self.window.blit(self.surfaceUp, self.loc)

        else:
            self.window.blit(self.surfaceDisabled, self.loc)


    def _debug(self):
        """' This is just for debugging, so we can see what buttons were drawn - not intended to be used in production"""
        self.window.blit(self.surfaceUp, (self.loc[0], 10))
        self.window.blit(self.surfaceOver, (self.loc[0], 60))
        self.window.blit(self.surfaceDown, (self.loc[0], 110))
        self.window.blit(self.surfaceDisabled, (self.loc[0], 160))


class TextButton(PygWidgetsButton):
    """
    TextButton is a class that creates a simple button on the fly from a given label text.
    Each TextButton has four states:  up, over, down, and disabled


    TextButton Parameters:
        window - the window to draw the button in
        loc - The location (left and top) of the button as a tuple e.g. (10, 200).
        label - The text on the button
    --Optional parameters:
        width - The width of the button (default is 100)
        height - the height of the button (default is 40)
        textColor - The color of the text. (default is black).
        upColor - The background color of the up button (default is a medium gray)
        overColor - The background color of the over button (default is a lighter gray)
        downColor - The background color of down button (default is a darker gray)
        fontName - The name of the font to use for the label (default is freesansbold)
        fontsize - The size fo the font to use (default is 14)
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the button is clicked (defaults to None)
        enterToActivate - If user presses Enter (or Return), button will activate (default is False)
    """

    DEFAULT_FONT_NAME = None # use pygame default font
    DEFAULT_FONT_SIZE = 20
    PYGWIDGETS_FONT = pygame.font.Font(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
    MINIMUM_WIDTH = 100

    def __init__(self, window, loc, label, width=None, height=40, textColor=BLACK, \
                 upColor=NORMAL_GRAY, overColor=OVER_GRAY, downColor=DOWN_GRAY, \
                 fontName=DEFAULT_FONT_NAME, fontSize=DEFAULT_FONT_SIZE, soundOnClick=None,\
                 enterToActivate=False):
        """ Initialize a text-based button object """
        
        # Create the button's Surface objects.
        label = ' ' + label + ' '  #  add padding for drawn text
        self.textColor = textColor
        self.upColor = upColor
        self.overColor = overColor
        self.downColor = downColor

        if (fontName == TextButton.DEFAULT_FONT_NAME) and (fontSize == TextButton.DEFAULT_FONT_SIZE):
            self.font = TextButton.PYGWIDGETS_FONT
        else:
            self.font = pygame.font.SysFont(fontName, fontSize)


        # create the label text for up state of button (to get the size)
        labelSurfaceUp = self.font.render(label, True, self.textColor, self.upColor)
        labelRect = labelSurfaceUp.get_rect()
        if width is None:
            # See if the text will fit inside the minimum width
            if labelRect.width < TextButton.MINIMUM_WIDTH:
                width = TextButton.MINIMUM_WIDTH
            else:  # Make the width wide enough to handle all the text
                width = labelRect.width

        buttonRect = pygame.Rect(loc[0], loc[1], width, height)
        w = buttonRect.width  # syntactic sugar
        h = buttonRect.height  # syntactic sugar
        size = buttonRect.size

        labelRect.center = (int(w / 2), int(h / 2))

        # draw the up button
        surfaceUp = pygame.Surface(size)
        surfaceUp.fill(self.upColor)
        surfaceUp.blit(labelSurfaceUp, labelRect)
        if enterToActivate:
            pygame.draw.rect(surfaceUp, BLACK, pygame.Rect((0, 0, w - 1, h - 1)), 2)  # thicker black border
            pygame.draw.line(surfaceUp, WHITE, (2, 2), (w - 3, 2))
            pygame.draw.line(surfaceUp, WHITE, (2, 2), (2, h - 3))
            pygame.draw.line(surfaceUp, GRAY, (3, h - 3), (w - 3, h - 3))
            pygame.draw.line(surfaceUp, GRAY, (w - 3, 3), (w - 3, h - 3))
        else:
            pygame.draw.rect(surfaceUp, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border
            pygame.draw.line(surfaceUp, WHITE, (1, 1), (w - 2, 1))
            pygame.draw.line(surfaceUp, WHITE, (1, 1), (1, h - 2))
            pygame.draw.line(surfaceUp, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
            pygame.draw.line(surfaceUp, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
            pygame.draw.line(surfaceUp, GRAY, (2, h - 2), (w - 2, h - 2))
            pygame.draw.line(surfaceUp, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw the down button
        surfaceDown = pygame.Surface(size)
        surfaceDown.fill(self.downColor)
        labelSurfaceDown = self.font.render(label, True, self.textColor, self.downColor)
        labelOffsetByOneRect = pygame.Rect(labelRect.left + 1, labelRect.top + 1, labelRect.width,
                                             labelRect.height)
        surfaceDown.blit(labelSurfaceDown, labelOffsetByOneRect)
        pygame.draw.rect(surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(surfaceDown, DARK_GRAY, (1, h - 2), (1, 1))
        pygame.draw.line(surfaceDown, DARK_GRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw the over button
        surfaceOver = pygame.Surface(size)
        surfaceOver.fill(self.overColor)
        labelSurfaceOver = self.font.render(label, True, self.textColor, self.overColor)
        surfaceOver.blit(labelSurfaceOver, labelRect)
        pygame.draw.rect(surfaceOver, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(surfaceOver, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(surfaceOver, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(surfaceOver, DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(surfaceOver, DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(surfaceOver, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(surfaceOver, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw the disabled button
        surfaceDisabled = pygame.Surface(size)
        surfaceDisabled.fill(DISABLED_GRAY)
        labelSurfaceDisabled = self.font.render(label, True, GRAY, DISABLED_GRAY)
        surfaceDisabled.blit(labelSurfaceDisabled, labelRect)
        pygame.draw.line(surfaceDisabled, GRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(surfaceDisabled, GRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(surfaceDisabled, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(surfaceDisabled, GRAY, (w - 2, 2), (w - 2, h - 2))

        # call the PygWidgetsButton superclass to finish initialization


        super().__init__(window, loc, surfaceUp, surfaceOver, \
                                    surfaceDown, surfaceDisabled, buttonRect, soundOnClick, label, enterToActivate)

## Older way to do the same thing:
##     super(TextButton, self).__init__(window, loc, surfaceUp, surfaceOver, \
##                                     surfaceDown, surfaceDisabled, buttonRect, soundOnClick, label, enterToActivate)


class CustomButton(PygWidgetsButton):
    """
    CustomButton is a class that allows the user to create a button using custom images.
    Each CustomButton has four states:  up, over, down, and disabled.

    The up, down, over, and disabled images must all be the same size.
    Only the up image needs to be specified. If any of the others are left out, 
    they will default to be a copy of the up surface.

    Parameters:
        window - The window to draw the button in
        loc - A tuple specifying the position (upper left corner) for the button to be drawn.
        up - A path to a file with the button's up appearance.
    -- optional parameters:
        down - A path to a file with the button's pushed down appearance.
        over - A path to a file with the button's appearance when the mouse is over it.
        disabled - A path to a file with the button's disabled appearance.
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the button is clicked (defaults to None)
        label - Any label you want to use to identify this button
    """


    def __init__(self, window, loc, up, down=None, over=None, disabled=None, soundOnClick=None, \
                 label=None, enterToActivate=False):
        """ Initialize a CustomButton """

        # Create the button's Surface objects.
        surfaceUp = pygame.image.load(up)

        if down is None:
            surfaceDown = surfaceUp
        else:
            surfaceDown = pygame.image.load(down)

        if over is None:
            surfaceOver = surfaceUp
        else:
            surfaceOver = pygame.image.load(over)

        if disabled is None:
            surfaceDisabled = surfaceUp
        else:
            surfaceDisabled = pygame.image.load(disabled)

        width, height = surfaceUp.get_size()
        buttonRect = pygame.Rect(loc[0], loc[1], width, height)

        if (width, height) == surfaceDown.get_size() \
                == surfaceOver.get_size() == surfaceDisabled.get_size():
            pass  # typical case, sizes all match
        else:
            raise Exception('Custom button files (starting with: ' + up + ') are not all the same size')

        # call the PygWidgetsButton superclass to finish initialization
        super().__init__(window, loc, surfaceUp, surfaceOver,
                                    surfaceDown, surfaceDisabled, buttonRect, soundOnClick, label, enterToActivate)
# Older way to do the same thing:
#    super(CustomButton, self).__init__(window, loc, surfaceUp, surfaceOver,
#                                        surfaceDown, surfaceDisabled, buttonRect, soundOnClick, label, enterToActivate)


#
#
#  CHECKBOX
#
#
class PygWidgetsCheckBox(PygWidget):
    """
    This is the superclass of TextCheckBox and CustomCheckBox (see code below)
    You would never instantiate from this class.
    Instead, instantiate a CheckBox or CustomCheckBox, then use the rest of the methods provided here


    Typical use:
    1) Create a CheckBox.  Your choice between two different types:

    Either a CheckBox (giving a loc (left, top), optionalValue, optionalLabel):

        myCheckBox = pygwidgets.TextButton(window, (500, 430), True, 'Text Label')

        There are many optional parameters, including width and height that have good defaults.

    Or a CustomCheckBox - giving a location tuple - as (left, top) and at least two images:

        myCheckBox = pygwidgets.CustomButton(window, (500, 430), \
                                on='images/CheckBoxOn.png',
                                off='images/CheckBoxDown.png',
                                value=True)

    2) In your big loop, check for the button being clicked by calling its handleEvent method:

        if myCheckBox.handleEvent(event):  # When clicked on to toggle, this returns True
            #  CheckBox was clicked
            #  do whatever you want here
            
    3) At the bottom of your big loop, draw the checkBox:

        myCheckBox.draw()
        
    """

    def __init__(self, window, loc, theRect, \
                 surfaceOn, surfaceOff, surfaceOnDown, surfaceOffDown,\
                 surfaceOnDisabled, surfaceOffDisabled, soundOnClick, value, label):

        if type(self) is PygWidgetsCheckBox:
            raise Exception('You need to instantiate a CheckBox or CustomCheckBox (not PygWidgetsCheckBox directly)')

        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.rect = theRect
        self.surfaceOn = surfaceOn
        self.surfaceOff = surfaceOff
        self.surfaceOnDown = surfaceOnDown
        self.surfaceOffDown = surfaceOffDown
        self.surfaceOnDisabled = surfaceOnDisabled
        self.surfaceOffDisabled = surfaceOffDisabled
        self.soundOnClick = soundOnClick
        # self.value is the most important attribute - contains True or False
        self.value = value

        # used to track the state of the checkBox
        self.buttonDown = False  # is the checkBox currently pushed down?
        self.mouseOverButton = False  # is the mouse currently hovering over the checkBox?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Track clicks.)
        if self.soundOnClick is not None:
            self.playSoundOnClick = True
            if type(self.soundOnClick) is str:  # user specified sound path, load it here
                pygame.mixer.init()
                self.soundOnClick = pygame.mixer.Sound(self.soundOnClick)  # save in same instance variable
        else:
            self.playSoundOnClick = False

        self.mouseIsDown = False



    def handleEvent(self, eventObj):
        """
        This method should be called every time through the main loop.  It handles showing the
        appropriate state of the check box.  When the user clicks down and later up
        on the check box, this method will return True to signal that the user has toggled on it.
        Normally returns False.
        """

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self.visible:
            # The checkBox only cares bout mouse-related events (or no events, if it is invisible)
            return False

        if not self.isEnabled:
            return False

        clicked = False

        if (not self.mouseOverButton) and self.rect.collidepoint(eventObj.pos):
            # if mouse has entered the checkBox:
            self.mouseOverButton = True


        elif self.mouseOverButton and (not self.rect.collidepoint(eventObj.pos)):
            # if mouse has exited the checkBox:
            self.mouseOverButton = False

        if self.rect.collidepoint(eventObj.pos):

            if eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True

        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the checkBox, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        if eventObj.type == MOUSEBUTTONDOWN:
            self.mouseIsDown = True
            
        # mouse up is handled whether or not it was over the checkBox
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            self.mouseIsDown = False
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False

            if doMouseClick:
                self.buttonDown = False
                clicked = True
                
                if self.playSoundOnClick:
                    self.soundOnClick.play()

                # switch state:
                self.value = not self.value

        return clicked

    def draw(self):
        """ Draw the checkbox """
        if not self.visible:
            return

        # Blit the current checkbox's image.

        if self.isEnabled:
            if self.mouseIsDown and self.lastMouseDownOverButton and self.mouseOverButton:
                if self.value:
                    self.window.blit(self.surfaceOnDown, self.loc)
                else:
                    self.window.blit(self.surfaceOffDown, self.loc)
            else:
                if self.value:
                    self.window.blit(self.surfaceOn, self.loc)
                else:
                    self.window.blit(self.surfaceOff, self.loc)


        else:
            if self.value:
                self.window.blit(self.surfaceOnDisabled, self.loc)
            else:
                self.window.blit(self.surfaceOffDisabled, self.loc)


    def getValue(self):    # This is the key method for getting the current value of the checkbox
        """ Returns the alue of the checkbox  (True/False) """
        return self.value

    def setValue(self, trueOrFalse):
        """ Sets a new value for the checkBox to the value passed in """
        self.value = trueOrFalse


class TextCheckBox(PygWidgetsCheckBox):
    """
    TextCheckBox is a class used to build a checkbox with a default appearance.
    Each TextCheckBox has six states:  on, off, onDown, offDown, onDisabled, and offDisabled

    Parameters:
        window - The window to draw the checkbox in
        loc - A tuple specifying the upper left corner to draw the checkbox on the surface
    -- Optional parameters:
        value - True for on, False for off (default is True)
        label - Optional text that appears to the right of the checkBox (default is no label)
        size - Used for both the width and the height (assuming a square box) - (default is 20 pixels)
        edgeColor - The color of the edges of the checkBox. (default is black)
        insideColor = The color of the inside of the checkBox.  (default is white)
        insideDownColor - The background color of down button (default is a light gray)
        textColor - The color of the text label next to the checkbox (default is black)
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the checkbox is clicked (defaults to None)
    """
    DEFAULT_FONT_NAME = None # use pygame default font
    DEFAULT_FONT_SIZE = 20
    PYGWIDGETS_FONT = pygame.font.Font(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)


    def __init__(self, window, loc, label='', value=True, size=16, edgeColor=BLACK, insideColor=WHITE,\
                 insideDownColor=OVER_GRAY, textColor=BLACK, soundOnClick=None):
        """ Initializes a text-based checkbox """

        self.edgeColor = edgeColor
        self.insideColor = insideColor
        self.insideDownColor = insideDownColor
        self.textColor = textColor

        # Create the button's surfaces.

        self.font = TextCheckBox.PYGWIDGETS_FONT
        self.fontHeight = self.font.size('Anything')[1]  # returns a tuple of (width, height)

        if label == '':
            actualWidth = size
            actualHeight = size
            textSurface = None
            textSurfaceGray = None
            textOffset = 0
        else:
            textSurface = self.font.render(label, True, self.textColor)
            textSurfaceGray = self.font.render(label, True, DISABLED_GRAY)
            thisRect = textSurface.get_rect()
            textOffset = size + 4  # to offset from checkbox, where to start the text
            actualWidth = thisRect.width + textOffset

            if size > self.fontHeight:
                actualHeight = size
            else:
                actualHeight = self.fontHeight

        checkBoxRect = pygame.Rect(loc[0], loc[1], actualWidth, actualHeight)

        w = size  # syntactic sugar
        h = size  # syntactic sugar
        boxSize = (actualWidth, actualHeight)

        # draw the On checkBox, with an X across it to show On state
        surfaceOn = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOn, self.insideColor, pygame.Rect(0, 0, w, h), 0)  # fill the box with inside color
        pygame.draw.rect(surfaceOn, BLACK, pygame.Rect(0, 0, w, h), 1)  # black border around everything
        pygame.draw.line(surfaceOn, BLACK, (0, 0), (w - 2, h - 1), 2)
        pygame.draw.line(surfaceOn, BLACK, (0, h), (w - 2, 0), 2)
        if label != '':
            surfaceOn.blit(textSurface, (textOffset, 0))
            surfaceOn = pygame.Surface.convert_alpha(surfaceOn)  # optimizes blitting

        # draw the Off checkBox
        surfaceOff = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOff, self.insideColor, pygame.Rect(0, 0, w, h), 0)  # fill the box with inside color
        pygame.draw.rect(surfaceOff, BLACK, pygame.Rect(0, 0, w, h), 1)  # black border around everything
        if label != '':
            surfaceOff.blit(textSurface, (textOffset, 0))
            surfaceOff = pygame.Surface.convert_alpha(surfaceOff)  # optimizes blitting

        # draw the OnDown checkBox, with an X across it to show On state
        surfaceOnDown = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOnDown, self.insideDownColor, pygame.Rect(0, 0, w, h), 0)
        # fill the box with inside color
        pygame.draw.rect(surfaceOnDown, BLACK, pygame.Rect(0, 0, w, h), 1)  # black border around everything
        pygame.draw.line(surfaceOnDown, BLACK, (0, 0), (w - 2, h - 1), 2)
        pygame.draw.line(surfaceOnDown, BLACK, (0, h), (w - 2, 0), 2)
        if label != '':
            surfaceOnDown.blit(textSurface, (textOffset, 0))
            surfaceOnDown = pygame.Surface.convert_alpha(surfaceOnDown)  # optimizes blitting

        # draw the OffDown checkBox
        surfaceOffDown = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOffDown, self.insideDownColor, pygame.Rect(0, 0, w, h), 0)
        pygame.draw.rect(surfaceOffDown, BLACK, pygame.Rect(0, 0, w, h), 1)  # black border around everything
        if label != '':
            surfaceOffDown.blit(textSurface, (textOffset, 0))
            surfaceOffDown = pygame.Surface.convert_alpha(surfaceOffDown)  # optimizes blitting

        # draw the OnDisabled checkBox, with an X across it to show On state
        surfaceOnDisabled = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOnDisabled, DISABLED_GRAY, pygame.Rect(0, 0, w, h),
                         0)  # fill the box with disabled color
        pygame.draw.rect(surfaceOnDisabled, DISABLED_GRAY, pygame.Rect(0, 0, w, h), 1)  # black border around everything
        pygame.draw.line(surfaceOnDisabled, BLACK, (0, 0), (w - 2, h - 1), 2)
        pygame.draw.line(surfaceOnDisabled, BLACK, (0, h), (w - 2, 0), 2)
        if label != '':
            surfaceOnDisabled.blit(textSurfaceGray, (textOffset, 0))
            surfaceOnDisabled = pygame.Surface.convert_alpha(surfaceOnDisabled)  # optimizes blitting

        # draw the OffDisabled checkBox
        surfaceOffDisabled = pygame.Surface(boxSize, pygame.SRCALPHA, 32)
        pygame.draw.rect(surfaceOffDisabled, DISABLED_GRAY, pygame.Rect(0, 0, w, h),
                         0)  # fill the box with disabled color
        pygame.draw.rect(surfaceOffDisabled, DISABLED_GRAY, pygame.Rect(0, 0, w, h),
                         1)  # black border around everything
        if label != '':
            surfaceOffDisabled.blit(textSurfaceGray, (textOffset, 0))
            surfaceOffDisabled = pygame.Surface.convert_alpha(surfaceOffDisabled)  # optimizes blitting

        super().__init__(window, loc, checkBoxRect, \
                                             surfaceOn, surfaceOff, \
                                             surfaceOnDown, surfaceOffDown, \
                                             surfaceOnDisabled, surfaceOffDisabled, \
                                             soundOnClick, value, label)


class CustomCheckBox(PygWidgetsCheckBox):
    """
    CustomCheckBox is a class that allows the user to specify their own images for a checkBox.
    Each CustomCheckBox has six states:  on, off, onDown, offDown, onDisabled, offDisabled

    Only the on and off states need to be specified.
    If left out, the others will default to be a copy of the on and off images.

    Parameters:
        window - the window to draw the checkbox in
        loc - A tuple specifying the position (upper left corner) for where the checkBox should be drawn.
        on - A path to a file with the checkBox's on appearance.
        off - A path to a file with the checkBox's off appearance.
    -- Optional parameters:
        onDown - A path to a file with the checkBox's appearance when the user has clicked on the on image.
        offDown - A path to a file with the checkBox's appearandce when the user has clicked on the off image.
        onDisabled - A path to a file with the checkBox's on appearance when not clickable.
        offDisabled - A path to a file with the checkBox's of appearance not clickable.
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the button is clicked (defaults to None)
        label - Any label you want to use to identify this button

    """


    def __init__(self, window, loc, on, off, value=False, \
                 onDown=None, offDown=None, onDisabled=None, offDisabled=None, soundOnClick=None, label=None):
        """ Initialize a CustomCheckBox """

        surfaceOn = pygame.image.load(on)
        surfaceOff = pygame.image.load(off)

        if onDown is None:
            surfaceOnDown = surfaceOn
        else:
            surfaceOnDown = pygame.image.load(onDown)

        if offDown is None:
            surfaceOffDown = surfaceOff
        else:
            surfaceOffDown = pygame.image.load(offDown)

        if onDisabled is None:
            surfaceOnDisabled = surfaceOn
        else:
            surfaceOnDisabled = pygame.image.load(onDisabled)

        if offDisabled is None:
            surfaceOffDisabled = surfaceOff
        else:
            surfaceOffDisabled = pygame.image.load(offDisabled)


        width, height = surfaceOn.get_size()
        checkBoxRect = pygame.Rect(loc[0], loc[1], width, height)

        # call the PygWidgetsCheckBox superclass to initialize
        super().__init__(window, loc, checkBoxRect, \
                                             surfaceOn, surfaceOff, \
                                             surfaceOnDown, surfaceOffDown, \
                                             surfaceOnDisabled, surfaceOffDisabled, \
                                             soundOnClick, value, label)




#
#
# RADIOBUTTON
#
#
class PygWidgetsRadioButton(PygWidget):
    #  The following is a class variable (dict) is used to keep track of all groups of RadioButtons.
    #  Each group has a group name (used as a key), and a list of radioButton objects (as the value).
    #  This makes it easy to send a "turn yourself off" message to all members of a group,
    #     before turning on the selected button.  It also makes it easy to find the currently
    #     selected radioButton, when it is requested.
    __PygWidgets__Radio__Buttons__Groups__Dicts__ = {}


    def __init__(self, window, loc, group, label, buttonRect, \
                 on, off, onDown, offDown, onDisabled, offDisabled, soundOnClick, value):
        if type(self) is PygWidgetsRadioButton:
            raise Exception('You need to instantiate a TextRadioButton or CustomRadioButton' + \
                            ' (not PygWidgetsRadioButton directly)')

        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.group = group
        self.rect = buttonRect
        self.surfaceOn = on
        self.surfaceOff = off
        self.surfaceOnDown = onDown
        self.surfaceOffDown = offDown
        self.surfaceOnDisabled = onDisabled
        self.surfaceOffDisabled = offDisabled
        self.soundOnClick = soundOnClick
        self.value = value
        self.obj = self   # save a reference to ourselves

        # used to track the state of the radioButton
        self.buttonDown = False # is the radioButton currently pushed down?
        self.mouseOverButton = False # is the mouse currently hovering over the radioButton?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Track clicks.)
        if self.soundOnClick is not None:
            self.playSoundOnClick = True
            if type(self.soundOnClick) is str:  # user specified sound path, load it here
                pygame.mixer.init()
                self.soundOnClick = pygame.mixer.Sound(self.soundOnClick)  # save in same instance variable
        else:
            self.playSoundOnClick = False

        self.mouseIsDown = False

        if self.group in PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__:
            # find the group
            thisGroupList = PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group]
            thisGroupList.append(self.obj)  # add this radio button object to the group
            #  Testing: print 'GroupList', self.group, 'is;', thisGroupList

        else:  # new group, not seen before
            # Add a new group, and set the value to a list of the first object
            PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group] = [self.obj]



    def handleEvent(self, eventObj):
        """
        This method should be called every time through the main loop.  It handles showing the
        appropriate state of the radio button.  When the user clicks down and later up
        on the radio button, this method will return True to signal that the user has selected it.
        Normally returns False.        
        """

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self.visible:
            # The radioButton only cares bout mouse-related events (or no events, if it is invisible)
            return False

        if not self.isEnabled:
            return False

        clicked = False

        if (not self.mouseOverButton) and self.rect.collidepoint(eventObj.pos):
            # if mouse has entered the radioButton:
            self.mouseOverButton = True

        elif self.mouseOverButton and (not self.rect.collidepoint(eventObj.pos)):
            # if mouse has exited the radioButton:
            self.mouseOverButton = False

        if self.rect.collidepoint(eventObj.pos):

            if eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True

        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the radioButton, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        if eventObj.type == MOUSEBUTTONDOWN:
            self.mouseIsDown = True
            
        # mouse up is handled whether or not it was over the radioButton
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            self.mouseIsDown = False
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False

            if doMouseClick:
                self.buttonDown = False
                clicked = True

                # Turn all radio buttons in this group off
                for radioButton in PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group]:
                    radioButton.setValue(False)
                self.setValue(True)   # And turn the current one (the one that was clicked) on
                
                if self.playSoundOnClick:
                    self.soundOnClick.play()

        return clicked

    def getSelectedLabel(self):  # returns the label of the currently selected radio button
        radioButtonListInGroup = PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group]
        for radioButton in radioButtonListInGroup:
            if radioButton.getValue():
                selectedLabel = radioButton.getLabel()
                return selectedLabel

        raise Exception('No radio button was selected')

    def draw(self):
        if not self.visible:
            return

        # Blit the radioButton's appropriate appearance
        if self.isEnabled:
            if self.mouseIsDown and self.lastMouseDownOverButton and self.mouseOverButton:
                if self.value:
                    self.window.blit(self.surfaceOnDown, self.loc)
                else:
                    self.window.blit(self.surfaceOffDown, self.loc)
            else:
                if self.value:
                    self.window.blit(self.surfaceOn, self.loc)
                else:
                    self.window.blit(self.surfaceOff, self.loc)

        else:  # show disabled state
            if self.value:
                self.window.blit(self.surfaceOnDisabled, self.loc)
            else:
                self.window.blit(self.surfaceOffDisabled, self.loc)


    def enable(self, allInGroup=False):
        super().enable()
        if allInGroup:
            self.enableGroup()

    def enableGroup(self):
        radioButtonListInGroup = PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group]
        for radioButton in radioButtonListInGroup:
            radioButton.enable()  # enable all in this group

    def disable(self, allInGroup=False):
        super().disable()
        if allInGroup:
            self.disableGroup()  # disable all in this group

    def disableGroup(self):
        radioButtonListInGroup = PygWidgetsRadioButton.__PygWidgets__Radio__Buttons__Groups__Dicts__[self.group]
        for radioButton in radioButtonListInGroup:
            radioButton.disable()  # not recursive

    def setValue(self, trueOrFalse):
        self.value = trueOrFalse

    def getValue(self):
        return self.value





class TextRadioButton(PygWidgetsRadioButton):
    """
    TextRadioButton is a class that allows the user to create a default-styled a radio button.
    Each RadioButton has six states:  on, off, onDown, offDown, onDisabled, offDisabled

    Parameters:
        window - the window to draw the radio button in
        loc - A tuple specifying the position (upper left corner) for where the radioButton should be drawn.
        label - A label, which is returned when querying (see getLabel and getSelectedLabel)
        group - A name for the group that this radio button belongs to 
                (all radio buttons in the group need to use the same group name)
    -- Optional parameters:
        value - True for on, False for Off  (defaults to False)
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the button is clicked (defaults to None)
    """
    DEFAULT_FONT_NAME = None # use pygame default font
    DEFAULT_FONT_SIZE = 20
    PYGWIDGETS_FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
    CIRCLE_DIAMETER = 14
    CIRCLE_LINE_WIDTH = 2
    TEXT_OFFSET = 18

    def __init__(self, window, loc, label, group, value=False, soundOnClick=None):
        # Initialize the TextRadioButton
        # Create the button's images.

        radius = TextRadioButton.CIRCLE_DIAMETER // 2
        center = TextRadioButton.CIRCLE_DIAMETER // 2

        # set up to draw the different states of the radioButton
        self.font = TextRadioButton.PYGWIDGETS_FONT
        self.fontHeight = self.font.size('Anything')[1]   # returns a tuple of (width, height)

        lineSurfaceBlack = self.font.render(label, True, BLACK)
        lineSurfaceGray = self.font.render(label, True, DISABLED_GRAY)
        thisRect = lineSurfaceBlack.get_rect()
        actualWidth = thisRect.width + TextRadioButton.TEXT_OFFSET

        if TextRadioButton.CIRCLE_DIAMETER > self.fontHeight:
            actualHeight = TextRadioButton.CIRCLE_DIAMETER
        else:
            actualHeight = self.fontHeight
        thisRect = pygame.Rect(loc[0], loc[1], actualWidth, actualHeight)

        # For each state of the button, create one larger surface, then blit the circle and the text
        # Special flags are needed to set the background alpha as transparent

        # draw the On TextRadioButton
        surfaceOn = pygame.Surface((actualWidth, actualHeight), pygame.SRCALPHA, 32)
        pygame.draw.circle(surfaceOn, WHITE, (center, center), radius, 0)
        pygame.draw.circle(surfaceOn, BLACK, (center, center), radius, TextRadioButton.CIRCLE_LINE_WIDTH)
        pygame.draw.circle(surfaceOn, BLACK, (center, center), 3, 0)
        surfaceOn.blit(lineSurfaceBlack, (TextRadioButton.TEXT_OFFSET, 0))
        surfaceOn = pygame.Surface.convert_alpha(surfaceOn)  # optimizes blitting

        # draw the Off TextRadioButton
        surfaceOff = pygame.Surface((actualWidth, actualHeight), pygame.SRCALPHA, 32)
        pygame.draw.circle(surfaceOff, WHITE, (center, center), radius, 0)
        pygame.draw.circle(surfaceOff, BLACK, (center, center), radius, TextRadioButton.CIRCLE_LINE_WIDTH)
        surfaceOff.blit(lineSurfaceBlack, (TextRadioButton.TEXT_OFFSET, 0))
        surfaceOff = pygame.Surface.convert_alpha(surfaceOff)  # optimizes blitting

        # draw the onDown and offDown surfaces
        surfaceOnDown = pygame.Surface((actualWidth, actualHeight), pygame.SRCALPHA, 32)
        pygame.draw.circle(surfaceOnDown, GRAY, (center, center), radius, 0)
        pygame.draw.circle(surfaceOnDown, BLACK, (center, center), radius, TextRadioButton.CIRCLE_LINE_WIDTH)
        surfaceOnDown.blit(lineSurfaceBlack, (TextRadioButton.TEXT_OFFSET, 0))
        surfaceOnDown = pygame.Surface.convert_alpha(surfaceOnDown)  # optimizes blitting
        surfaceOffDown = surfaceOnDown   # Copy the same surface as the onDown state

        # draw the OnDisabled radioButton
        surfaceOnDisabled = pygame.Surface((actualWidth, actualHeight), pygame.SRCALPHA, 32)
        pygame.draw.circle(surfaceOnDisabled, DISABLED_GRAY, (center, center), radius, TextRadioButton.CIRCLE_LINE_WIDTH)
        pygame.draw.circle(surfaceOnDisabled, DISABLED_GRAY, (center, center), 3, 0)
        surfaceOnDisabled.blit(lineSurfaceGray, (TextRadioButton.TEXT_OFFSET, 0))
        surfaceOnDisabled = pygame.Surface.convert_alpha(surfaceOnDisabled)  # optimizes blitting

        # draw the OffDisabled radioButton
        surfaceOffDisabled = pygame.Surface((actualWidth, actualHeight), pygame.SRCALPHA, 32)
        pygame.draw.circle(surfaceOffDisabled, DISABLED_GRAY, (center, center), radius, TextRadioButton.CIRCLE_LINE_WIDTH)
        surfaceOffDisabled.blit(lineSurfaceGray, (TextRadioButton.TEXT_OFFSET, 0))
        surfaceOffDisabled = pygame.Surface.convert_alpha(surfaceOffDisabled)  # optimizes blitting

        # call the PygWidgetsRadio superclass to initialize
        super().__init__(window, loc, group, label, thisRect, \
                                          surfaceOn, surfaceOff, \
                                          surfaceOnDown, surfaceOffDown, \
                                          surfaceOnDisabled, surfaceOffDisabled, \
                                          soundOnClick, value)

class CustomRadioButton(PygWidgetsRadioButton):
    """
    CustomRadioButton is a class that allows the user to specify their own images for a radio button.
    Each CustomRadioButton has up to six states:  on, off, onDown, offDown, onDisabled, offDisabled

    Only the on and off states need to be specified.
    If left out, the others will default to copies of the on and off surfaces.

    Parameters:
        window - the window to draw the radio button in
        loc - A tuple specifying the position (upper left corner) for where the radioButton should be drawn.
        label - a label, which is returned when querying (see getLabel and getSelectedLabel)
        group - a name for the group that this radio button belongs to 
                (all radio buttons in the group need to use the same group name)
        on - A path to a file with the radioButton's on appearance.
        off - A path to a file with the radioButton's off appearance.
    -- Optional parameters:
        value - True for selected, False for not selected (defaults to False)
        onDown - A path to the file with the radioButton's on down appearance. (defaults to copy of on)
        offDown - A path to the file withthe radioButton's off down appearance.(defaults to copy of off)
        onDisabled - A path to a file with the radioButton's on appearance when not clickable. (defaults to copy of on)
        offDisabled - A path to a file with the radioButton's of appearance not clickable. (defaults to copy of off)
        soundOnClick - A path to a sound file or sound that has been loaded.
                    Plays when the button is clicked (defaults to None)
    """

    def __init__(self, window, loc, label, group, on, off, value=False, \
                 onDown=None, offDown=None, onDisabled=None, offDisabled=None, soundOnClick=None):
        # Initialize the CustomRadioButton
        # Set up the image

        surfaceOn = pygame.image.load(on)
        surfaceOff = pygame.image.load(off)

        if onDisabled is None:
            surfaceOnDisabled = surfaceOn
        else:
            surfaceOnDisabled = pygame.image.load(onDisabled)

        if offDisabled is None:
            surfaceOffDisabled = surfaceOff
        else:
            surfaceOffDisabled = pygame.image.load(offDisabled)

        if onDown is None:
            surfaceOnDown = surfaceOn
        else:
            surfaceOnDown = pygame.image.load(onDown)

        if offDown is None:
            surfaceOffDown = surfaceOff
        else:
            surfaceOffDown = pygame.image.load(offDown)

        width, height = surfaceOn.get_size()
        thisRect = pygame.Rect(loc[0], loc[1], width, height)

        # call the PygWidgetsRadio superclass to initialize
        super().__init__(window, loc, group, label, thisRect, \
                                                surfaceOn, surfaceOff, \
                                                surfaceOnDown, surfaceOffDown, \
                                                surfaceOnDisabled, surfaceOffDisabled, \
                                                soundOnClick, value)

#
#
#  DISPLAYTEXT
#
#
class DisplayText(PygWidget):
    """
    DisplayText - Allows the user to create a field for displaying text.

        Inspired by a similar module written by David Clark (da_clark at shaw.ca)
        Changed parameters, defaults, methods to call, etc.
    
    DisplayText typical use:
    
    1) Create a DisplayText field:

    myDisplayText = pygwidgets.DisplayText(myWindow, (100, 200))  # Other optional arguments ...
    
    2) Whenever you want to change the text to be displayed in your field, make this call to the setValue method:

          myDisplayText.setValue('Here is some new text to display')

    3) To show the text field in your window, call the draw method:

           myDisplayText.draw()
           
           
        
    Parameters have reasonable defaults, so you only need to provide a window and a loc
    
    Parameters:
        window - The window of the to draw the text into
        loc - Location of where the text should be drawn
    -- Optional parameters:
        value - Any initial text (defaults to the empty string)
        fontName - Name of font to use (defaults to None)
        fontSize - Size of font to use (defaults to 24)
        width - Width of the input text field (defauls to with of text to draw)
        height - Height of display text field (default to height of text to draw)
        textColor - Color of the text (default to black)
        backgroundColor - Background color of the text (defaults to white)
        justified - 'left', 'center', or 'right' (defaults to 'left')
            Note: If you want center or right justified, you probably want to specify a width value
            (Otherwise, with a single text line, you will not see any difference)
    """
    def __init__(self, window, loc=(0, 0), value='',
                 fontName=None, fontSize=18, width=None, height=None, \
                 textColor=BLACK, backgroundColor=None, justified='left', label=None):

        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.text = None # special trick so that the call to setText below will force the creation of the text image
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.userHeight = height
        self.userWidth = width
        self.justified = justified
        self.textImage = None

        self.fontHeight = self.font.size('Anything')[1]   # returns a tuple of (width, height)
        if (height is None) and (width is None):
            self.useSpecifiedArea = False
        else:
            self.useSpecifiedArea = True
        self.setValue(value) # Set the initial text for drawing


    def setValue(self, newText):  # newer name for setText
        newText = str(newText)  #  attempt to convert to string (might be int or float ...)
        if self.text == newText:
            return  # nothing to change

        self.text = newText  # save the new text

        textLines = self.text.splitlines()
        nLines = len(textLines)
        surfacesList = []  # build up a list of surfaces, one for each line of original text
        actualWidth = 0  # will eventually be set the width of longest line

        for line in textLines:
            lineSurface = self.font.render(line, True, self.textColor)
            surfacesList.append(lineSurface)
            thisRect = lineSurface.get_rect()
            if thisRect.width > actualWidth:
                actualWidth = thisRect.width

        heightOfOneLine = self.fontHeight
        actualHeight = nLines * heightOfOneLine
        self.rect = pygame.Rect(self.loc[0], self.loc[1], actualWidth, actualHeight)

        # Create one larger surface, then blit all line surfaces into it
        # Special flags are needed to set the background alpha as transparent
        self.textImage = pygame.Surface((actualWidth, actualHeight), flags=SRCALPHA)
        if self.backgroundColor is not None:
            self.textImage.fill(self.backgroundColor)

        thisLineTop = 0
        for lineSurface in surfacesList:
            if self.justified == 'left':
                self.textImage.blit(lineSurface, (0, thisLineTop))
            else:
                thisSurfaceWidth = lineSurface.get_rect()[2]  # element 2 is the width
                if self.justified == 'center':
                    theLeft = (actualWidth - thisSurfaceWidth) / 2
                elif self.justified == 'right':  # right justified
                    theLeft = actualWidth - thisSurfaceWidth
                else:
                    raise Exception('Value of justified was: ' + self.justified + '. Must be left, center, or right')
                self.textImage.blit(lineSurface, (theLeft, thisLineTop))
            thisLineTop = thisLineTop + heightOfOneLine


        if self.useSpecifiedArea:
            # Fit the text image into a user specified area, may truncate the text off left, right, or bottom
            textRect = self.textImage.get_rect()
            if self.userWidth is None:
                theWidth = textRect.width
            else:
                theWidth = self.userWidth
            if self.userHeight is None:
                theHeight = textRect.height
            else:
                theHeight = self.userHeight

            # Create a surface that is the size that the user asked for
            userSizedImage = pygame.Surface((theWidth, theHeight), flags=SRCALPHA)
            self.rect = pygame.Rect(self.loc[0], self.loc[1], theWidth, theHeight)
            if self.backgroundColor is not None:
                userSizedImage.fill(self.backgroundColor)

            #  Figure out the appropriate left edge within the userSizedImage
            if self.justified == 'left':
                theLeft = 0
            elif self.justified == 'center':
                theLeft = (theWidth - textRect.width) / 2
            else:  # right justified
                theLeft = theWidth - textRect.width

            # Copy the appropriate part from the text image into the user sized image
            # Then re-name it to the textImage so it can be drawn later
            userSizedImage.blit(self.textImage, (theLeft, 0))
            self.textImage = userSizedImage
            self.textImage = pygame.Surface.convert_alpha(self.textImage)  # optimizes blitting

    def setText(self, newText):  # older name, keeping this for older code that used it
        self.setValue(newText)

    def getValue(self):  # Get the text entered by the user
        return self.text

    def getText(self):  # older name, now, use getValue above
        return self.text

    def getTextImage(self):
        return self.textImage

    def draw(self):
        if not self.visible:
            return

        self.window.blit(self.textImage, self.loc)


#
#
# INPUT TEXT
#
#
class InputText(PygWidget):
    """
    InputText - Allows the user to have a field where they enter text (an editable field).
    
        Heavily inspired by (and code borrowed from) NEAROO (Silas Gyger) Found on GitHub dated: 11/14/2014
        Any number of InputText fields can now be created, and only one will have focus.
        Major rewrite to be object oriented.
        Changed parameters, defaults, the way some keys are handled, repeating keys,
             method names, ability to click on field to set new cursor spot, etc.

    InputText typical use:
    
    1) Create an InputText field:

    myInputText = pygwidgets.InputText(myWindow, (100, 200))  # Other optional arguments ...

    2) In your big while loop, call the 'handleEvent' method of the InputText object(s)
    It will return False most of the time, and will return True when the user presses RETURN or ENTER
    Here is the typical code to use:

          if myInputText.handleEvent(event):
            theText = myInputText.getValue()  # call this method to get the text in the field
            print 'The text of myInputText is: ' + theText

    3) To show the text field in your window, the typical code is to call the draw method:

           myInputText.draw()
           
           
    Parameters have reasonable defaults, so you only need to provide a window and a loc
    
    Parameters:
        window: The window to draw the text field in
        loc: Location of where the text should be drawn 
    -- Optional parameters:
        value: Any initial text (defaults to the empty string)
        fontName: Name of font to use (defaults to None)
        fontSize: Dize of font to use (defaults to 24)
        width: Width of the input text field (defauls to 200 pixels)
        textColor: Color of the text (default to black)
        backgroundColor: Background color of the text (defaults to white)
        focusColor: Color of a rectangle around the text when focused (defaults to black)
        initialFocus: should this field have focus when at the beginning? (defaults to False)
                Note:  Only one field should have focus.  If more than one, all focused fields will get keys
    """
    def __init__(self, window, loc, value='', \
                 fontName=None, fontSize=24, width=200, \
                 textColor=BLACK, backgroundColor=WHITE, focusColor=BLACK, initialFocus=False, label=None):

        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.text = value
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.width = width
        self.focus = initialFocus
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.focusColor = focusColor  # color of focus rectangle arount text

        # Get the height of the field by geting the size of the font
        self.height = self.font.get_height()
        # Set the rect of the text image
        self.imageRect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.height)
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.width, self.height)
        # Set the rect of the focus highlight rectangle (when the text has been clicked on and has focus)
        self.focusedImageRect = pygame.Rect(self.loc[0] - 3, self.loc[1] - 3, self.width + 6, self.height + 6)

        # Cursor related things:
        self.cursorSurface = pygame.Surface((1, self.height))
        self.cursorSurface.fill(self.textColor)
        self.cursorPosition = len(self.text)  # put the cursor at the end of the initial text
        self.cursorVisible = False
        self.cursorSwitchMs = 500 # Blink every half=second
        self.cursorMsCounter = 0
        self.cursorLoc = [self.loc[0], self.loc[1]]   # this is a list because element 0 will change as the user edits
        self.clock = pygame.time.Clock()


        # Create one surface, blit the text into it during updateImage
        # Special flags are needed to set the background alpha as transparent
        self.textImage = pygame.Surface((self.width, self.height), flags=SRCALPHA)

        self.currentKey = None
        self.unicodeOfKey = None
        self.updateImage()  # create the image of the starting text

    def updateImage(self):
        # Fill the background of the image
        if self.backgroundColor is not None:
            self.textImage.fill(self.backgroundColor)

        # Render the text as a single line, and blit it onto the textImage surface
        lineSurface = self.font.render(self.text, True, self.textColor)
        self.textImage.blit(lineSurface, (0, 0))


    def handleEvent(self, event):
        if not self.isEnabled:
            return False

        if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1): # user clicked
            theX, theY = event.pos
            # if self.imageRect.collidepoint(pos):
            if self.imageRect.collidepoint(theX, theY):
                if not self.focus:
                    self.focus = True   # give this field focus
                else:
                    # Field already has focus, must position the cursor where the user clicked
                    nPixelsFromLeft = theX - self.loc[0]
                    nChars = len(self.text)

                    lastCharOffset = self.font.size(self.text)[0]
                    if nPixelsFromLeft >= lastCharOffset:
                        self.cursorPosition = nChars
                    else:
                        for thisCharNum in range(0, nChars):
                            thisCharOffset = self.font.size(self.text[:thisCharNum])[0]
                            if thisCharOffset >= nPixelsFromLeft:
                                self.cursorPosition = thisCharNum  # Found the proper position for the cursor
                                break
                    self.cursorVisible = True # Show the cursor at the click point

            else:
                self.focus = False


        if not self.focus:  # if this field does not have focus, don't do anything
            return False

        keyIsDown = False  # assume False

        if event.type == pygame.KEYDOWN:
            keyIsDown = True
            self.currentKey = event.key  # remember for potential repeating key
            self.unicodeOfKey = event.unicode # remember for potential repeating key

        if event.type == pygame.USEREVENT:
            # This is a special signal to check for a repeating key
            # if the key is still down, repeat it
            keyPressedList = pygame.key.get_pressed()

            if (self.currentKey is not None) and (keyPressedList[self.currentKey]):  # Key is still down
                keyIsDown = True
            else:
                # Key is up
                pygame.time.set_timer(pygame.USEREVENT, 0)  # kill the timer
                return False


        if keyIsDown:
            if self.currentKey in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # User is done typing, return True to signal that text is available (via a call to getValue)
                self.focus = False
                self.currentKey = None
                self.updateImage()
                return True

            keyIsRepeatable = True  # assume it is repeatable unless specifically turned off
            if self.currentKey == pygame.K_DELETE:
                self.text = self.text[:self.cursorPosition] + \
                        self.text[self.cursorPosition + 1:]
                self.updateImage()

            elif self.currentKey == pygame.K_BACKSPACE:  # forward delete key
                self.text = self.text[:max(self.cursorPosition - 1, 0)] + \
                                    self.text[self.cursorPosition:]

                # Subtract one from cursor_pos, but do not go below zero:
                self.cursorPosition = max(self.cursorPosition - 1, 0)
                self.updateImage()

            elif self.currentKey == pygame.K_RIGHT:
                if self.cursorPosition < len(self.text):
                    self.cursorPosition = self.cursorPosition + 1

            elif self.currentKey == pygame.K_LEFT:
                if self.cursorPosition > 0:
                    self.cursorPosition = self.cursorPosition - 1

            elif self.currentKey == pygame.K_END:
                self.cursorPosition = len(self.text)
                keyIsRepeatable = False

            elif self.currentKey == pygame.K_HOME:
                self.cursorPosition = 0
                keyIsRepeatable = False

            elif self.currentKey in [pygame.K_UP, pygame.K_DOWN]:
                return False   # ignore up arrow and down arrow

            else:  # standard key
                # If no special key is pressed, add unicode of key to input_string
                self.text = self.text[:self.cursorPosition] + \
                                    self.unicodeOfKey + \
                                    self.text[self.cursorPosition:]
                self.cursorPosition = self.cursorPosition + len(self.unicodeOfKey)
                self.updateImage()

            if keyIsRepeatable:  # set up userevent to try to repeat key
                pygame.time.set_timer(pygame.USEREVENT, 200)  # wait for a short time before repeating

        return False


    # Draw the input text field on the specified surface
    def draw(self):
        if not self.visible:
            return

        # If this input text has focus, draw an outline around the text image
        if self.focus:
            pygame.draw.rect(self.window, self.focusColor, self.focusedImageRect, 1)
            
        # Blit in the image of text (set earlier in updateImage)
        self.window.blit(self.textImage, self.loc)

        # If this field has focus, see if it is time to blink the cursor
        if self.focus:
            self.cursorMsCounter = self.cursorMsCounter + self.clock.get_time()
            if self.cursorMsCounter >= self.cursorSwitchMs:
                self.cursorMsCounter = self.cursorMsCounter % self.cursorSwitchMs
                self.cursorVisible = not self.cursorVisible
    
            if self.cursorVisible:
                cursorOffset = self.font.size(self.text[:self.cursorPosition])[0]
                if self.cursorPosition > 0: # Try to get between characters
                    cursorOffset = cursorOffset - 1
                if cursorOffset < self.width:  # if the loc is within the text area, draw it
                    self.cursorLoc[0] = self.loc[0] + cursorOffset
                    self.window.blit(self.cursorSurface, self.cursorLoc)
    
            self.clock.tick()


    # Helper methods
    def getValue(self):  # Get the text entered by the user
        return self.text

    def getText(self):  # older name, now, use getValue above
        return self.text

    def setValue(self, newText):  # older name, keeping this for older code that used it
        self.text = newText
        self.cursorPosition = len(self.text)
        self.updateImage()

    def setText(self, newText):
        self.setValue(newText)

    def getTextImage(self):
        return self.textImage

    def clearText(self, keepFocus=False):
        self.text = ''
        self.focus = keepFocus
        self.updateImage()

    # Might want to call this (and getValue above), if there is some button to say user has finished typing
    def removeFocus(self):
        self.focus = False


#
#
# DRAGGER
# 
#
class Dragger(PygWidget):
    """
    Dragger - Allows the user to drag an object around in the window

    Dragger typical use:
    
    1) Create a Dragger:

    myDragger= pygwidgets.Dragger(myWindow, (100, 200), 'images/DragMe.png')  # Other optional arguments ...

    2) In your big while loop, call the 'handleEvent' method of the Dragger object(s)
    It will return False most of the time, and will return True when the user presses lifts up on the mouse
    Here is the typical code to use:

          if myDragger.handleEvent(event):
            print 'Done dragging'  # do whatever you want here

    3) To show the dragger in your window, the typical code is to call the draw method:

           myDragger.draw()

    Parameters:
        window - The window of the application so the draw method can draw into
        loc - Location of where the text should be drawn
        up -  Path to up image
    -- Optional parameters:
        down - Path to down image
        over -  Path to over image
        disabled -  Path to disabled image
        label - Any label you want to use to identify this dragger

    """    
    def __init__(self, window, loc, up, down=None, over=None, disabled=None, label=None):
        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.surfaceUp = pygame.image.load(up)
        if down is None:
            self.surfaceDown = self.surfaceUp
        else:
            self.surfaceDown = pygame.image.load(down)
        if over is None:
            self.surfaceOver = self.surfaceUp
        else:
            self.surfaceOver = pygame.image.load(over)
        if disabled is None:
            self.surfaceDisabled = self.surfaceUp
        else:
            self.surfaceDisabled = pygame.image.load(disabled)

        # figure out the rect of the dragger, (used to see if the mouse is within the dragger)
        self.rect = self.surfaceUp.get_rect()
        self.rect.left = self.loc[0]
        self.rect.top = self.loc[1]
        self.startDraggingX = self.rect.left
        self.startDraggingY = self.rect.top
        self.mouseUpLoc = (0, 0)  # some initial value

        # used to track the state of the dragger
        self.mouseOver = False
        self.isEnabled = True
        self.dragging = False
        self.deltaX = 0
        self.deltaY = 0


    def handleEvent(self, eventObj):
        if not self.isEnabled:
            return False
        # This method will return True if user clicks the button.
        # Normally returns False.

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) :
            # The dragger only cares bout mouse-related events 
            return False

        clicked = False
        if eventObj.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(eventObj.pos):
                self.dragging = True
                self.deltaX = eventObj.pos[0] - self.rect.left
                self.deltaY = eventObj.pos[1] - self.rect.top
                self.startDraggingX = self.rect.left
                self.startDraggingY = self.rect.top

        elif eventObj.type == MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                clicked = True
                self.mouseUpLoc = (eventObj.pos[0], eventObj.pos[1])


        elif eventObj.type == MOUSEMOTION:
            if self.dragging:
                self.rect.left = eventObj.pos[0] - self.deltaX
                self.rect.top = eventObj.pos[1] - self.deltaY
            else:
                self.mouseOver = self.rect.collidepoint(eventObj.pos)

        return clicked

    # Returns the rect of the dragger
    # Could use this to see if the dragger was released over a target
    def getRect(self):
        return self.rect

    def getMouseUpLoc(self):
        return self.mouseUpLoc

    # Resets the loc of the dragger back to the place where dragging started
    # Could be used in a test situation if the incorrect answer was dragged.
    def resetToPreviousLoc(self):
        self.rect.left = self.startDraggingX
        self.rect.top = self.startDraggingY

    def draw(self):
        if not self.visible:
            return

        if self.isEnabled:
        
            # Draw the dragger's current appearance to the window.
            if self.dragging:
                self.window.blit(self.surfaceDown, self.rect)
            else:  # mouse is up
                if self.mouseOver:
                    self.window.blit(self.surfaceOver, self.rect)
                else:
                    self.window.blit(self.surfaceUp, self.rect)
        else:
            self.window.blit(self.surfaceDisabled, self.rect)



#
#
# Image
# 
#
class Image(PygWidget):
    """
    Image - Show an image at a given location. 

    Image typical use:
    
    1) Create an Image object:

    myImage = pygwidgets.Image(myWindow, (100, 200), 'images/SomeImage.png') 

    2) To show the Image in your window, the typical code is to call the draw method:

           myImage.draw()

    Parameters:
        window - The window of the application so the draw method can draw into
        loc - Location of where the text should be drawn
        paht -  Path to  image
    -- Optional parameters:
        label - Any label you want to use to identify this dragger

    """    
    def __init__(self, window, loc, path, label=None):
        super().__init__(label)  # initialize base class
        self.window = window
        self.loc = loc
        self.surface = pygame.image.load(path)
        # get and save out the rect of the image
        self.rect = self.surface.get_rect()

    # Returns the rect of the image
    def getRect(self):
        return self.rect

    def draw(self):
        if not self.visible:
            return

        self.window.blit(self.surface, self.loc)





