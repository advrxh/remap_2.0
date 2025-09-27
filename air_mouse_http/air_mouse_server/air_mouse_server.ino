#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <MPU6050.h>

#define PORT 80
#define BAUD_RATE 115200

#define LEFT_BTN_PIN D5
#define RIGHT_BTN_PIN D6

MPU6050 mpu;
ESP8266WebServer server(PORT);

const char* ssid = "MECAP-WPA2";
const char* password = "8b140b20e7";

void setup() {
  Serial.begin(BAUD_RATE);
  Wire.begin();
  mpu.initialize();

  pinMode(LEFT_BTN_PIN, INPUT_PULLUP);
  pinMode(RIGHT_BTN_PIN, INPUT_PULLUP);

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

      String left_btn_read = (digitalRead(LEFT_BTN_PIN) == LOW) ? "ON" : "OFF";
      String right_btn_read = (digitalRead(RIGHT_BTN_PIN) == LOW) ? "ON" : "OFF";
      
      String data = "gx:" + String(gx) + ";" +
                    "gz:" + String(gz) + ";" +
                    "left_btn:" + left_btn_read + ";" +
                    "right_btn:" + right_btn_read;

      server.send(200, "text/plain", data);
  });
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
