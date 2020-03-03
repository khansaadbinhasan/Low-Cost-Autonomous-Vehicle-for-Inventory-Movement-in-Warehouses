/*
  --> This sketch runs motors in different directions.
  --> After setting up the Robot, upload this sketch to arduino.
  --> This can be used to test if motors are working correctly or not and also if the robot is executing steering commands correctly(e.g, on different surfaces)
*/

// motor driver 1
// motor one
const int input11 = 2;
const int input12 = 4;


// motor two
const int input13 = 7;
const int input14 = 8;


// motor driver 2
// motor three
const int input23 = 12;
const int input24 = 13;


// motor four
const int input21 = 10;
const int input22 = 11;


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
void rotate_right(int delayTime)
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
void rotate_left(int delayTime)
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
  move_forward(2500);
  delay(1000);
  rotate_left(2500);
  delay(1000);
  move_forward(1000);
  delay(1000);
  rotate_right(2500);
  delay(1000);
  move_backward(2500);
  delay(1000);
  stop(10000);
  delay(5000);
}





































// void backup()
// {
//    // update_distances();
//  // decide_and_execute();
//  if( distance1 > safety_dist && distance1 < upper_HCSR04_limit )
//  {
//    // servoang1 = defaultAng;
//    // servoang2 = defaultAng;
//    move_forward(200);
//  }

//  if( distance1 < safety_dist && distance1 > lower_HCSR04_limit )
//  {
//    servoang1 = minAng;

//    while( distance1 < safety_dist && distance1 < upper_HCSR04_limit && servoang1 < maxAng ) 
//    {
//      servoang1++;  
//      update_distances();
//    }

//    if( servoang1 > minAng && servoang1 < midAng )
//    { 
//      while(servoang1 > minAng && servoang1 < midAng && distance1 > safety_dist)
//      {
//        rotate_left(100);
//        update_distances();
//      }

//      if( distance1 < safety_dist )
//      {
//        rotate_right(200);

//        if( distance1 < safety_dist )
//        {
//          forward_movement--;
//        }
//      }

//    }

//    if( servoang1 > midAng && servoang1 < maxAng )
//    {
//      while(servoang1 > midAng && servoang1 < maxAng && distance1 > safety_dist)
//      {
//        rotate_right(100);
//        update_distances();
//      }

//      if( distance1 < safety_dist )
//      {
//        rotate_left(200);

//        if( distance1 < safety_dist )
//        {
//          forward_movement--;
//        }
//      }
//    }

//    if( servoang1 == maxAng && forward_movement == 0 )
//    {
//      Serial.println("forward movement not possible");
//    }

//  }

//  update_distances();

//  if( forward_movement == 0 && distance1 < upper_HCSR04_limit && distance1 > lower_HCSR04_limit )
//  {
//    if( distance2 > safety_dist && distance2 < upper_HCSR04_limit )
//    {
//      servoang1 = defaultAng;
//      servoang2 = defaultAng;
//      move_backward(200);
//    }

//    if( distance2 < safety_dist && distance2 > lower_HCSR04_limit )
//    {
//      servoang2 = minAng;

//      while( distance2 < safety_dist && distance2 < upper_HCSR04_limit && servoang2 < maxAng ) 
//      {
//        servoang2++;  
//        update_distances();
//      }

//      if( servoang2 > minAng && servoang2 < midAng )
//      { 
//        while(servoang2 > minAng && servoang2 < midAng && distance2 > safety_dist)
//        {
//          rotate_right(100);
//          update_distances();
//        }

//        if( distance2 < safety_dist )
//        {
//          rotate_left(200);

//          if( distance2 < safety_dist )
//          {
//            backward_movement--;
//          }
//        }

//      }

//      if( servoang2 > midAng && servoang2 < maxAng )
//      {
//        while(servoang2 > midAng && servoang2 < maxAng && distance2 > safety_dist)
//        {
//          rotate_left(100);
//          update_distances();
//        }

//        if( distance2 < safety_dist )
//        {
//          rotate_right(200);

//          if( distance2 < safety_dist )
//          {
//            backward_movement--;
//          }
//        }
//      }

//      if( servoang2 == maxAng && backward_movement == 0 )
//      {
//        Serial.println("forward movement not possible");
//      }

//    }

//  }

//  reset_variables();

// }








  // if( distance1 > safety_dist && distance1 < upper_HCSR04_limit )
  // {
  //   Serial.println("distance > safety_dist, adjusting servos to default angle moving forward");
  //   servo1.write(servoang1);
  //   servo2.write(servoang2);
  // }

  // if( distance1 < safety_dist && distance1 > lower_HCSR04_limit )
  // {
  //   servoang1 = minAng;
  //   Serial.println("distance < safety_dist, adjusting servos to min angle");
  //   servo1.write(servoang1);

  //   while( distance1 < safety_dist && distance1 < upper_HCSR04_limit && servoang1 < maxAng ) 
  //   {
  //     servoang1++;  
      
  //     Serial.println("distance < safety_dist, and servoang1 < maxAng rotating servo");
    
  //     servo1.write(servoang1);
  //     update_distances();
  //   }

  //   if( servoang1 > minAng && servoang1 < midAng )
  //   { 
  //     while(servoang1 > minAng && servoang1 < midAng && distance1 > safety_dist)
  //     {
  //       // rotate_left(100);
  //       update_distances();
  //     }

  //     if( distance1 < safety_dist )
  //     {
  //       // rotate_right(200);

  //       if( distance1 < safety_dist )
  //       {
  //         forward_movement--;
  //       }
  //     }

  //   }

  //   if( servoang1 > midAng && servoang1 < maxAng )
  //   {
  //     while(servoang1 > midAng && servoang1 < maxAng && distance1 > safety_dist)
  //     {
  //       // rotate_right(100);
  //       update_distances();
  //     }

  //     if( distance1 < safety_dist )
  //     {
  //       // rotate_left(200);

  //       if( distance1 < safety_dist )
  //       {
  //         forward_movement--;
  //       }
  //     }
  //   }

  //   if( servoang1 == maxAng && forward_movement == 0 )
  //   {
  //     Serial.println("forward movement not possible");
  //   }

  // }

  // update_distances();


  // if( forward_movement == 0 && distance1 < upper_HCSR04_limit && distance1 > lower_HCSR04_limit )
  // {
  //   reset_variables();

  //   if( distance2 > safety_dist && distance2 < upper_HCSR04_limit )
  //   {
  //     Serial.println("distance > safety_dist, adjusting servos to default angle moving forward");
  //     servo1.write(servoang1);
  //     servo2.write(servoang2);
  //     // move_backward(200);
  //   }

  //   if( distance2 < safety_dist && distance2 > lower_HCSR04_limit )
  //   {
  //     servoang2 = minAng;
  //     Serial.println("distance < safety_dist, and servoang1 < maxAng rotating servo");
  //     servo2.write(servoang2);

  //     while( distance2 < safety_dist && distance2 < upper_HCSR04_limit && servoang2 < maxAng ) 
  //     {
  //       servoang2++;  
  //       Serial.println("distance < safety_dist, and servoang1 < maxAng rotating servo");
  //       servo2.write(servoang2);
        
  //       update_distances();
  //     }

  //     if( servoang2 > minAng && servoang2 < midAng )
  //     { 
  //       while(servoang2 > minAng && servoang2 < midAng && distance2 > safety_dist)
  //       {
  //         // rotate_right(100);
  //         update_distances();
  //       }

  //       if( distance2 < safety_dist )
  //       {
  //         // rotate_left(200);

  //         if( distance2 < safety_dist )
  //         {
  //           backward_movement--;
  //         }
  //       }

  //     }

  //     if( servoang2 > midAng && servoang2 < maxAng )
  //     {
  //       while(servoang2 > midAng && servoang2 < maxAng && distance2 > safety_dist)
  //       {
  //         // rotate_left(100);
  //         update_distances();
  //       }

  //       if( distance2 < safety_dist )
  //       {
  //         // rotate_right(200);

  //         if( distance2 < safety_dist )
  //         {
  //           backward_movement--;
  //         }
  //       }
  //     }

  //     if( servoang2 == maxAng && backward_movement == 0 )
  //     {
  //       Serial.println("forward movement not possible");
  //     }

  //   }

  // }

  // reset_variables();
