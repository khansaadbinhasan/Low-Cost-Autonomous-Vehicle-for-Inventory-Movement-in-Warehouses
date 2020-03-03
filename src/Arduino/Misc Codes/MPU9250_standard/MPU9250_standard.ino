#include "math.h"
#include "MPU9250.h"

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);
int status;

void setup() 
{
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

  // start communication with IMU 
  status = IMU.begin();
  
  if (status < 0) 
  {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
}

void loop() {
  // read the sensor
  IMU.readSensor();

  float accelX = IMU.getAccelX_mss();

  
  // display the data
  Serial.print("\n\n");

  Serial.print("Acceleration(m/s^2):");
  Serial.print("\n\t\tX:\t");
  Serial.print(IMU.getAccelX_mss(),6);
  Serial.print("\n\t\tY:\t");
  Serial.print(IMU.getAccelY_mss(),6);
  Serial.print("\n\t\tZ:\t");
  Serial.print(IMU.getAccelZ_mss(),6);
  

  Serial.print("\n\n");
  Serial.print("Gyroscope(Degree):");
  Serial.print("\n\t\tX:\t");
  Serial.print(IMU.getGyroX_rads()*180/M_PI,6);
  Serial.print("\n\t\tY:\t");
  Serial.print(IMU.getGyroY_rads()*180/M_PI,6);
  Serial.print("\n\t\tZ:\t");
  Serial.print(IMU.getGyroZ_rads()*180/M_PI,6);
  

  Serial.print("\n\n");
  Serial.print("Magnetometer(microTesla):");
  Serial.print("\n\t\tX:\t");
  Serial.print(IMU.getMagX_uT(),6);
  Serial.print("\n\t\tY:\t");
  Serial.print(IMU.getMagY_uT(),6);
  Serial.print("\n\t\tZ:\t");
  Serial.print(IMU.getMagZ_uT(),6);
  Serial.print("\n\n");

//
//  pitch = 180 * atan2(accelX, sqrt(accelY*accelY + accelZ*accelZ))/PI;
//  roll = 180 * atan2(accelY, sqrt(accelX*accelX + accelZ*accelZ))/PI;
//  mag_x = magReadX*cos(pitch) + magReadY*sin(roll)*sin(pitch) + magReadZ*cos(roll)*sin(pitch)
//  mag_y = magReadY * cos(roll) - magReadZ * sin(roll)
//  yaw = 180 * atan2(-mag_y,mag_x)/M_PI;


  Serial.print("Temperature(Deg Celsius):\t");
  Serial.println(IMU.getTemperature_C(),6);
  Serial.print("\n\n");
  

  delay(100);
}
