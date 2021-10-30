#include <SD.h>

File dataFile;

void setup() {
  SD.begin();
  Serial.begin(9600);
  dataFile = SD.open("test.dat", FILE_WRITE);
}

void loop() {
  float x = 1024;
  dataFile.read((char *)&x, sizeof(float));
  Serial.println(x);
  delay(10000);
}
