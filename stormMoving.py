'''
Everything starts with the GUI at the bottom. Intended use is that you type in a number from 1-60 in the first entry box of the gui, as 
well as the name of a currently streaming Twitch streamer in the next box. Then you click the button 'Open Stream', which will go to the twitch stream
of your choice using a selenium browser. Immediately after, you'll want to click the button 'Detect Storm'. 

At this point, the app will be screenshotting a particular region on the stream every second and passing the screenshot through the very impressive
and much appreciated pytesseract module, which attempts to convert the contents of an image into text. This result, often an empty string but sometimes
the timer on the screen as a string object, is passed into the 'process' function which, if the string variable fits the criteria, will use the 
setTimer function in order to tell the app to speak just before the storm moves. 

Notes:

This is a joke app, so it's not exactly intuitive. On startup, you should enter a time interval and make sure you create the sound file. Otherwise, the app 
will set the clock but there will be no sound file to play. If you set the time interval to, say, 40 seconds, but you've only created sound files for 
10, 20, and 30 seconds, then the timer will attempt to read and speak the sound file 40 seconds before the storm moves but will not find any sound file. 

Also, there are two SCREENSHOT_REGION global variables. The second SCREENSHOT_REGION works on a regular stream from a ps4 in 720p that is being read in 
full screen on my laptop, but on your laptop, and for the streamer you want to warn about the gas, the pixel values are likely slightly different. For this
reason, I've included the 'Coordinates' button, which will print to terminal the current cursor location. You can use these coordinates, plus the pyautogui
documentation for the screenshot_region function in order to set new pixel values for SCREENSHOT_REGION. I've found the SCREENSHOT_REGION I commented out
works from some big streamers.

One last note. This app can be improved quite a bit. The controls are not intuitive. The functionality is limited. I just think selenium and pyautgui, 
plus pytesseract gTTS are some really powerful tools and I wanted some practice. Theoretically, one might use this kind of app to read all kinds of 
information out loud. You could set it to say happy birthday when the clock on your computer hits a certain value.
'''

import pyautogui
import pytesseract
import selenium
from selenium import webdriver
import time
from gtts import gTTS 
import os 
from tkinter import *
import datetime

CLOCK_NEEDS_SET = True
WARNING_TIME = 10

def createSoundFile(time_str):
	global WARNING_TIME
	WARNING_TIME = int(time_str)
	text_str = time_str + " seconds until the circle moves"
	myobj = gTTS(text=text_str, lang='en', slow=False) 
	myobj.save("stormMoving" + time_str + ".mp3")
	print('Saved sound file') 

def setClock(result,time_elapsed):
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	try:
		print('Setting Clock')
		circle = result[1]
		screenshot_time = result[3:-1]
		screenshot_time = screenshot_time.split(':')
		screenshot_time_minutes = float(screenshot_time[0])
		screenshot_time_seconds = float(screenshot_time[1].replace('\n',''))
		screenshot_time_in_seconds = screenshot_time_minutes*60 + screenshot_time_seconds
		time_until_warning = screenshot_time_in_seconds - time_elapsed - WARNING_TIME
		print('Sleeping' + str(time_until_warning))
		time.sleep(time_until_warning-2.0)
		sendMessage()
	except:
		CLOCK_NEEDS_SET = True	
		pass
	
def sendMessage():
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	os.system("mpg321 stormMoving" + str(WARNING_TIME) + ".mp3") 
	time.sleep(WARNING_TIME)
	CLOCK_NEEDS_SET = True
		
def process(result,image,start):
	global CLOCK_NEEDS_SET
	image.save('aTest' + str(datetime.datetime.now()) + '.png')
	if result[0] == '(':
		CLOCK_NEEDS_SET = False   #I can run another process. Another thread. If map detected, store contracts. Take a screenshot. If map detected a second time, set images equal and see if there's a difference
		time_elapsed = time.time() - start
		setClock(result,time_elapsed)
	else:
		pass
		
def openStream(streamer):		
	path = '/home/james/Downloads/chromedriver'
	driver = webdriver.Chrome(path)
	url = 'https://www.twitch.tv/' + streamer
	driver.get(url)
	time.sleep(5)
	pyautogui.click(x=1933, y=1336)

#SCREENSHOT_REGION = (160,680,185,68)
SCREENSHOT_REGION = (186,693,219,63)
def stormDetect():
	global SCREENSHOT_REGION
	while CLOCK_NEEDS_SET:  #need to fix coordinates below
		im = pyautogui.screenshot(region=SCREENSHOT_REGION)#can return bounding box, this can be used to narrow the region
		start = time.time()#I shouldnt screenshot the circle number, maybe just tell if theres very little time left in the current circle
		result = pytesseract.image_to_string(im)
		process(result,im,start)
		time.sleep(1)
	while not CLOCK_NEEDS_SET:
		time.sleep(1)
		pass

def getCoordinates():	
	while True:
		print(pyautogui.position())
		time.sleep(1)
		
def homeReset():
	global CANVAS
	clearCanvas()
	warn = StringVar()
	warn_label = Label(CANVAS, text='Integer Time Warning', font=('bold', 12))
	warn_label.pack()
	warn_entry = Entry(CANVAS, textvariable=warn)
	warn_entry.pack()
	top_btn = Button(CANVAS, text='Sound File',  command=lambda: createSoundFile(warn.get()))
	top_btn.pack()
	streamer = StringVar()
	streamer_label = Label(CANVAS, text='Enter Streamer', font=('bold', 12))
	streamer_label.pack()
	streamer_entry = Entry(CANVAS, textvariable=streamer)
	streamer_entry.pack()
	mid_btn = Button(CANVAS, text='Open Stream', command=lambda: openStream(streamer.get()))
	mid_btn.pack()
	bot_btn = Button(CANVAS, text='Detect Storm', command=lambda: main())
	bot_btn.pack()
	extra_btn = Button(CANVAS, text='Coordinates', command=getCoordinates)
	extra_btn.pack()
	
def clearCanvas():
	global CANVAS
	CANVAS.destroy()
	CANVAS = Canvas(APP)
	CANVAS.pack()
	
def main():
	while True:
		stormDetect()
	
global CANVAS
global APP
APP = Tk()
CANVAS = Canvas(APP)
CANVAS.pack()
APP.title('Storm Detector')
MENUBAR = Menu(APP)
MENUBAR.add_command(label="Home", command=homeReset)
APP.config(menu=MENUBAR)
homeReset()
APP.mainloop()
	
	
	

