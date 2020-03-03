/*
  --> Uses A4 and A5 pins of arduino and connects according to /rsc/i2c.jpg
  --> This sketch helps in I2C communication with the raspberry pi, receives command from the pi and sends ACK to it
  --> This sketch runs motors in different directions according to commands received via I2C from rpi.
  --> After setting up the Robot, upload this sketch to arduino.
  --> This can be used to test if remote control is working or not
*/

/*  Temperature(*C) Table for ultrasonic sound

Temp, T(*C)     Speed, v(m/s)

T < 10        331 + 0.6*T
10 < T < 20     331 + 0.6*T
20 < T < 30     331 + 0.6*T
30 < T < 40     331 + 0.6*T
40 < T < 50     331 + 0.6*T
Over          336 + 0.1*T

*/


#include <Servo.h>
#include <Wire.h>

#define SLAVE_ADDRESS 0x04


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

// commands to move the robot in different directions
int STOP = 0;
int UP = 1;
int DOWN = 2;
int RIGHT = 3;
int LEFT = 4;

int cmd = STOP;


// motor driver front
// motor one
int input_front1 = 2;
int input_front2 = 4;


// motor two
int input_front3 = 7;
int input_front4 = 8;


// motor driver 2
// motor three
int input_back3 = 12;
int input_back4 = 13;


// motor four
int input_back1 = 10;
int input_back2 = 11;


// Variables for HC-SR04 sensor
long duration_backward;
int distance_backward;
long duration_forward;
int distance_forward;

int currentTemp = 25;
const int v = 331 + 0.6*currentTemp;
const int upper_HCSR04_limit = 400;
const int lower_HCSR04_limit = 2;


// Variables for Servo
// const int defaultAng = 90;
const int minAng = 0;
const int maxAng = 180;
const int midAng = ( maxAng - minAng ) / 2;

int servoang_front = midAng;
int servoang_back = midAng;

int i = 0;
int j = 0;


// For Backup
int safetyDist = 10;
int robotSafe = 1;
int letRun = 0;
int wireIn = -1;

void setup() 
{
  //Setting up the I2C connections
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);


  //motor drive 1
  // motor 1
  pinMode(input_front1, OUTPUT);
  pinMode(input_front2, OUTPUT);
  
  // motor 2
  pinMode(input_front3, OUTPUT);
  pinMode(input_front4, OUTPUT);


  //motor drive 2
  // motor 3
  pinMode(input_back3, OUTPUT);
  pinMode(input_back4, OUTPUT);
  
  // motor 4
  pinMode(input_back1, OUTPUT);
  pinMode(input_back2, OUTPUT);


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

// void reset_variables()
// {
//   int servoang_front = midAng;
//   int servoang_back = midAng;

//   // int forward_movement = 2;
//   // int backward_movement = 2;

//   update_distances();
// }


// void rotate_servo_left(int servo_num)
// {
//   if( servo_num == 1 )
//   {
//     servo_forward.write(midAng);

//     for(i = midAng; i < maxAng; i++)
//     {
//       servo_forward.write(i);  // tell servo to go to a particular angle
//       update_distances();
//       delay(10);
//     }
//   } 


//   if( servo_num == 2 )
//   {
//     servo_backward.write(midAng);

//     for(i = midAng; i < maxAng; i++)
//     {
//       servo_backward.write(i);  // tell servo to go to a particular angle
//       update_distances();
//       delay(10);
//     }

//   } 
// }

// void rotate_servo_right(int servo_num)
// {
//   if( servo_num == 1 )
//   {
//     servo_forward.write(midAng);

//     for(i = midAng; i > minAng; i--)
//     {
//       servo_forward.write(i);  // tell servo to go to a particular angle
//       update_distances();
//       delay(10);
//     }
//   } 


//   if( servo_num == 2 )
//   {
//     servo_backward.write(midAng);

//     for(i = midAng; i > minAng; i--)
//     {
//       servo_backward.write(i);  // tell servo to go to a particular angle
//       update_distances();
//       delay(10);
//     }

//   } 
// }




// this function will run all the motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_forward( int delayTime )
{
  //assigning input directions to motor driver 1
  stop(1000);
  delay(500);
  
  // motor 1
  digitalWrite(input_front1, LOW);
  digitalWrite(input_front2, HIGH); 
  
  //motor 2
  digitalWrite(input_front3, LOW);
  digitalWrite(input_front4, HIGH);

  delay(500);

  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input_back3, LOW);
  digitalWrite(input_back4, HIGH); 
  
  //motor 4
  digitalWrite(input_back1, LOW);
  digitalWrite(input_back2, HIGH);

  delay(delayTime);
}


// this function will run all the motors in backward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_backward(int delayTime)
{
  // Executing this function resulted in shutting off of powerbank, most likely reason maybe since we were not only making high pins to low but also low to high
  // This may have resulted in a lot of usage of current, Hence, we first stop the robot so that current used is less. This seems to work for this particular case.
  stop(1000);

  delay(500);

  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input_front1, HIGH);
  digitalWrite(input_front2, LOW); 
  
  //motor 2
  digitalWrite(input_front3, HIGH);
  digitalWrite(input_front4, LOW);


  delay(500);

  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input_back3, HIGH);
  digitalWrite(input_back4, LOW); 
  
  //motor 4
  digitalWrite(input_back1, HIGH);
  digitalWrite(input_back2, LOW);

  delay(delayTime);

}


// this function will run right motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_right(int delayTime)
{
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input_front1, LOW);
  digitalWrite(input_front2, LOW); 
  
  //motor 2
  digitalWrite(input_front3, LOW);
  digitalWrite(input_front4, HIGH);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input_back3, LOW);
  digitalWrite(input_back4, LOW); 
  
  //motor 4
  digitalWrite(input_back1, LOW);
  digitalWrite(input_back2, HIGH);

  delay(delayTime);
}


// this function will run left motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_left(int delayTime)
{
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input_front1, LOW);
  digitalWrite(input_front2, HIGH); 
  
  //motor 2
  digitalWrite(input_front3, LOW);
  digitalWrite(input_front4, LOW);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input_back3, LOW);
  digitalWrite(input_back4, HIGH); 
  
  //motor 4
  digitalWrite(input_back1, LOW);
  digitalWrite(input_back2, LOW);

  delay(delayTime);
}


// this function will stop all motors
// parameter delayTime indicates the time for which we want to execute the command
void stop(int delayTime)
{
  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input_front1, LOW);
  digitalWrite(input_front2, LOW); 
  
  //motor 2
  digitalWrite(input_front3, LOW);
  digitalWrite(input_front4, LOW);


  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input_back3, LOW);
  digitalWrite(input_back4, LOW); 
  
  //motor 4
  digitalWrite(input_back1, LOW);
  digitalWrite(input_back2, LOW);  

  delay(delayTime);
}


// Function to receive commands from rpi and move the robot accordingly
void receiveData(int byteCount) 
{

  Serial.print("recieving commands");

  while (Wire.available()) 
  {
    wireIn = Wire.read();

    if( wireIn == UP || wireIn == DOWN || wireIn == LEFT || wireIn == RIGHT || wireIn == STOP )
    {
      cmd = wireIn;

      Serial.print("command received: ");

      
      Serial.println(cmd);


      if( letRun )
      {

        if (cmd == UP) 
        {
          move_forward(1000);
        } 

        else if (cmd == DOWN) 
        {
          move_backward(1000);
        } 

        else if (cmd == RIGHT) 
        {
          move_right(1000);
        } 

        else if (cmd == LEFT) 
        {
          move_left(1000);
        } 

        else 
        {
          stop(5000);
        }

        delay(1000);
      }
    }

  }

}

void sendData() 
{
  Wire.write(wireIn);
}

void check_obstacle_take_action()
{
  update_distances();

  if( distance_forward < safetyDist )
  {
    stop(1);

    if( cmd == UP )
    {
      Serial.println("Command may lead to collision. Overriding. Initiating backup sequence....");
      letRun = 0;
      backup_algo();
    }

    else if( cmd == RIGHT || cmd == LEFT )
      letRun = 1;

  }

  if( distance_backward < safetyDist )
  {
    stop(1);

    if( cmd == DOWN )
    {
      Serial.println("Command may lead to collision. Overriding. Initiating backup sequence....");
      letRun = 0;
      backup_algo();
    }

    else
      letRun = 1;
  }

  if( distance_forward > safetyDist && distance_backward > safetyDist )
    letRun = 1;

}

void backup_algo()
{
  if( distance_forward < safetyDist )
  {
    int spaceFound = 0;
    servoang_front = midAng;

    while( !spaceFound )
    {
      servo_forward.write(servoang_front);
      update_distances();
      delay(10);      

      if(distance_forward > safetyDist)
        spaceFound = 1;

      if(servoang_front != maxAng)
        servoang_front++;

      else
      {
        Serial.println("No path found on the right.");
        break;
      }

    }

    if( spaceFound )
    {
      servo_forward.write(midAng);
      update_distances();

      while( distance_forward < safetyDist )
      {
        move_right(100);
        update_distances();
      }

      
      robotSafe = 0;

      while(!robotSafe)      
      {
        move_forward(1000);
        update_distances();

        if( distance_forward > safetyDist && distance_backward > safetyDist )
        {
          Serial.println("Robot now safe backup algo aborting....");
          stop(1);
          servo_forward.write(midAng);
          servo_backward.write(midAng);
          update_distances();
          robotSafe = 1;
          return;
        }
      }
    }

    if( !spaceFound )
      Serial.println("Looking for Path on Left");

    servoang_front = midAng;

    while( !spaceFound )
    {
      servo_forward.write(servoang_front);
      update_distances();
      delay(10);      

      if(distance_forward > safetyDist)
        spaceFound = 1;

      if(servoang_front != minAng)
        servoang_front--;

      else
      {
        Serial.println("No path found on the left.");
        break;
      }

    }

    if( spaceFound )
    {
      servo_forward.write(midAng);
      update_distances();

      while( distance_forward < safetyDist )
      {
        move_left(100);
        update_distances();
      }

      robotSafe = 0;

      while(!robotSafe)      
      {
        move_forward(1000);
        update_distances();

        if( distance_forward > safetyDist && distance_backward > safetyDist )
        {
          Serial.println("Robot now safe backup algo aborting....");
          robotSafe = 1;
          stop(1);
          servo_forward.write(midAng);
          servo_backward.write(midAng);
          update_distances();
          return;
        }
      }
    }

  }


  if( distance_backward < safetyDist )
  {
    int spaceFound = 0;
    servoang_back = midAng;

    while( !spaceFound )
    {
      servo_backward.write(servoang_back);
      update_distances();
      delay(10);      

      if(distance_backward > safetyDist)
        spaceFound = 1;

      if(servoang_back != maxAng)
        servoang_back++;

      else
      {
        Serial.println("No path found on the right.");
        break;
      }

    }

    if( spaceFound )
    {
      servo_backward.write(midAng);
      update_distances();

      while( distance_backward < safetyDist )
      {
        move_left(100);
        update_distances();
      }

      
      robotSafe = 0;

      while(!robotSafe)      
      {
        move_backward(1000);
        update_distances();

        if( distance_forward > safetyDist && distance_backward > safetyDist )
        {
          Serial.println("Robot now safe backup algo aborting....");
          stop(1);
          servo_forward.write(midAng);
          servo_backward.write(midAng);
          update_distances();

          robotSafe = 1;
          return;
        }
      }
    }

    if( !spaceFound )
      Serial.println("Looking for Path on Left");


    spaceFound = 0;
    servoang_back = midAng;

    while( !spaceFound )
    {
      servo_backward.write(servoang_back);
      update_distances();
      delay(10);      

      if(distance_backward > safetyDist)
        spaceFound = 1;

      if(servoang_back != minAng)
        servoang_back--;

      else
      {
        Serial.println("No path found on the left.");
        break;
      }

    }

    if( spaceFound )
    {
      servo_backward.write(midAng);
      update_distances();

      while( distance_backward < safetyDist )
      {
        move_right(100);
        update_distances();
      }

      
      robotSafe = 0;

      while(!robotSafe)      
      {
        move_backward(1000);
        update_distances();

        if( distance_forward > safetyDist && distance_backward > safetyDist )
        {
          Serial.println("Robot now safe backup algo aborting....");
          stop(1);
          servo_forward.write(midAng);
          servo_backward.write(midAng);
          update_distances();
          robotSafe = 1;
          return;
        }
      }
    }

    if( !spaceFound )
      Serial.println("No path found");

  }
}

void loop() 
{
  digitalWrite(powerPin, HIGH);
  update_distances();

  letRun = 0;
  check_obstacle_take_action();

  delay(100);
}
