import cv2
import serial
import time
from ultralytics import YOLO

# =========================
# CONFIGURACIÓN
# =========================
MODELO = "yolov8n.pt"
CAMERA_INDEX = 0
CONF_MIN = 0.5
CLASE_PERSONA = 0
ZONA_MUERTA = 80

PUERTO_ESP32 = "COM8"   # CAMBIA esto por el puerto real de tu ESP32
BAUDIOS = 115200

# =========================
# INICIALIZACIÓN
# =========================
model = YOLO(MODELO)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

try:
    ser = serial.Serial(PUERTO_ESP32, BAUDIOS, timeout=1)
    time.sleep(2)  # tiempo para que el ESP32 reinicie
    print(f"Conectado al puerto {PUERTO_ESP32}")
except Exception as e:
    print(f"No se pudo abrir el puerto serial: {e}")
    cap.release()
    exit()

ultimo_comando = ""

def enviar_comando(cmd):
    global ultimo_comando
    if cmd != ultimo_comando:
        ser.write((cmd + "\n").encode())
        ultimo_comando = cmd
        print("Enviado:", cmd)

# =========================
# BUCLE PRINCIPAL
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame.")
        break

    alto, ancho = frame.shape[:2]
    centro_imagen = ancho // 2

    resultados = model(frame, verbose=False)

    mejor_persona = None
    mejor_score = -999999

    for r in resultados:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0].item())
            conf = float(box.conf[0].item())

            if cls == CLASE_PERSONA and conf >= CONF_MIN:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                ancho_box = x2 - x1
                alto_box = y2 - y1
                area = ancho_box * alto_box

                # filtro mínimo
                if area < 5000 or alto_box < 120:
                    continue

                x_centro = (x1 + x2) // 2
                dist_centro = abs(x_centro - centro_imagen)

                # favorece cajas grandes y cercanas al centro
                score = area - 25 * dist_centro

                if score > mejor_score:
                    mejor_score = score
                    mejor_persona = (x1, y1, x2, y2, conf)

    direccion = "BUSCANDO"
    comando = "S"

    if mejor_persona is not None:
        x1, y1, x2, y2, conf = mejor_persona

        x_persona = (x1 + x2) // 2
        y_base = y2
        error_x = centro_imagen - x_persona

        if error_x > ZONA_MUERTA:
            direccion = "IZQUIERDA"
            comando = "L"
        elif error_x < -ZONA_MUERTA:
            direccion = "DERECHA"
            comando = "R"
        else:
            direccion = "CENTRO"
            comando = "F"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (x_persona, (y1 + y2)//2), 5, (0, 0, 255), -1)
        cv2.circle(frame, (x_persona, y_base), 7, (255, 0, 255), -1)

        cv2.putText(frame, f"Persona {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, f"Error X: {error_x}", (10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    enviar_comando(comando)

    cv2.line(frame, (centro_imagen, 0), (centro_imagen, alto), (255, 0, 0), 2)
    cv2.line(frame, (centro_imagen - ZONA_MUERTA, 0), (centro_imagen - ZONA_MUERTA, alto), (255, 255, 0), 1)
    cv2.line(frame, (centro_imagen + ZONA_MUERTA, 0), (centro_imagen + ZONA_MUERTA, alto), (255, 255, 0), 1)

    cv2.putText(frame, f"Direccion: {direccion}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, f"Comando: {comando}", (10, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("YOLOv8 + Serial + Camara Laptop", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()