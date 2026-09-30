const int greenLedPin = 7;       // LED verte
const int redLedPin = 8;         // LED rouge
const int buzzerPin = 10;        // Buzzer
const int motorControlPin = 9;   // Moteur (PWM)

int motorSpeed = 0;              // Vitesse actuelle du moteur (0-255)
bool accelerating = false;       // Accélération en cours
bool decelerating = false;       // Décélération en cours

unsigned long previousMillis = 0;
const long interval = 50;        // Intervalle d'accélération/décélération en ms
const int accelerationStep = 5;
const int decelerationStep = 5;

void setup() {
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(motorControlPin, OUTPUT);

  Serial.begin(9600);
  Serial.println("🟢 Système prêt. Moteur en marche...");

  // État initial :
  digitalWrite(greenLedPin, HIGH);    // LED verte allumée
  digitalWrite(redLedPin, LOW);       // LED rouge éteinte

  // Pour le buzzer, teste avec LOW ou HIGH selon ton buzzer:
  digitalWrite(buzzerPin, LOW);       // Buzzer éteint (changer en HIGH si nécessaire)

  motorSpeed = 0;
  analogWrite(motorControlPin, motorSpeed); // Moteur à l'arrêt (0 vitesse)
  
  accelerating = true;   // Commencer à accélérer dès le départ
  decelerating = false;
  previousMillis = millis();
}

void loop() {
  unsigned long currentMillis = millis();

  // Gestion de la décélération progressive
  if (decelerating && currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (motorSpeed > 0) {
      motorSpeed -= decelerationStep;
      if (motorSpeed < 0) motorSpeed = 0;
      analogWrite(motorControlPin, motorSpeed);
      Serial.print("⏬ Décélération: vitesse = ");
      Serial.println(motorSpeed);
    } else {
      decelerating = false;
      Serial.println("🛑 Moteur arrêté");
    }
  }

  // Gestion de l'accélération progressive
  if (accelerating && currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (motorSpeed < 255) {
      motorSpeed += accelerationStep;
      if (motorSpeed > 255) motorSpeed = 255;
      analogWrite(motorControlPin, motorSpeed);
      Serial.print("⏫ Accélération: vitesse = ");
      Serial.println(motorSpeed);
    } else {
      accelerating = false;
      Serial.println("⚡ Moteur à pleine vitesse");
    }
  }

  // Lecture des commandes série
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
     
    if (receivedChar == '1') {
      // Yeux fermés → alerte → décélération
      digitalWrite(greenLedPin, LOW);
      digitalWrite(redLedPin, HIGH);
      digitalWrite(buzzerPin, HIGH);  // Activer le buzzer (alerte)

      decelerating = true;
      accelerating = false;
      previousMillis = currentMillis;

      Serial.println("⚠️ Yeux fermés : Alerte - Décélération en cours");

    } else if (receivedChar == '0') {
      // Yeux ouverts → normal → accélération
      digitalWrite(greenLedPin, HIGH);
      digitalWrite(redLedPin, LOW);
      digitalWrite(buzzerPin, LOW);   // Éteindre le buzzer

      accelerating = true;
      decelerating = false;
      previousMillis = currentMillis;

      Serial.println("✅ Yeux ouverts : Reprise normale - Accélération en cours");

    } else {
      Serial.println("❌ Commande inconnue. Envoyez '1' (yeux fermés) ou '0' (yeux ouverts)");
    }
  }
}
