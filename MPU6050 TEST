
#include <Wire.h>

#define MPU_ADDR 0x68

void setup() {
  Serial.begin(115200);

  // NodeMCU ESP8266 I2C pins
  Wire.begin(D2, D1);  // SDA, SCL

  Serial.println();
  Serial.println("MiniTARS MPU6050 Test");

  // Check whether MPU6050 responds
  Wire.beginTransmission(MPU_ADDR);
  byte error = Wire.endTransmission();

  if (error == 0) {
    Serial.println("MPU6050 detected!");

    // Read WHO_AM_I register
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x75);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_ADDR, 1);

    if (Wire.available()) {
      byte id = Wire.read();
      Serial.print("WHO_AM_I: 0x");
      Serial.println(id, HEX);
    }

    // Wake up the MPU6050
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x6B);  // Power management register
    Wire.write(0x00);  // Wake up sensor
    Wire.endTransmission();

  } else {
    Serial.println("MPU6050 NOT detected!");
    Serial.println("Check VCC, GND, SDA and SCL.");
  }
}

void loop() {
  // Read 14 bytes starting from accelerometer X high byte
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  if (Wire.endTransmission(false) != 0) {
    Serial.println("I2C read error");
    delay(1000);
    return;
  }

  byte count = Wire.requestFrom(MPU_ADDR, 14);

  if (count == 14) {
    int16_t ax = (Wire.read() << 8) | Wire.read();
    int16_t ay = (Wire.read() << 8) | Wire.read();
    int16_t az = (Wire.read() << 8) | Wire.read();

    int16_t temperature = (Wire.read() << 8) | Wire.read();

    int16_t gx = (Wire.read() << 8) | Wire.read();
    int16_t gy = (Wire.read() << 8) | Wire.read();
    int16_t gz = (Wire.read() << 8) | Wire.read();

    // Default sensitivity: accelerometer ±2g, gyro ±250 degrees/sec
    Serial.print("Accel (g): ");
    Serial.print(ax / 16384.0, 2);
    Serial.print(", ");
    Serial.print(ay / 16384.0, 2);
    Serial.print(", ");
    Serial.print(az / 16384.0, 2);

    Serial.print(" | Gyro (deg/s): ");
    Serial.print(gx / 131.0, 2);
    Serial.print(", ");
    Serial.print(gy / 131.0, 2);
    Serial.print(", ");
    Serial.println(gz / 131.0, 2);
  } else {
    Serial.println("Incomplete sensor data");
  }

  delay(1000);
}
