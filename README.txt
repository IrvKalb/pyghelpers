#pyghelpers  (pronounced as: "pig helpers")

An open collection of classes and functions for use with pygame development.

Version 1.1
6/23
    Big change to startup:
       The main program should now create a dictionary of sceneKey: sceneObject pairs
           and get pass this in when creating the SceneMgr.
       This eliminates the earlier need for each scene to have a getSceneKey() method.
       (The old approach is still supported for backward compatibility)
    Added addScene to add a scene dynamically (pass in a sceneKey and sceneObject)
    Added removeScene to remove an existing scene to free up memory (pass in a sceneKey)
       (This can be called from the current scene, as long as the next line is a gotoScene)
2/23
    Added code in all timers to check for and handle multiple pauses and resumes.
    In CountDownTimer made ended() method check the time
       Client code doesn't need to call getTime()   Suggested by Lando Chan
    In CountUpTimer and CountDown timer added forceFullHHMMSS for full HH:MM:SS presentation
10/22
   SceneMgr:  Added optional frame rate display for debugging
4/22
    Timer, CountUpTimer, CountDownTimer: Added pause() and resume()
    

To install, open the command line and enter the following:

  python3 -m pip install -U pip --user
  
  python3 -m pip install -U pyghelpers --user
  
The first command ensures that you have the latest version of pip (the installer).
The second line installs the latest version of pyghelpers from PyPI into the
site-packages folder on your computer, so that this package is available to all
of your Python programs.

Documentation can be found at:  https://pyghelpers.readthedocs.io/en/latest/


If you have questions or are interested in making additions, please contact me:  

Irv at furrypants.com