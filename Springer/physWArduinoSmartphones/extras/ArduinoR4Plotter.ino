/*
    Arduino V4 LED plotter
    Copyright (C) 2023 giovanni.organtini@gmail.com

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

#include "Arduino_LED_Matrix.h"

#define _DEBUG

ArduinoLEDMatrix matrix;

float x = 0.;
float dx = .05;

uint8_t arr[96];

void setup() {
  Serial.begin(9600);
  matrix.begin();
  for (int i = 0; i < 96; i++) {
    arr[i] = 0;
  }
}

void debug(float x, float y, int ix, int iy) {
  Serial.print(x);
  Serial.print(", ");
  Serial.print(y);
  Serial.print(" --> ");
  Serial.print(ix);
  Serial.print(", ");
  Serial.print(iy);
  Serial.println();
}
  
/* the following function returns the index of an LED on the Arduino V4
   LED matrix, given the cartesian coordinates (x,y). Coordinates are
   scaled such that one corner corresponds to (xm, xM), and the opposite
   to (ym, yM) */ 
int ledno(float x, float y, float xm = 0., float xM = 1., float ym = 0., float yM = 1.) {
  int ix = (int)(round((x - xm) * 12./(xM-xm))) % 12;
  int iy = (int)(round((y - ym) * 8./(yM - ym)));
  int index = (int)(12 * iy + ix);
#ifdef _DEBUG
  debug(x, y, ix, iy);
#endif
  arr[index] = 1;
  return index;
}

void corners() {
  matrix.on(ledno(0, 0));
  matrix.on(ledno(0,.9));
  matrix.on(ledno(.9,0));
  matrix.on(ledno(.9,.9));
}

#define _PERSIST

void plot(float x) {
  matrix.on(ledno(x, sin(2*PI*x), 0, 1, -1, 1));
#ifdef _PERSIST
  matrix.loadPixels(arr, 96);
#endif
}

void poly(float x, int degree, float* a, float xm = 0., 
          float xM = 1., float ym = 0., float yM = 1.) {
  float y = 0;
  for (int i = 0; i < degree + 1; i++) {
    y += a[i]*pow(x, i);
  }
  matrix.on(ledno(x, y, xm, xM, ym, yM));
#ifdef _PERSIST
  matrix.loadPixels(arr, 96);
#endif
}

void clear() {
  for (int i = 0; i < 96; i++) {
    arr[i] = {0};
  }
  matrix.loadPixels(arr, 96);
}

void show() {
  for (int n = 0; n < 7; n++) {
    x = -1;
    while (x < 1) {
      float a[7] = {0.};
      if (n > 0) {
        a[n] = 1.;
      }
      poly(x, n, a, -1, 1, -1, 1);
      x += dx;
    }
    delay(200);
    clear();
  }
}

void loop() {
  x += dx;
  //corners();
  //plot(x);
  //float a[3] = {0., 0., 1.};
  //poly(x, 2, a);
  //if (x >= 1) {
  //  while (1) {
  //    // do nothing
  //  }
  //}
  show();
}
