# OCR-Pyautogui-Detect-Storm-Movement-COD-Warzone-TTS
This is a simple app that lets you type in a streamer's name (your own stream) and then your computer will warn you out loud when the storm in COD Warzone is about to move. Could save your virtual life

There are a few dependencies. On Ubuntu 21.04, I did:
```
pip3 install pytesseract
pip3 install selenium
pip3 install gTTs
pip3 install pyautogui
pip3 install pynput
```
#From there, you can run the script from the terminal. A window will appear with several functions including:
* Setting an integer time warning - input 10 seconds and you will be warned with text to speech 10 seconds before the circle moves
* Entering a Twitch streamer's name. Storm detector will then attempt to open that Twitch streamer's live stream
* Checking coordinates of the mouse cursor
* Setting the region of the screen for the storm detector to screenshot repeatedly, checking for the timer - set the region to a small box just around the storm timer on the left side of the screen and the storm detector will repeatedly screenshot that section and warn you when the timer is getting low
* Hit 'Detect Storm' and the Storm Detector, given the proper coordinates, will warn you throughout the match of when the circle is going to move. 

