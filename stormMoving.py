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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
