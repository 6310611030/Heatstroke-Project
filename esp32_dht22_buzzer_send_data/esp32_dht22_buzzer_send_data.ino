#include <DHT.h>
#include <Adafruit_MLX90614.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>

DHT dht(18, DHT22);
int buzzer = 19;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

const char* ssid = "Xiaomi 11T";
const char* password = "113333555555";
const char* serverUrl = "http://192.168.51.238:8000/sensor/receive/";

void setup()
{
  Wire.begin();
  dht.begin(); 
  mlx.begin();
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}
 
void loop()
{
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  float bodyTemp = mlx.readObjectTempC();

  Serial.print("Temp: ");
  Serial.print(temperature, 1);
  Serial.print(" C \n");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" % \n");
  Serial.print("Body Temp: ");
  Serial.print(bodyTemp, 1);
  Serial.print(" C \n");

  if (temperature > 30 || humidity > 75) {
    tone(buzzer, 1000);
    delay(1000);
    noTone(buzzer);
  }

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read sensor data");
    delay(1000);
    return;
  }

  HTTPClient http;

  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"bodyTemp\":" + String(bodyTemp) + "}";

  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("HTTP Request failed. Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();

  delay(10000);
}