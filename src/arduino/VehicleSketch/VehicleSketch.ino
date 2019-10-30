
const int ledPin = 0;

void setup() {
    //Initialize Serial
    Serial.begin(9600);

    //Wait for Serial
    while (!Serial) {}

    Serial.println(F("Serial is initialized."));

    //Set the led pinMode
    pinMode(ledPin, OUTPUT);
}

void loop() {
    // put your main code here, to run repeatedly:
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
}
