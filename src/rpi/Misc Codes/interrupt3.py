import RPi.GPIO as GPIO  
import time
from apscheduler.schedulers.background import BackgroundScheduler



def periodic_exec():
	global counter1
	global counter2
	global counter3
	global counter4

	rotation1 = (counter1 / 20) * 60
	print("Motor Speed1: ", rotation1, " RPM")
	counter1 = 0

	rotation2 = (counter2 / 20) * 60
	print("Motor Speed2: ", rotation2, " RPM")
	counter2 = 0


	rotation3 = (counter3 / 20) * 60
	print("Motor Speed3: ", rotation3, " RPM")
	counter3 = 0


	rotation4 = (counter4 / 20) * 60
	print("Motor Speed4: ", rotation4, " RPM")
	counter4 = 0



# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback1(channel):  
    global counter1 
    counter1 = counter1 + 1

  
def my_callback2(channel):  
    global counter2
    counter2 = counter2 + 1

  
def my_callback3(channel):  
    global counter3
    counter3 = counter3 + 1

def my_callback4(channel):  
    global counter4
    counter4 = counter4 + 1




if __name__ == '__main__':
		
	GPIO.setmode(GPIO.BCM)  

	# GPIO 27, 14, 15, 17 & 18 set up as inputs, pulled up to avoid false detection.  
	# Both ports are wired to connect to GND on button press.  
	# So we'll be setting up falling edge detection for both  
	GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
	GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # correct
	GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # correct

	global counter1
	global counter2
	global counter3
	global counter4


	counter1 = 0
	counter2 = 0
	counter3 = 0
	counter4 = 0

	time1 = time.time()*1000
	time2 = time.time()*1000
	time3 = time.time()*1000
	time4 = time.time()*1000

	# when a RISING edge is detected on port 23, regardless of whatever   
	# else is happening in the program, the function my_callback2 will be run  
	# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
	GPIO.add_event_detect(27, GPIO.RISING, callback=my_callback1, bouncetime=1)  
	GPIO.add_event_detect(14, GPIO.RISING, callback=my_callback2, bouncetime=1)  
	GPIO.add_event_detect(15, GPIO.RISING, callback=my_callback3, bouncetime=1)  
	GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback4, bouncetime=1)  


	sched = BackgroundScheduler()

	# seconds can be replaced with minutes, hours, or days
	sched.add_job(periodic_exec, 'interval', seconds=1)
	sched.start()
	

	while True:
		continue


	sched.shutdown()
	GPIO.cleanup()	