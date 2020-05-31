/*
  --> Uses A4 and A5 pins of arduino and connects according to /rsc/i2c.jpg
  --> This sketch helps in I2C communication with the raspberry pi, receives command from the pi and sends ACK to it
  --> This sketch runs motors in different directions according to commands received via I2C from rpi.
  --> After setting up the Robot, upload this sketch to arduino.
  --> This can be used to test if remote control is working or not
*/
#include <Wire.h>

#define SLAVE_ADDRESS 0x04


// commands to move the robot in different directions
int STOP = 0;
int UP = 1;
int DOWN = 2;
int RIGHT = 3;
int LEFT = 4;

int cmd = STOP;


// motor driver 1
// motor one
int input11 = 2;
int input12 = 4;


// motor two
int input13 = 7;
int input14 = 8;


// motor driver 2
// motor three
int input23 = 12;
int input24 = 13;


// motor four
int input21 = 10;
int input22 = 11;


void setup()
{
  //Setting up the I2C connections
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);


  //motor drive 1
  // motor 1
  pinMode(input11, OUTPUT);
  pinMode(input12, OUTPUT);
  
  // motor 2
  pinMode(input13, OUTPUT);
  pinMode(input14, OUTPUT);


  //motor drive 2
  // motor 3
  pinMode(input23, OUTPUT);
  pinMode(input24, OUTPUT);
  
  // motor 4
  pinMode(input21, OUTPUT);
  pinMode(input22, OUTPUT);

  Serial.begin(9600);

}


// this function will run all the motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_forward( int delayTime )
{
  //assigning input directions to motor driver 1
  stop(1000);

  
  // motor 1
  digitalWrite(input11, HIGH);
  digitalWrite(input12, LOW); 
  
  //motor 2
  digitalWrite(input13, HIGH);
  digitalWrite(input14, LOW);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, HIGH);
  digitalWrite(input24, LOW); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, HIGH);

  delay(delayTime);
}


// this function will run all the motors in backward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_backward(int delayTime)
{
  // Executing this function resulted in shutting off of powerbank, most likely reason maybe since we were not only making high pins to low but also low to high
  // This may have resulted in a lot of usage of current, Hence, we first stop the robot so that current used is less. This seems to work for this particular case.
  stop(1000);

  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, LOW);
  digitalWrite(input12, HIGH); 
  
  //motor 2
  digitalWrite(input13, LOW);
  digitalWrite(input14, HIGH);


  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, LOW);
  digitalWrite(input24, HIGH); 
  
  //motor 4
  digitalWrite(input21, HIGH);
  digitalWrite(input22, LOW);

  delay(delayTime);

}


// this function will run right motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_right(int delayTime)
{
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, LOW);
  digitalWrite(input12, LOW); 
  
  //motor 2
  digitalWrite(input13, HIGH);
  digitalWrite(input14, LOW);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, LOW);
  digitalWrite(input24, LOW); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, HIGH);

  delay(delayTime);
}


// this function will run left motors in forward direction
// parameter delayTime indicates the time for which we want to execute the command
void move_left(int delayTime)
{
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, HIGH);
  digitalWrite(input12, LOW); 
  
  //motor 2
  digitalWrite(input13, LOW);
  digitalWrite(input14, LOW);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, HIGH);
  digitalWrite(input24, LOW); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, LOW);

  delay(delayTime);
}


// this function will stop all motors
// parameter delayTime indicates the time for which we want to execute the command
void stop(int delayTime)
{
  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, LOW);
  digitalWrite(input12, LOW); 
  
  //motor 2
  digitalWrite(input13, LOW);
  digitalWrite(input14, LOW);


  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, LOW);
  digitalWrite(input24, LOW); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, LOW);  

  delay(delayTime);
}


// Function to receive commands from rpi and move the robot accordingly
void receiveData(int byteCount) 
{

  Serial.print("receiveing commands");

  while (Wire.available()) 
  {
    cmd = Wire.read();

    Serial.print("command received: ");

    
    Serial.println(cmd);


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

void sendData() 
{
  Wire.write(cmd);
}


void loop()
{
  delay(100);
}
