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
  float accelY = IMU.getAccelY_mss();
  float accelZ = IMU.getAccelZ_mss();

  float gyroX = IMU.getGyroX_rads();
  float gyroY = IMU.getGyroY_rads();
  float gyroZ = IMU.getGyroZ_rads();

  float magReadX = IMU.getMagX_uT();
  float magReadY = IMU.getMagY_uT();
  float magReadZ = IMU.getMagZ_uT();

  float tempC = IMU.getTemperature_C();

  float pitch = 180 * atan2( accelX, sqrt(accelY * accelY + accelZ * accelZ) ) / PI;
  float roll = 180 * atan2( accelY, sqrt(accelX * accelX + accelZ * accelZ) ) / PI;

  float mag_x = magReadX*cos(pitch) + magReadY*sin(roll)*sin(pitch) + magReadZ*cos(roll)*sin(pitch);
  float mag_y = magReadY * cos(roll) - magReadZ * sin(roll);
  float yaw = 180 * atan2(-mag_y,mag_x)/M_PI;


  // display the data
//  Serial.print("\n\nAcceleration(m/s^2):");
//    Serial.print("\n\t\tX:\t");Serial.print(accelX);
//    Serial.print("\n\t\tY:\t");Serial.print(accelY);
//    Serial.print("\n\t\tZ:\t");Serial.print(accelZ);
//  
//
//  Serial.print("\n\nGyroscope(rad/s):");
//    Serial.print("\n\t\tX:\t");Serial.print(gyroX);
//    Serial.print("\n\t\tY:\t");Serial.print(gyroY);
//    Serial.print("\n\t\tZ:\t");Serial.print(gyroZ);
//  
//
//  Serial.print("\n\nMagnetometer(microTesla):");
//    Serial.print("\n\t\tX:\t");Serial.print(magReadX);
//    Serial.print("\n\t\tY:\t");Serial.print(magReadY);
//    Serial.print("\n\t\tZ:\t");Serial.print(magReadZ);
//
//
//  Serial.print("\n\nTemperature(Deg Celsius):\t");Serial.println(tempC);
  

  Serial.print("\n\nYPR(degrees):");
    Serial.print("\n\t\tYaw:\t");Serial.print(yaw);
    Serial.print("\n\t\tPitch:\t");Serial.print(pitch);
    Serial.print("\n\t\tRoll:\t");Serial.print(roll);

  delay(100);

}
