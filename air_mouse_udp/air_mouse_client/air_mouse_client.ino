#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "MPU6050.h"

#define BAUD_RATE 115200
#define LEFT_BTN_PIN D5
#define RIGHT_BTN_PIN D6
#define SERVER_IP "192.168.9.255"
#define SERVER_PORT 4210

MPU6050 mpu;
WiFiUDP udp;

const char *ssid = "MECAP-WPA2";
const char *password = "8b140b20e7";

void setup()
{
  Serial.begin(BAUD_RATE);
  Wire.begin();
  mpu.initialize();

  pinMode(LEFT_BTN_PIN, INPUT_PULLUP);
  pinMode(RIGHT_BTN_PIN, INPUT_PULLUP);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(SERVER_PORT); 
  Serial.println("UDP ready to send data");
}

void loop()
{

  int16_t gx, gz, gy, ax, az, ay;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  String left_btn_read = (digitalRead(LEFT_BTN_PIN) == LOW) ? "ON" : "OFF";
  String right_btn_read = (digitalRead(RIGHT_BTN_PIN) == LOW) ? "ON" : "OFF";

  String data = "";
  data += "gx:" + String(gx) + ";";
  data += "gz:" + String(gz) + ";";
  data += "left_btn:" + left_btn_read + ";";
  data += "right_btn:" + right_btn_read;

  udp.beginPacket(SERVER_IP, SERVER_PORT);
  udp.write(data.c_str());
  udp.endPacket();

  delay(10); // Refresh 100 times per second ~ 100Hz 
}
