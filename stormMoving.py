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



CLOCK_NEEDS_SET = True
WARNING_TIME = 10
CLOCK_PIXELS = ['na','na']
RESULT_CACHE = ''

def customSoundFile(text_str): 
	myobj = gTTS(text=text_str, lang='en', slow=False) 
	myobj.save("customSound.mp3")
	
#customSoundFile('Player died')
	
def checkInt(int_str):
	try:
		x = int(int_str)
		return True
	except:
		return False
		
def playerCountDetect(flag):
	while True:
		playerCountDetectProcess()
	
def playerCountDetectProcess():
	global RESULT_CACHE
	im = pyautogui.screenshot(region=SCREENSHOT_REGION)
	result = pytesseract.image_to_string(im)
	if checkInt(result):
		if RESULT_CACHE != '':
			if result != RESULT_CACHE:
				os.system("mpg321 customSound.mp3") 
				RESULT_CACHE = result
				print('updated result cache')
		elif RESULT_CACHE == '':
			RESULT_CACHE = result
			print('first result cached')
	else:
		print('Result not a number')

def createSoundFile(time_str):
	text_str = time_str + " seconds until the circle moves"
	myobj = gTTS(text=text_str, lang='en', slow=False) 
	myobj.save("stormMoving" + time_str + ".mp3")
	print('Saved sound file') 
	
def setWarning(time_str):
	global WARNING_TIME
	WARNING_TIME = int(time_str)
	if path.exists("stormMoving" + time_str + ".mp3") :
		print('Warning time set, sound file found')
	else:
		createSoundFile(time_str)
	


def setClock(result,time_elapsed):
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	try:
		print('Setting Clock')
		minutes_seconds = result.split(':')
		screenshot_time_minutes = int(minutes_seconds[0])
		screenshot_time_seconds = int(minutes_seconds[1])
		screenshot_time_in_seconds = screenshot_time_minutes*60 + screenshot_time_seconds
		time_until_warning = screenshot_time_in_seconds - time_elapsed - WARNING_TIME
		print('Sleeping' + str(time_until_warning))
		time.sleep(time_until_warning-2.0)
		sendMessage()
	except:
		CLOCK_NEEDS_SET = True	
		pass
	
def sendMessage():
	print('speaking')
	global CLOCK_NEEDS_SET
	global WARNING_TIME
	os.system("mpg321 stormMoving" + str(WARNING_TIME) + ".mp3") 
	#playsound("stormMoving" + str(WARNING_TIME) + ".mp3") 
	time.sleep(WARNING_TIME)
	CLOCK_NEEDS_SET = True
		
def process(result,image,start):
	global CLOCK_NEEDS_SET
	if result != '':
		CLOCK_NEEDS_SET = False
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

SCREENSHOT_REGION = (159,677,350,350)
def stormDetect():
	global SCREENSHOT_REGION
	while CLOCK_NEEDS_SET:  #need to fix coordinates below
		im = pyautogui.screenshot(region=SCREENSHOT_REGION)#can return bounding box, this can be used to narrow the region
		start = time.time()#I shouldnt screenshot the circle number, maybe just tell if theres very little time left in the current circle
		result = pytesseract.image_to_string(im)
		print(result)
		process(result,im,start)
		time.sleep(1)
	while not CLOCK_NEEDS_SET:
		time.sleep(1)
		pass

def getCoordinates():	
	while True:
		x = pyautogui.position()
		print(x[0])
		print(x[1])
		print(pyautogui.position())
		time.sleep(1)
		
def calcRegion():
	global SCREENSHOT_REGION
	global CLOCK_PIXELS
	top_left = CLOCK_PIXELS[0]
	bottom_right = CLOCK_PIXELS[1]
	left = top_left[0]
	top = top_left[1]
	width = abs(top_left[0] - bottom_right[0])
	height = abs(top_left[1] - bottom_right[1])
	return (left,top,width,height)
	
		
def setRegion(flag):
	global CLOCK_PIXELS
	global SCREENSHOT_REGION
	checkKeys()
	if 'na' not in CLOCK_PIXELS:
		SCREENSHOT_REGION = calcRegion()
		print('Set custom screenshot region: ' + str(SCREENSHOT_REGION))
	else:
		print('Default screenshot region: ' + str(SCREENSHOT_REGION))
		pass
	

def onPress(key):
	global CLOCK_PIXELS
	try:
		if key.char == 'a':
			print('Top Left Set')
			CLOCK_PIXELS[0] = pyautogui.position()
		elif key.char == 'b':
			print('Top Right Set')
			CLOCK_PIXELS[1] = pyautogui.position()
		elif key.char == 'c':
			print('Calculating Region')
			return False
	except:
		print('Invalid Key')
		
def onRelease(key):
	pass

def checkKeys():
	print('Listening')
	with Listener(on_press=onPress,on_release=onRelease) as listener:
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
	mid_btn = Button(CANVAS, text='Open Stream', command=lambda: openStream(streamer.get()))
	mid_btn.pack()
	bot_btn = Button(CANVAS, text='Detect Storm', command=lambda: main())
	bot_btn.pack()
	extra_btn = Button(CANVAS, text='Coordinates', command=getCoordinates)
	extra_btn.pack()
	last_btn = Button(CANVAS, text='Set Region', command= lambda :setRegion(streamer.get()))
	last_btn.pack()
	one_more_btn = Button(CANVAS,text='Detect Count',command=lambda:playerCountDetect(streamer.get()))
	one_more_btn.pack()
	
def clearCanvas():
	global CANVAS
	CANVAS.destroy()
	CANVAS = Canvas(APP)
	CANVAS.pack()
	
	

NEW_GAME = True	
def main():
	global NEW_GAME
	global CLOCK_NEEDS_SET
	CLOCK_NEEDS_SET = True
	while NEW_GAME:
		stormDetect()
	return None
		
		

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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
