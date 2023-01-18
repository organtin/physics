/*
  speedoMeter  
  Copyright (C) 2023 Giovanni Organtini giovanni.organtini@uniroma1.it

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

/*
  See 
*/

#define TRIG 7    // the pin connected to the TRIG lead of the HCSR04 
#define ECHO 8    // the pin connected to the ECHO lead of the HCSR04
#define DMAX 1.   // the maximum distance between the sensor and the moving part
#define S 0.165   // the length of the moving part (in m): adjust it to your needs

unsigned long threshold;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  digitalWrite(TRIG, LOW);
  // compute the time threshold for the HCSR04, as 70% of the
  // time needed to sound to cover the distance the 
  // maximum possible distance    
  threshold = floor(2*0.7*DMAX/340.*1e6);
  Serial.print("Threshold = ");
  Serial.print(threshold);
  Serial.print(" us, corresponding to ");
  Serial.print(threshold * 1.e-6 * 33000. / 2);
  Serial.println(" cm");
}

void loop() {
  unsigned long t;
  do {    
    digitalWrite(TRIG, HIGH);  // trigger the sensor
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    t = pulseIn(ECHO, HIGH);   // measure the distance of the obstacle
  } while (t > threshold);     // wait until it goes below the threshold
  unsigned long t1 = micros(); // start time
  do {    
    digitalWrite(TRIG, HIGH);  //repeat the distance measurement
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    t = pulseIn(ECHO, HIGH);
  } while (t <= threshold);
  unsigned long t2 = micros(); // stop time
  Serial.print("t = "); 
  Serial.print(t2-t1);
  Serial.print(" us --> v = ");
  Serial.print(S/((t2 - t1)*1.e-6));
  Serial.println(" m/s");
  delay(1000);
}
