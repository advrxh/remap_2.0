#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Replace with your WiFi credentials
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

// Create web server on port 80
ESP8266WebServer server(80);

const int ledPin = D4;

void homePage() {
  String html;
  html += "<a href=\"/on\"><button style=\"background:green\">LED ON</button></a>";
  html += "<br/>"
  html += "<a href=\"/off\"><button  style=\"background:red\">LED OFF</button></a>";
  server.send(200, "text/html", html);
}

void switchOn() {
  digitalWrite(ledPin, !HIGH);
  server.sendHeader("Location", "/"); // redirect back to main page
  server.send(303);
}

void switchOff() {
  digitalWrite(ledPin, !LOW);
  server.sendHeader("Location", "/"); // redirect back to main page
  server.send(303);
}

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, !LOW);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("ESP8266 IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", homePage);
  server.on("/on", switchOn);
  server.on("/off", switchOff);

  server.begin();
  Serial.println("Web server started!");
}

void loop() {
  server.handleClient();
}
