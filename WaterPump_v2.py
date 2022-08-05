# v1: Water Pump on schedule with switch can top up water
# v2: Water detector: when water run low, stop water pump and red LED on as warning
import RPi.GPIO as GPIO
import time
import schedule
from datetime import datetime

# Pin definition
PUMP_PIN=11
SWITCH_PIN=13
WATERDETECTOR_PIN=15
LED_PIN=16
Switch_On=False
LED_On=False
Start_Time=0
End_Time=0

# Use Pin number
GPIO.setmode(GPIO.BOARD)
# Set Pin 11 as output(supply 3.3v power)
GPIO.setup(PUMP_PIN, GPIO.OUT)
# Set Pin 13 as input
GPIO.setup(SWITCH_PIN, GPIO.IN)
# Set pin 15 as input
GPIO.setup(WATERDETECTOR_PIN, GPIO.IN)
# set pin 16 as output
GPIO.setup(LED_PIN, GPIO.OUT)


def PumpWater(duration=0):
	print("Start watering...")
	GPIO.output(PUMP_PIN,GPIO.HIGH)
	if duration>0:
		print("Continue...")
		time.sleep(duration)

def StopWater(duration=0):
	print("Stop watering...")
	GPIO.output(PUMP_PIN,GPIO.LOW)
	if duration>0:
		print("Continue...")
		time.sleep(duration)

def ScheduledPump():
	print("Scheduled Task...")
	ScheduleStart=datetime.now()
	PumpWater(5)
	StopWater(0)
	ScheduleEnd=datetime.now()
	# Log
	WriteToCSV(ScheduleStart, ScheduleEnd, "Scheduled")

def WriteToCSV(st, et, type):
	with open('WaterPumpLog.csv', mode='a') as f:
		f.write("{},{},{}".format(st.strftime("%d/%m/%Y %H:%M:%S"),et.strftime("%d/%m/%Y %H:%M:%S"),type))
		f.write("\n")

def FlashLED():
	global LED_On
	LED_On=True
	# Flash LED
	GPIO.output(LED_PIN,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(LED_PIN,GPIO.LOW)
	time.sleep(1)
	
def TurnOffLED():
	global LED_On
	LED_On=False
	GPIO.output(LED_PIN,GPIO.LOW)


#schedule.every().minute.at(":10").do(ScheduledPump)
schedule.every().day.at("09:00").do(ScheduledPump)

while True:
	# Run scheduled task
	#schedule.run_pending()
	# Button override: False switch on water, True on schedule 
	Switch_Value=GPIO.input(SWITCH_PIN)
	# Water detector: False enough water, True not enough water
	WaterDetector_Value=GPIO.input(WATERDETECTOR_PIN)
	# Enough water and switch on water
	if WaterDetector_Value==False and Switch_Value==False:
		# Switch off LED if needed
		if LED_On==True:
			print("Water level ok...")
			TurnOffLED()
		else:
			print("Switch on")
		Switch_On=True
		Start_Time=datetime.now()
		# Pump water until switched off
		PumpWater(0)
		while WaterDetector_Value==False and Switch_Value==False:
			Switch_Value=GPIO.input(SWITCH_PIN)
			WaterDetector_Value=GPIO.input(WATERDETECTOR_PIN)
			time.sleep(0.1)
	# Enough water and on schedule
	elif WaterDetector_Value==False and Switch_Value==True:
		# Switch off LED if needed
		if LED_On==True:
			print("Water level ok...")
			TurnOffLED()
		else:
			print("Switch off")
		if Switch_On==True:
			Switch_On=False
			StopWater(0)
			End_Time=datetime.now()
			WriteToCSV(Start_Time, End_Time, "Switch")
		#schedule.run_pending()
		while WaterDetector_Value==False and Switch_Value==True:
			Switch_Value=GPIO.input(SWITCH_PIN)
			WaterDetector_Value=GPIO.input(WATERDETECTOR_PIN)		
			schedule.run_pending()
	# Not enough water
	else:
		# Running out water
		print("Running out of  water...")
		#  Switch off water
		if Switch_On==True:
			Switch_On=False
			StopWater(0)
			End_Time=datetime.now()
			WriteToCSV(Start_Time, End_Time, "Switch")
		#Switch on LED
		FlashLED()
		while WaterDetector_Value==True:
			FlashLED()
			WaterDetector_Value=GPIO.input(WATERDETECTOR_PIN)
