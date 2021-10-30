#include <MPU6050.h>
#include <SPI.h>
#include <SD.h>

MPU6050 mpu;

const int chipSelect = 10;
File dataFile;

void setup() {
  unsigned long t0 = micros();
  Serial.begin(9600);
  delay(5000);
  Wire.begin();
  mpu.initialize();
  mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_2000);
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
  SD.remove("datalog.txt");
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  dataFile.println("time [us],a_x, a_y,"
    "a_z,omega_x,omega_y,omega_z,acc range,gyro range");
  dataFile.print("-1,");
  dataFile.print(mpu.getXAccelOffset());
  dataFile.print(",");
  dataFile.print(mpu.getYAccelOffset());
  dataFile.print(",");
  dataFile.print(mpu.getZAccelOffset());
  dataFile.print(",");
  dataFile.print(mpu.getXGyroOffset());
  dataFile.print(",");
  dataFile.print(mpu.getYGyroOffset());
  dataFile.print(",");
  dataFile.print(mpu.getZGyroOffset());
  dataFile.print(",");
  dataFile.print(mpu.getFullScaleAccelRange());
  dataFile.print(",");
  dataFile.println(mpu.getFullScaleGyroRange());
  Serial.println((micros()-t0)*1e-6);
  dataFile.close();
}

void loop() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;  
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  dataFile = SD.open("datalog.txt", FILE_WRITE);
  dataFile.print(micros());
  dataFile.print(",");  
  dataFile.print(ax);
  dataFile.print(",");
  dataFile.print(ay);
  dataFile.print(",");
  dataFile.print(az);
  dataFile.print(",");
  dataFile.print(gx);
  dataFile.print(",");
  dataFile.print(gy);
  dataFile.print(",");
  dataFile.println(gz);
  dataFile.close();
}
