// This program gives commands to move car in forward, backward, right and left directions and to stop the car
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define LED  13


// status of the command given -1 represents error
int status = -1;
int forward = 0;
int backward = 1;
int right = 2;
int left = 3;
int stopcmd = 4;

// motor driver 1
// motor one
int enable1A = 3;
int input11 = 2;
int input12 = 4;


// motor two
int enable1B = 5;
int input13 = 7;
int input14 = 8;



// motor driver 2
// motor three
int enable2B = 6;
int input23 = 12;
int input24 = 13;


// motor four
int enable2A = 9;
int input21 = 10;
int input22 = 11;




void setup()
{
  //motor drive 1
  // motor 1
  pinMode(input11, OUTPUT);
  pinMode(input12, OUTPUT);
  pinMode(enable1A, OUTPUT);
  
  // motor 2
  pinMode(input13, OUTPUT);
  pinMode(input14, OUTPUT);
  pinMode(enable1B, OUTPUT);



  //motor drive 2
  // motor 3
  pinMode(input23, OUTPUT);
  pinMode(input24, OUTPUT);
  pinMode(enable2B, OUTPUT);
  
  // motor 4
  pinMode(input21, OUTPUT);
  pinMode(input22, OUTPUT);
  pinMode(enable2A, OUTPUT);

  Serial.begin(9600);

  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveCmd);
  Wire.onRequest(sendStatus);

  Serial.println("Ready!");
}



void move_forward()
{
  // this function will run all the motors in forward direction
  
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
  digitalWrite(input21, LOW);
  digitalWrite(input22, HIGH);
  

  //assigning input speeds to motors
  analogWrite(enable1A, 290);
  analogWrite(enable1B, 290);
  analogWrite(enable2B, 290);
  analogWrite(enable2A, 290);

}


void move_backward()
{
  // this function will run all the motors in backward direction
  
  //assigning input directions to motor driver 1
  
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
  digitalWrite(input21, HIGH);
  digitalWrite(input22, LOW);
  

  //assigning input speeds to motors
  analogWrite(enable1A, 290);
  analogWrite(enable1B, 290);
  analogWrite(enable2B, 290);
  analogWrite(enable2A, 290);

}


void move_right()
{
  // this function will turn the car in right direction
  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, LOW);
  digitalWrite(input12, HIGH); 

  //motor 2
  digitalWrite(input13, LOW);
  digitalWrite(input14, LOW);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, LOW);
  digitalWrite(input24, HIGH); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, LOW);
  

  //assigning input speeds to motors
  analogWrite(enable1A, 290);
  analogWrite(enable2B, 290);

}


void move_left()
{
  // this function will turn the car in left direction
  
  //assigning input directions to motor driver 1
  
  // motor 1
  digitalWrite(input11, LOW);
  digitalWrite(input12, LOW); 

  //motor 2
  digitalWrite(input13, LOW);
  digitalWrite(input14, HIGH);



  //assigning input directions to motor driver 2
  
  //motor 3
  digitalWrite(input23, LOW);
  digitalWrite(input24, LOW); 
  
  //motor 4
  digitalWrite(input21, LOW);
  digitalWrite(input22, HIGH);
  

  //assigning input speeds to motors
  analogWrite(enable1B, 290);
  analogWrite(enable2A, 290);
}


void stop()
{
  // this function will stop all motors
  
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
  
}


void receiveCmd(int inputCmd)
{

  Serial.print("receiveData");

  while (Wire.available())
  {
    inputCmd = Wire.read();

    if( inputCmd == forward )
    {
      move_forward();
      Serial.println("moving forward ......");
      status = forward;
    }

    else if( inputCmd == backward )
    {
      move_backward();
      Serial.println("moving backward ......");
      status = backward;
    }
    
    else if( inputCmd == right )
    {
      move_right();
      Serial.println("moving right ......");
      status = right;
    }
    
    else if( inputCmd == left )
    {
      move_left();
      Serial.println("moving left ......");
      status = left;
    }
    
    else if( inputCmd == stopcmd )
    {
      stop();
      Serial.println("stopping ......");
      status = stopcmd;
    }
  }
}


void sendStatus()
{
  Wire.write(status);
}

// void loop()
// {
//   move_forward();
//   delay(1000);

//   move_backward();
//   delay(1000);
  
//   move_right();
//   delay(1000);
  
//   move_left();
//   delay(1000);
  
//   stop();
//   delay(1000);
// }


void loop()
{
  delay(100);
}
