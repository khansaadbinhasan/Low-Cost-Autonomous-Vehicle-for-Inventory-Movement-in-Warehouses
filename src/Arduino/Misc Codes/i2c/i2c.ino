/*
  --> This sketch helps in I2C communication with the raspberry pi
  --> This sketch receives the data from rpi and sends the data to it
  --> This was taken from https://dzone.com/articles/arduino-and-raspberry-pi-working-together-part-2-now-with-i2
  --> Uses A4 and A5 pins of arduino and connects according to /rsc/i2c.jpg
*/


#include <Wire.h>

#define SLAVE_ADDRESS 0x04

int cmd = 0;

void setup() 
{
  pinMode(LED, OUTPUT);

  Serial.begin(9600);

  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready!");
}

void loop() 
{
  delay(100);
}

void receiveData(int byteCount) 
{

  Serial.print("receiveData");

  while (Wire.available()) 
  {
    cmd = Wire.read();

    Serial.print("command received: ");

    Serial.println(cmd);

    if (cmd == 1) 
    {
      Serial.println("move_forward");

    } 
    
    else 
    {
      Serial.println("Stopping");
    }

  }

}

void sendData() {

  Wire.write(number);

}
