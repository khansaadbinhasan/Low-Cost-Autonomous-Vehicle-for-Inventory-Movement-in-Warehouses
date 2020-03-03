/*  
Temperature(*C) Table for ultrasonic sound

	Temp, T(*C)     Speed, v(m/s)

	T < 10  	    331 + 0.6*T
	10 < T < 20     331 + 0.6*T
	20 < T < 30     331 + 0.6*T
	30 < T < 40     331 + 0.6*T
	40 < T < 50     331 + 0.6*T
	Over	        336 + 0.1*T

*/


#include <Servo.h>


Servo servo1;
Servo servo2;


// pin numbers for HC-SR04, 1 is front, 2 is back
#define trigPin1 A0
#define echoPin1 A1

#define trigPin2 A2
#define echoPin2 A3


// pin numbers for Servos, 1 is front, 2 is back
#define servoPin1 5
#define servoPin2 6


// variables

// Defining different directions for the robot
const int forward = 1;
const int backward = 2;
const int left = 3;
const int right = 4;
const int stopped = 0;

// Variables for HC-SR04 sensor
long duration1;
int distance1;
long duration2;
int distance2;

const int v = 331 + 0.6*18;
const int upper_HCSR04_limit = 400;
const int lower_HCSR04_limit = 2;


// Variables for Servo
const int defaultAng = 90;
const int minAng = 0;
const int maxAng = 180;
const int midAng = ( maxAng - minAng ) / 2;

int servoang1 = defaultAng;
int servoang2 = defaultAng;


int i = 0;
int j = 0;



// Variables for deciding
// int decision = stopped;
const int safety_dist = 10;
int forward_movement = 2;
int backward_movement = 2;




void update_distances()
{
	// Clears the trigPin
	digitalWrite(trigPin1, LOW);
	delayMicroseconds(2);

	// Sets the trigPin on HIGH state for 10 micro seconds
	digitalWrite(trigPin1, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin1, LOW);

	// Reads the echoPin, returns the sound wave travel time in microseconds
	duration1 = pulseIn(echoPin1, HIGH);

	// Calculating the distance in cm
	distance1 = duration1*v/(2*10000);

	delayMicroseconds(2);



	// Clears the trigPin
	digitalWrite(trigPin2, LOW);
	delayMicroseconds(2);

	// Sets the trigPin on HIGH state for 10 micro seconds
	digitalWrite(trigPin2, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin2, LOW);

	// Reads the echoPin, returns the sound wave travel time in delayMicroseconds
	duration2 = pulseIn(echoPin2, HIGH);

	// Calculating the distance in cm
	distance2 = duration2*v/(2*10000);



  	// Prints the distance on the Serial Monitor
    
	if( distance1 > upper_HCSR04_limit || distance1 < lower_HCSR04_limit )
	{
	  distance1 = -1;
	  Serial.println("forward distance is out of range.");
	}

	else
	{
	  Serial.print("Forward Distance: ");
	  Serial.print(distance1);
	  Serial.println(" cm");
	}


	if( distance2 > upper_HCSR04_limit || distance2 < lower_HCSR04_limit )
	{
	  distance2 = -1;
	  Serial.println("backward distance is out of range.");
	}

	else
	{   
	  Serial.print("Backward Distance: ");
	  Serial.print(distance2);
	  Serial.println(" cm\n\n");
	}
}

void reset_variables()
{
	int servoang1 = defaultAng;
	int servoang2 = defaultAng;

	int forward_movement = 2;
	int backward_movement = 2;

	update_distances();
}



void setup() 
{
  //HCSR04 pins, 1 is front 2 is back
  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin1, INPUT); // Sets the echoPin as an Input

  pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin2, INPUT); // Sets the echoPin as an Input


  //Servo pins, 1 is front 2 is back
  servo1.attach(servoPin1, minAng, maxAng );
  servo2.attach(servoPin2, minAng, maxAng );

  Serial.begin(9600); // Starts the serial communication
}




void loop() 
{
  update_distances();

  while(j < 10)
  {
    for(i = 0; i < 360; i++)
    {
      servo1.write(i);  // tell servo to go to a particular angle
      servo2.write(i);  // tell servo to go to a particular angle
      delay(100);
    }
    
    while(i--)
    {
      servo1.write(i);  // tell servo to go to a particular angle
      servo2.write(i);  // tell servo to go to a particular angle
      delay(100);
    }  

    j++;
  }

	// delay(100);
}
