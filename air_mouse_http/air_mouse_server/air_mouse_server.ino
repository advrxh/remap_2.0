#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <MPU6050.h>

#define PORT 80
#define BAUD_RATE 115200

MPU6050 mpu;
ESP8266WebServer server(PORT);

const char* ssid = "Airtel_ZEPTO";
const char* password = "Ks@12345678";

void setup() {
  Serial.begin(BAUD_RATE);
  Wire.begin();
  mpu.initialize();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", [](){
      int16_t ax, ay, az, gx, gy, gz;
      mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

      String data = "gx:" + String(gx) + ";" + "gz:" + String(gz);

      server.send(200, "text/plain", data);
  });
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
