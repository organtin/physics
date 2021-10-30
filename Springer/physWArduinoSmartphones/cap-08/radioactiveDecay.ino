#define N 750

int n = 0;
int atoms[N] = {0};

void setup() {
  pinMode(3, OUTPUT);
  digitalWrite(3, 0);
  Serial.begin(9600);
}

void loop() {
  n++;
  int k = 0;
  for (int i = 0; i < N; i++) {
    float p = (float)random(10000)/10000;
    if ((p < 1.e-4) && (atoms[i] == 0)) {
      digitalWrite(3, 127);
      delay(10);
      digitalWrite(3, 0);
      atoms[i] = 1;
      k++;
    }
  }
  Serial.print(n);
  Serial.print(" ");
  Serial.println(k);
}
