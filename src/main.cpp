#include <Arduino.h>

#define LED_PIN 25

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

uint blinkTime {0};
bool blink {false};
void loop() {
  uint currentTime = millis();
  if (currentTime >= blinkTime + 1000) {
    Serial.println("Blink");
    digitalWrite(LED_PIN, blink);
    blink = !blink;
    blinkTime = currentTime;
  }
}