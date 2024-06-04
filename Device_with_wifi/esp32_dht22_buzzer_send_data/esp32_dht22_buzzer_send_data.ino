#include <DHT.h>
#include <Adafruit_MLX90614.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "MAX30105.h"
#include "heartRate.h"

DHT dht(18, DHT22);//dht pin 18
int buzzer = 19;//buzzer pin 19
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
float bodyTemp;
int risk;
float humidity;
float temperature;
float heatIndex;
float calibrate_infra = 1.5;
float calibrate_dht = -0.7;
float calibrate_humid = -6.1;

MAX30105 particleSensor;

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred
float bpm;
unsigned long previousTempMillis = 0;
unsigned long previousRiskMillis = 0;
unsigned long previousHeartRatePrintMillis = 0;
unsigned long previousHTTPMillis = 0;
unsigned long previousBuzzerMillis = 0;
unsigned long previousBuzzerMillis2 = 0;
bool buzzerState = false; 
bool buzzerState2 = false; 

const char* ssid = "wifi_name"; // change this to your wifi name 
const char* password = "wifi_password"; // change this to your wifi password 
const char* serverUrl = "http://192.168.xxx.xxx:8000/sensor/receive/"; // change this to your local ip address

void setup()
{
  Wire.begin();
  dht.begin(); 
  mlx.begin();
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  pinMode(buzzer, OUTPUT);

  ledcSetup(0, 5000, 8);
  ledcAttachPin(buzzer, 0);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }
  particleSensor.setup(); //Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  particleSensor.setPulseAmplitudeGreen(0); //Turn off Green LED
  buzzerState = false;
  buzzerState2 = false;
}
 
void loop()
{
  unsigned long currentMillis = millis();

  // Temperature reading interval = 20 sec
  if (currentMillis - previousTempMillis >= 20000) {
    previousTempMillis = currentMillis;

    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    bodyTemp = mlx.readObjectTempC();

    bodyTemp = bodyTemp + calibrate_infra;
    temperature = temperature + calibrate_dht;
    humidity = humidity + calibrate_humid;

    heatIndex = -8.78469475556 + 1.61139411 * temperature + 2.33854883889 
    * humidity - 0.14611605 * temperature * humidity - 0.012308094 * pow(temperature, 2) 
    - 0.0164248277778 * pow(humidity, 2) + 0.002211732 * pow(temperature, 2) * humidity + 0.00072546 
    * temperature * pow(humidity, 2) - 0.000003582 * pow(temperature, 2) * pow(humidity, 2);

    Serial.print("Temp: ");
    Serial.print(temperature, 1);
    Serial.print(" C \n");
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print(" % \n");
    Serial.print("Body Temp: ");
    Serial.print(bodyTemp, 1);
    Serial.print(" C \n");
    Serial.print("Heat Index: ");
    Serial.print(heatIndex, 1);
    Serial.print(" C \n");
  }

  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue) == true)
  {
    long delta = millis() - lastBeat;
    lastBeat = millis();

    bpm = 60 / (delta / 1000.0);

    if (bpm < 255 && bpm > 20)
    {
      rates[rateSpot++] = (byte)bpm; //Store this reading in the array
      rateSpot %= RATE_SIZE; //Wrap variable
    }
  }

  // Heart rate print interval  = 20 sec
  if (currentMillis - previousHeartRatePrintMillis >= 20000) {
    previousHeartRatePrintMillis = currentMillis;

    Serial.print("BPM: ");
    Serial.println(bpm);
    risk = calculateRisk(bpm, bodyTemp, heatIndex);
    Serial.print("Risk: ");
    Serial.println(risk);
    Serial.print("--------------------");
    Serial.println();
  }

  if (risk >= 5 && risk <= 6) {
    //buzzer alarm = 2 sec
    if (currentMillis - previousBuzzerMillis >= 2000) {
      previousBuzzerMillis = currentMillis;  // Update the time
      buzzerState = !buzzerState;  // Toggle the buzzer state

      if (buzzerState) {
        tone(buzzer, 1000);  // Turn the buzzer on
      } else {
        noTone(buzzer);  // Turn the buzzer off
      }  
    }
  } else if (risk >= 7 && risk <= 8) {
    //buzzer alarm = 0.5 sec
    if (currentMillis - previousBuzzerMillis2 >= 500) {
      previousBuzzerMillis2 = currentMillis;  // Update the time
      buzzerState2 = !buzzerState2;  // Toggle the buzzer state

      if (buzzerState2) {
        tone(buzzer, 1000);  // Turn the buzzer on
      } else {
        noTone(buzzer);  // Turn the buzzer off
      }
    }
  } else {
    noTone(buzzer);  // Ensure the buzzer is off if the risk is out of range
    buzzerState = false;  // Reset the buzzer state
    buzzerState2 = false;  // Reset the buzzer state for the other risk level
  }



  if (currentMillis - previousHTTPMillis >= 20000) {
      previousHTTPMillis = currentMillis;

    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"temperature\":" + String(temperature, 1) + 
                      ",\"humidity\":" + String(humidity) + 
                      ",\"bodyTemp\":" + String(bodyTemp, 1) +
                      ",\"bpm\":" + String(bpm) + 
                      ",\"risk\":" + String(risk) + 
                      ",\"user\":\"test4\"}";//change username

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
  }
}

int calculateRisk(float bpm, float bodyTemp, float heatIndex) {
  int risk = 0;

  if (bodyTemp > 37.4 && bodyTemp <= 38.4) {
    risk += 1;
  } else if (bodyTemp > 38.4 && bodyTemp <= 39.4) {
    risk += 2;
  } else if (bodyTemp > 39.4) {
    risk += 3;
  }

  if (heatIndex >= 33 && heatIndex <= 41) {
    risk += 1;
  } else if (heatIndex > 41 && heatIndex <= 51) {
    risk += 2;
  } else if (heatIndex > 51) {
    risk += 3;
  }

  if (bpm >= 101 && bpm <= 120) {
    risk += 1;
  } else if (bpm > 120) {
    risk += 2;
  }

  return risk;
}
