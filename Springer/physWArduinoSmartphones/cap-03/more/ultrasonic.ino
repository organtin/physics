#define TRIG 7
#define ECHO 8

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  digitalWrite(TRIG, LOW);
}

void loop() {
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long t1 = micros();
  unsigned long t = pulseIn(ECHO, HIGH);
  unsigned long t2 = micros();
  Serial.print((t1+t2)/2);
  Serial.print(",");
  Serial.println(t);
}
