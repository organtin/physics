void setup() {
  Serial.begin(9600);
}

void loop() {
  float S = 0.;
  float S2 = 0.;
  for (int i = 0; i < 1000; i++) {
    int k = analogRead(A0);
    int k2 = k*k;
    S += k;
    S2 += k2;
  }
  Serial.print(S/1000);
  Serial.print("+-");
  Serial.println(sqrt(S2/1000-S*S*1e-6));
  while (1) {
  // do nothing  
  }
}
