#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <QMC5883LCompass.h>
#include <Arduino.h>

float ax,ay,az;
float gx,gy,gz;
float mx,my,mz;

Adafruit_MPU6050 mpu;
QMC5883LCompass compass;

void setup()
{
  Serial.begin(115200);
  mpu.begin();
  mpu.setI2CBypass(true);
  compass.init();
  mpu.setGyroRange(MPU6050_RANGE_1000_DEG);
  delay(100);
}

void loop()
{
  compass.read();
  sensors_event_t a,g,temp;
  mpu.getEvent(&a, &g, &temp);

  ax = a.acceleration.x;
  ay = a.acceleration.y;
  az = a.acceleration.z;

  gx = g.gyro.x;
  gy = g.gyro.y;
  gz = g.gyro.z;

  mx = compass.getX();
  my = compass.getY();
  mz = compass.getZ();

  Serial.print(ax);
  Serial.print(" ");
  Serial.print(ay);
  Serial.print(" ");
  Serial.print(az);
  Serial.print("\n");

  Serial.print(gx);
  Serial.print(" ");
  Serial.print(gy);
  Serial.print(" ");
  Serial.print(gz);
  Serial.print("\n");

  Serial.print(mx);
  Serial.print(" ");
  Serial.print(my);
  Serial.print(" ");
  Serial.print(mz);
  Serial.print("\n");

  delay(100);
}
