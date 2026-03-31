// ===============================
// CONTROL DE 2 MOTORES CON ESP32
// COMANDOS POR SERIAL:
// L = izquierda
// R = derecha
// F = forward / avanzar
// S = stop
// Compatible con Arduino-ESP32 3.x
// ===============================

// -------- Pines puente H --------
#define IN1 14
#define IN2 27
#define ENA 26

#define IN3 25
#define IN4 33
#define ENB 32

// -------- Configuración PWM --------
const int freqPWM = 1000;
const int resolucionPWM = 8;   // 0 a 255

// -------- Potencias --------
int pwmAvance = 160;
int pwmGiro   = 150;

// -------- Variable de comando --------
String comando = "";

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // API nueva de Arduino-ESP32 3.x
  ledcAttach(ENA, freqPWM, resolucionPWM);
  ledcAttach(ENB, freqPWM, resolucionPWM);

  detener();

  Serial.println("ESP32 listo para recibir comandos");
}

void loop() {
  if (Serial.available()) {
    comando = Serial.readStringUntil('\n');
    comando.trim();

    Serial.print("Comando recibido: ");
    Serial.println(comando);

    if (comando == "L") {
      girarIzquierda();
    }
    else if (comando == "R") {
      girarDerecha();
    }
    else if (comando == "F") {
      avanzar();
    }
    else if (comando == "S") {
      detener();
    }
  }
}

void avanzar() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, pwmAvance);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, pwmAvance);

  Serial.println("Accion: AVANZAR");
}

void girarIzquierda() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, 0);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, pwmGiro);

  Serial.println("Accion: GIRAR IZQUIERDA");
}

void girarDerecha() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, pwmGiro);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, 0);

  Serial.println("Accion: GIRAR DERECHA");
}

void detener() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  ledcWrite(ENA, 0);
  ledcWrite(ENB, 0);

  Serial.println("Accion: DETENER");
}