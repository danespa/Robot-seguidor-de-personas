# Robot-seguidor-de-personas
Robot móvil seguidor de personas con YOLOv8n, Python, ESP32 y Arduino Uno. Detecta la posición del objetivo en la imagen, envía comandos por Bluetooth/UART y controla dos motores con puente H. Integra un HC-SR04 para seguridad de proximidad y maniobras de retroceso.
---

## Objetivo

Desarrollar un robot móvil capaz de seguir a una persona en tiempo real mediante visión artificial, integrando procesamiento de imagen, comunicación inalámbrica y control de motores.

---

## Descripción general del sistema

El sistema está dividido en tres módulos principales:

1. Visión artificial en Python
   - Captura video desde una cámara.
   - Usa YOLOv8n para detectar personas.
   - Calcula la posición horizontal del objetivo dentro de la imagen.
   - Genera comandos:
     - `L` → izquierda
     - `R` → derecha
     - `F` → avanzar

2. Comunicación inalámbrica con ESP32
   - El ESP32 recibe los comandos por Bluetooth.
   - Reenvía los comandos por comunicación serial al Arduino Uno.

3. Control del carro con Arduino Uno
   - El Arduino Uno recibe los comandos seriales.
   - Controla el puente H y los dos motores.
   - Usa el sensor ultrasónico HC-SR04 para medir distancia.
   - Si el obstáculo o persona está demasiado cerca, el carro retrocede y luego continúa con la lógica de seguimiento.

---

## Arquitectura del sistema

Camara -> Python + YOLOv8n -> Bluetooth -> ESP32 -> UART -> Arduino Uno -> Puente H + Motores
                                                              |
                                                              -> HC-SR04
