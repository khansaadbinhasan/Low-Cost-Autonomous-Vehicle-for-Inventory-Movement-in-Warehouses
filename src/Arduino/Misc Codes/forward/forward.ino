/*
  --> This sketch runs all motors in forward direction.
  --> After setting up the Robot, upload this sketch to arduino.
  --> This can be used to test if motors are working correctly or not
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
void move_forward()
{
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

  //assigning input speeds to motors
  
  delay(2000);

}
void loop()
{
  move_forward();
  delay(2000);
}