/*
  --> This sketch runs motors in different directions.
  --> After setting up the Robot, upload this sketch to arduino.
  --> This can be used to test if motors are working correctly or not and also if the robot is executing steering commands correctly(e.g, on different surfaces)
*/

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

void loop()
{
  move_forward(5000);
  delay(1000);
  move_left(5000);
  delay(1000);
  move_forward(5000);
  delay(1000);
  move_right(2500);
  delay(1000);
  move_forward(5000);
  delay(1000);
  move_backward(5000);
  delay(1000);
  stop(10000);
  delay(5000);
}
