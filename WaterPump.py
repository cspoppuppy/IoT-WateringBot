import RPi.GPIO as GPIO
import time
import schedule
from datetime import datetime

PUMP_PIN=11
SWITCH_PIN=13
Switch_On=False
Start_Time=0
End_Time=0

# Use Pin number
GPIO.setmode(GPIO.BOARD)
# Set Pin 11 as output(supply 3.3v power)
GPIO.setup(PUMP_PIN, GPIO.OUT)
# Set Pin 13 as input
GPIO.setup(SWITCH_PIN, GPIO.IN)

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

schedule.every().day.at("09:00").do(ScheduledPump)

while True:
	# Run scheduled task
	#schedule.run_pending()
	# Button override
	input_value=GPIO.input(SWITCH_PIN)
	if input_value==False:
		print("Switch on")
		Switch_On=True
		Start_Time=datetime.now()
		# Pump water until switched off
		PumpWater(0)
		while input_value==False:
			input_value=GPIO.input(SWITCH_PIN)
			time.sleep(0.1)
	else:
		print("Switch off")
		if Switch_On==True:
			Switch_On=False
			StopWater(0)
			End_Time=datetime.now()
			WriteToCSV(Start_Time, End_Time, "Switch")
		#schedule.run_pending()
		while input_value==True:
			input_value=GPIO.input(SWITCH_PIN)		
			schedule.run_pending()
