#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "MPU6050.h"

#define BAUD_RATE 115200

MPU6050 mpu;
WiFiUDP udp;

const char *ssid = "Airtel_ZEPTO";
const char *password = "Ks@12345678";

const char *serverIP = "192.168.1.12"; 
const int serverPort = 4210;

void setup()
{
  Serial.begin(BAUD_RATE);
  Wire.begin();
  mpu.initialize();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(serverPort); 
  Serial.println("UDP ready to send data");
}

void loop()
{
  int16_t gx, gz;
  mpu.getMotion6(NULL, NULL, NULL, &gx, NULL, &gz);

  String data = "gx:" + String(gx) + ";gz:" + String(gz);

  udp.beginPacket(serverIP, serverPort);
  udp.write(data.c_str());
  udp.endPacket();

  delay(10); // Refresh 100 times per second ~ 100Hz 
}
