  /*
  #define TRIG 2
  #define ECHO 4

  #define V 343.
  #define CONV (1.e-6*100.)
*/
  int TRIG = 2;
  int ECHO = 4;
  float V = 343.;
  float CONV = 1.e-6*100.;
  
  void setup() {
    Serial.begin(9600);
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    digitalWrite(TRIG, LOW);
  }
  
  void doMeasurement() {
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    unsigned long t0 = micros();
    unsigned long ut = pulseIn(ECHO, HIGH);
    unsigned long t1 = micros();
    float d = V*ut*CONV/2.;
    Serial.print((t0+t1)/2.);
    Serial.print(" ");
    Serial.println(d);
  }

  void loop() {
    doMeasurement();
    delay(50);
  }
