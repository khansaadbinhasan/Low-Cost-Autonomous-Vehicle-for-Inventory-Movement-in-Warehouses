/*
  This sketch is to:
  --> Test if the servos work properly
  --> To adjust the angles of servos while mounting
*/

#include <Servo.h>

Servo myservo1;  // create servo object to control a servo
Servo myservo2;  // create servo object to control a servo

int i = 0;
int j = 0;

void setup() {
  myservo1.attach(5,600,2300);  // (pin, min, max)
  myservo2.attach(6,600,2300);  // (pin, min, max)
}
void loop() {

//  while(j < 10)
//  {
//    for(i = 0; i < 360; i++)
//    {
//      myservo1.write(i);  // tell servo to go to a particular angle
//      myservo2.write(i);  // tell servo to go to a particular angle
//      delay(100);
//    }
//    
//    while(i--)
//    {
//      myservo1.write(i);  // tell servo to go to a particular angle
//      myservo2.write(i);  // tell servo to go to a particular angle
//      delay(100);
//    }  
//
//    j++;
//  }

      myservo1.write(90);  // tell servo to go to a particular angle
      myservo2.write(90);  // tell servo to go to a particular angle
  delay(1000);
}
