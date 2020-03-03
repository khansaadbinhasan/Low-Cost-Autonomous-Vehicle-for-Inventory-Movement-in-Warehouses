/*  Temperature(*C) Table for ultrasonic sound

Temp, T(*C)     Speed, v(m/s)

T < 10  	    331 + 0.6*T
10 < T < 20     331 + 0.6*T
20 < T < 30     331 + 0.6*T
30 < T < 40     331 + 0.6*T
40 < T < 50     331 + 0.6*T
Over	        336 + 0.1*T

*/


#include <Servo.h>


Servo servo_forward;
Servo servo_backward;


// pin numbers for HC-SR04, 1 is front, 2 is back
#define trigPin_backward A0
#define echoPin_backward A1

#define trigPin_forward A2
#define echoPin_forward A3


#define powerPin 9


// pin numbers for Servos, 1 is front, 2 is back
#define servoPin_forward 5
#define servoPin_backward 6



// variables

// Defining different directions for the robot
const int forward = 1;
const int backward = 2;
// const int left = 3;
// const int right = 4;
// const int stopped = 0;

// Variables for HC-SR04 sensor
long duration_backward;
int distance_backward;
long duration_forward;
int distance_forward;


const int v = 331 + 0.6*18;
const int upper_HCSR04_limit = 400;
const int lower_HCSR04_limit = 2;


// Variables for Servo
const int defaultAng = 90;
const int minAng = 0;
const int maxAng = 180;
const int midAng = ( maxAng - minAng ) / 2;

int servoang_front = defaultAng;
int servoang_back = defaultAng;


int i = 0;
int j = 0;


void setup() 
{
  //HCSR04 pins, 1 is front 2 is back
  pinMode(trigPin_backward, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin_backward, INPUT); // Sets the echoPin as an Input

  pinMode(trigPin_forward, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin_forward, INPUT); // Sets the echoPin as an Input


  pinMode(powerPin, OUTPUT); // Sets the echoPin as an Input


  //Servo pins, 1 is front 2 is back
  servo_forward.attach(servoPin_forward, minAng, maxAng );
  servo_backward.attach(servoPin_backward, minAng, maxAng );

  Serial.begin(115200); // Starts the serial communication

}



void update_distances()
{
	// Clears the trigPin
	digitalWrite(trigPin_backward, LOW);
	delayMicroseconds(2);

	// Sets the trigPin on HIGH state for 10 micro seconds
	digitalWrite(trigPin_backward, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin_backward, LOW);

	// Reads the echoPin, returns the sound wave travel time in microseconds
	duration_backward = pulseIn(echoPin_backward, HIGH);

	// Calculating the distance in cm
	distance_backward = duration_backward*v/(2*10000);

	delayMicroseconds(2);



	// Clears the trigPin
	digitalWrite(trigPin_forward, LOW);
	delayMicroseconds(2);

	// Sets the trigPin on HIGH state for 10 micro seconds
	digitalWrite(trigPin_forward, HIGH);
	delayMicroseconds(10);
	digitalWrite(trigPin_forward, LOW);

	// Reads the echoPin, returns the sound wave travel time in delayMicroseconds
	duration_forward = pulseIn(echoPin_forward, HIGH);

	// Calculating the distance in cm
	distance_forward = duration_forward*v/(2*10000);




  	// Prints the distance on the Serial Monitor
	if( distance_backward > upper_HCSR04_limit || distance_backward < lower_HCSR04_limit )
	{
		distance_backward = -1;
		Serial.println("backward distance is out of range.");
		Serial.print(distance_backward);

	}

	else
	{
		Serial.print("Backward Distance: ");
		Serial.print(distance_backward);
		Serial.println(" cm");
	}


	if( distance_forward > upper_HCSR04_limit || distance_forward < lower_HCSR04_limit )
	{
		distance_forward = -1;
		Serial.println("forward distance is out of range.");
		Serial.print(distance_forward);

	}

	else
	{   
		Serial.print("Forward Distance: ");
		Serial.print(distance_forward);
		Serial.println(" cm\n\n");

	}
}

void reset_variables()
{
	int servoang_front = defaultAng;
	int servoang_back = defaultAng;

	// int forward_movement = 2;
	// int backward_movement = 2;

	update_distances();
}


void rotate_servo_left(int servo_num)
{
	if( servo_num == 1 )
	{
		servo_forward.write(midAng);

		for(i = midAng; i < maxAng; i++)
		{
			servo_forward.write(i);  // tell servo to go to a particular angle
			update_distances();
			delay(10);
		}
	}	


	if( servo_num == 2 )
	{
		servo_backward.write(midAng);

		for(i = midAng; i < maxAng; i++)
		{
			servo_backward.write(i);  // tell servo to go to a particular angle
			update_distances();
			delay(10);
		}

	}	
}

void rotate_servo_right(int servo_num)
{
	if( servo_num == 1 )
	{
		servo_forward.write(midAng);

		for(i = midAng; i > minAng; i--)
		{
			servo_forward.write(i);  // tell servo to go to a particular angle
			update_distances();
			delay(10);
		}
	}	


	if( servo_num == 2 )
	{
		servo_backward.write(midAng);

		for(i = midAng; i > minAng; i--)
		{
			servo_backward.write(i);  // tell servo to go to a particular angle
			update_distances();
			delay(10);
		}

	}	
}


void loop() 
{
	digitalWrite(powerPin, HIGH);
	update_distances();

	for(j = 0; j < 2; j++)
	{
		rotate_servo_right(forward);
		rotate_servo_left(backward);

		rotate_servo_left(2);
		rotate_servo_right(2);
	}

	delay(100);

}
