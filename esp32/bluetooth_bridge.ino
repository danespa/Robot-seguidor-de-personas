#include <Arduino.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;
HardwareSerial EnlaceUNO(2);   // UART2

const int TX_UNO = 21;         // D21 / GPIO21

void setup() {
  Serial.begin(115200);

  // Bluetooth Classic SPP
  SerialBT.begin("RobotBT");

  // UART2 usando solo TX en GPIO21
  EnlaceUNO.begin(9600, SERIAL_8N1, -1, TX_UNO);

  Serial.println("ESP32 listo");
  Serial.println("Bluetooth: RobotBT");
  Serial.println("Enviando al Arduino por D21");
}

void loop() {
  if (SerialBT.available()) {
    String cmd = SerialBT.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();

    if (cmd == "L" || cmd == "R" || cmd == "F") {
      EnlaceUNO.write(cmd[0]);   // manda solo el caracter
      Serial.print("Enviado al UNO: ");
      Serial.println(cmd);
    } else if (cmd.length() > 0) {
      Serial.print("Comando ignorado: ");
      Serial.println(cmd);
    }
  }
}