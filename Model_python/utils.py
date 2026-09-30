import cv2
import numpy as np
import serial
import time
from tensorflow.keras.models import load_model

# Charger le modèle IA
model = load_model('model_drowsiness_detection.h5')

# Connexion série à l'Arduino
try:
    ser = serial.Serial('COM11', 9600) 
    time.sleep(2)
    print("Connexion série Arduino établie.")
except Exception as e:
    ser = None
    print(f"Aucune connexion série Arduino détectée : {e}")

# Fonction principale
def real_time_drowsiness_detection():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Webcam non détectée.")
        return

    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    print("Détection en cours... Appuie sur 'q' pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture caméra.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        state = "Open"

        for (x, y, w, h) in eyes:
            roi = gray[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (64, 64))
            roi_normalized = roi_resized / 255.0
            roi_input = np.reshape(roi_normalized, (1, 64, 64, 1))

            prediction = model.predict(roi_input, verbose=0)[0][0]
            state = "Open" if prediction >= 0.5 else "Closed"
            color = (0, 255, 0) if state == "Open" else (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, state, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            if ser:
                ser.write(b'1' if state == "Closed" else b'0')

            break  # Un seul œil traité

        cv2.imshow('Détection de Somnolence', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Lancer la détection
if __name__ == "__main__":
    real_time_drowsiness_detection()
