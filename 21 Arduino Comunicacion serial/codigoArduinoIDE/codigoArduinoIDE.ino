#include <DHT.h>

const int led = 12;
const int led2 = 13;
const int led3 = 9;
const int led4 = 10;
const int led5 = 11;

const int dhtPin = 4;  // Pin al que está conectado el sensor de temperatura


void setup() {
  Serial.begin(9600);
}

void loop() {
  // Lectura de entrada
  int valorEntrada = analogRead(A0);
  Serial.print("Entrada: ");
  Serial.println(valorEntrada);

  // Algo de lógica y operaciones...

  // Envío de salida
  int valorSalida = 42;  // Puedes poner aquí el valor que desees
  Serial.print("Salida: ");
  Serial.println(valorSalida);

  delay(1000);  // Puedes ajustar el tiempo de espera según tus necesidades
}


DHT dht(dhtPin, DHT11);

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);

  dht.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String option = Serial.readStringUntil('\r');
    String rgb = Serial.readStringUntil('\r');

    if (option == "rojo") {
      digitalWrite(led, HIGH);
      delay(200);
      digitalWrite(led, LOW);
    }
    
    if (option == "azul") {
      digitalWrite(led2, HIGH);
      delay(200);
      digitalWrite(led2, LOW);
    }
    
    if (option == "amarillo") {
      // Establecer un color amarillo personalizado
      analogWrite(led3, 255);    // Rojo al máximo brillo
      analogWrite(led4, 233);   // Azul con una intensidad personalizada
      analogWrite(led5, 0);
      delay(200);

      // Apagar el LED después de un tiempo
      analogWrite(led3, 0);
      analogWrite(led4, 0);
    }

    if (option == "temperatura") {
      // Leer la temperatura del sensor
      float temperatura = dht.readTemperature();
      
      // Mostrar la temperatura en el Monitor Serie
      Serial.print("Temperatura: ");
      Serial.print(temperatura);
      Serial.println(" °C");
    }

    if (option == "humedad") {
      // Leer la humedad del sensor
      float humedad = dht.readHumidity();
      
      // Mostrar la humedad en el Monitor Serie
      Serial.print("Humedad: ");
      Serial.print(humedad);
      Serial.println(" %");
    }
    int r, g, b;
    if (sscanf(rgb.c_str(), "%d,%d,%d", &r, &g, &b) == 3) {
      // Ajustar los pines LED con los valores RGB
      analogWrite(led3, r);
      analogWrite(led4, g);
      analogWrite(led5, b);
      delay(200);
      analogWrite(led3, 0);
      analogWrite(led4, 0);
      analogWrite(led5, 0);


}
}
}
