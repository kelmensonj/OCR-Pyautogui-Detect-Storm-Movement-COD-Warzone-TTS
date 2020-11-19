import pyautogui
import pytesseract
import selenium
from selenium import webdriver
import time
from gtts import gTTS 
import os 
import os.path
from os import path
from tkinter import *
import datetime
from pynput.keyboard import Key, Listener



SCREENSHOT_REGION = (159,677,350,350) #This is a default screenshot region. Intended us for this app is that you set your own region
CLOCK_NEEDS_SET = True #This will pause the screenshotting whenever a result is found
WARNING_TIME = 10 #This is the default warning time
CLOCK_PIXELS = ['na','na'] #This is just a placeholder, and will be used when you set the screenshot region
RESULT_CACHE = ''

def customSoundFile(text_str): 
	myobj = gTTS(text=text_str, lang='en', slow=False) #here you create a sound file to be played whenever the player count changes
	myobj.save("customSound.mp3")
	
#customSoundFile('Player died') #this should be in the GUI, but really, its just a test. You run this line and create a sound file
	
def checkInt(int_str):
	try:
		x = int(int_str)
		return True #this returns True if a result is an integer
	except:
		return False
		
def playerCountDetect(flag):
	while True:
		playerCountDetectProcess() #loops playerCountDetectProcess(), can be altered to stop the process
	
def playerCountDetectProcess():
	global RESULT_CACHE
	im = pyautogui.screenshot(region=SCREENSHOT_REGION) #so, first, you should set the region to be the few pixels that show player count
	result = pytesseract.image_to_string(im) #then that screenshot is turned into text
	if checkInt(result): #now check if the text from the screenshot is an integer
		if RESULT_CACHE != '': #now check if its not the first integer result found
			if result != RESULT_CACHE: #now check if the integer result is different from the previous integer result we stored
				os.system("mpg321 customSound.mp3") #if the integer results differ, we play an alert
				RESULT_CACHE = result #and cache the new new result
				print('updated result cache')
		elif RESULT_CACHE == '': #else, if we have an empty cache
			RESULT_CACHE = result #no checks are needed and no sound file will be played, we just cache our integer result
			print('first result cached')
	else:
		print('Result not a number') #this is what happens when the text isnt recognized properly

def createSoundFile(time_str):
	text_str = time_str + " seconds until the circle moves"
	myobj = gTTS(text=text_str, lang='en', slow=False) #this uses a text to speech module
	myobj.save("stormMoving" + time_str + ".mp3") #this is where we save our speech
	print('Saved sound file') 
	
def setWarning(time_str):
	global WARNING_TIME
	WARNING_TIME = int(time_str) #from the UI, user inputs a warning time
	if path.exists("stormMoving" + time_str + ".mp3"): #if the file already exists, we don't need to create the file
		print('Warning time set, sound file found')
	else:
		createSoundFile(time_str) #if the file doesn't exist, we need a file. We need a unique sound file for each integer warning time
	
def setClock(result,time_elapsed):
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	try: #we use a try and except here so that if the result from pytesseract doesn't look like a time, we trip the exception
		minutes_seconds = result.split(':') #this splits on the colon
		screenshot_time_minutes = int(minutes_seconds[0]) #the clock is in the format '0:24'
		screenshot_time_seconds = int(minutes_seconds[1])
		screenshot_time_in_seconds = screenshot_time_minutes*60 + screenshot_time_seconds #converting time to seconds
		time_until_warning = screenshot_time_in_seconds - time_elapsed - WARNING_TIME #shifting time based on warning time
		print('Sleeping' + str(time_until_warning))
		time.sleep(time_until_warning-2.0) #now we sleep until its time to send the message
		sendMessage()
	except:
		CLOCK_NEEDS_SET = True	#if there's any exception we go right back to screenshotting the set region and looking for a result that doesnt
		pass			#trip this exception
	
def sendMessage():
	print('speaking')
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	os.system("mpg321 stormMoving" + str(WARNING_TIME) + ".mp3") #theres a bug where the sound file isn't saved as playable mp3, so you might get stuck here
	#playsound("stormMoving" + str(WARNING_TIME) + ".mp3") #but anyway, its the os line where you play the mp3 from the command line
	time.sleep(WARNING_TIME) #now we sleep, successfully warning the player of the circle
	CLOCK_NEEDS_SET = True #now its time to awake and begin checking the clock again
		
def process(result,image,start):
	global CLOCK_NEEDS_SET
	if result != '': #here for speed, often the pytesseract result is this
		CLOCK_NEEDS_SET = False #this pauses the screenshotting process
		time_elapsed = time.time() - start #this is just here for increased accuracy, pytesseract can take some time
		setClock(result,time_elapsed)
	else:
		pass
		
def openStream(streamer):		
	path = '/home/james/Downloads/chromedriver'
	driver = webdriver.Chrome(path)
	url = 'https://www.twitch.tv/' + streamer #this goes with the 'Open Stream' button in the GUI
	driver.get(url) #pretty simple, just uses selenium to open twitch, and then clicks the maximize button
	time.sleep(5)
	pyautogui.click(x=1933, y=1336) #coordinates of maximize button on twitch
	
def stormDetect():
	global SCREENSHOT_REGION
	while CLOCK_NEEDS_SET:  
		im = pyautogui.screenshot(region=SCREENSHOT_REGION) #SCREENSHOT_REGION is either set by user or a default value
		start = time.time() #this is the exact moment we got the screenshot
		result = pytesseract.image_to_string(im) #look at that magic
		print(result)
		process(result,im,start) 
		time.sleep(1)
	while not CLOCK_NEEDS_SET: #stormDetect has something to do when the user has been warned
		time.sleep(1)
		pass

def getCoordinates():	
	while True: #just a debugging tool, this will print coordinates of your cursor
		print(pyautogui.position())
		time.sleep(1)
		
def calcRegion():
	global SCREENSHOT_REGION
	global CLOCK_PIXELS
	top_left = CLOCK_PIXELS[0]
	bottom_right = CLOCK_PIXELS[1]
	left = top_left[0]
	top = top_left[1]
	width = abs(top_left[0] - bottom_right[0]) #this function is just formatting our pixel readings so pyautogui.screenshot() can work
	height = abs(top_left[1] - bottom_right[1])
	return (left,top,width,height)
	
		
def setRegion(flag):
	global CLOCK_PIXELS
	global SCREENSHOT_REGION
	checkKeys() #starts listening for keys, will stop once return True is called in onPress()
	if 'na' not in CLOCK_PIXELS: #this means the user has loaded a value for top left and bottom right bounds
		SCREENSHOT_REGION = calcRegion()
		print('Set custom screenshot region: ' + str(SCREENSHOT_REGION))
	else:
		print('Default screenshot region: ' + str(SCREENSHOT_REGION)) #if there's missing values we just go to default SCREENSHOT_REGION
		pass
	

def onPress(key):
	global CLOCK_PIXELS #what you do is label the screen where the program should screenshot, move your cursor to the bounds and press the keys
	try:
		if key.char == 'a': #a labels the top left corner bounds
			print('Top Left Set')
			CLOCK_PIXELS[0] = pyautogui.position()
		elif key.char == 'b': #b labels the top right corner bounds
			print('Top Right Set')
			CLOCK_PIXELS[1] = pyautogui.position()
		elif key.char == 'c': #c tells the listener to stop
			print('Calculating Region')
			return False
	except:
		print('Invalid Key')
		
def onRelease(key):
	pass

def checkKeys():
	print('Listening')
	with Listener(on_press=onPress,on_release=onRelease) as listener: #standard for pynput Listener, check their docs
		listener.join()
			
def homeReset():
	global CANVAS
	clearCanvas()
	warn = StringVar()
	warn_label = Label(CANVAS, text='Integer Time Warning', font=('bold', 12))
	warn_label.pack()
	warn_entry = Entry(CANVAS, textvariable=warn)
	warn_entry.pack()
	top_btn = Button(CANVAS, text='Set Warning Time',  command=lambda: setWarning(warn.get()))
	top_btn.pack()
	streamer = StringVar()
	streamer_label = Label(CANVAS, text='Enter Streamer', font=('bold', 12))
	streamer_label.pack()
	streamer_entry = Entry(CANVAS, textvariable=streamer)
	streamer_entry.pack()
	mid_btn = Button(CANVAS, text='Open Stream', command=lambda: openStream(streamer.get())) #all basic GUI here
	mid_btn.pack()
	bot_btn = Button(CANVAS, text='Detect Storm', command=lambda: main())
	bot_btn.pack()
	extra_btn = Button(CANVAS, text='Coordinates', command=getCoordinates)
	extra_btn.pack()
	last_btn = Button(CANVAS, text='Set Region', command= lambda :setRegion(streamer.get()))
	last_btn.pack()
	one_more_btn = Button(CANVAS,text='Detect Count',command=lambda:playerCountDetect(streamer.get())) #this goes to an experimental feature
	one_more_btn.pack() #in this feature, the idea is to screenshot in the top right and keep track of player count for various reasons
	
def clearCanvas():
	global CANVAS
	CANVAS.destroy() #just a refresh for GUI
	CANVAS = Canvas(APP)
	CANVAS.pack()
	
NEW_GAME = True	
def main():
	global NEW_GAME
	global CLOCK_NEEDS_SET
	CLOCK_NEEDS_SET = True #feel free to change this i know its bad
	while NEW_GAME:
		stormDetect()
	return None
		
global CANVAS
global APP
APP = Tk()
CANVAS = Canvas(APP)
CANVAS.pack()
APP.title('Storm Detector') #more GUI down here
MENUBAR = Menu(APP)
MENUBAR.add_command(label="Home", command=homeReset)
APP.config(menu=MENUBAR)
homeReset()
APP.mainloop()
	
	

