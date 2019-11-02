// Low Power library that is currently not working properly
//#include <ArduinoLowPower.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>

//----------------------------------------------------------------------------------------------------------------------
// Config
//----------------------------------------------------------------------------------------------------------------------

//Pins
const int ledPin = 7;
const int hallSensorPin = 6;

//Network ssid and password
const char ssid[] = "RaspberryWlan";
const char pass[] = "raspi1234";

//Vehicle type
// 1 - Car
// 2 - Bus
const byte vehicleType = 1;

//Backend ip
const char backendIp[] = "192.168.4.1";
const unsigned int backendPort = 5000;
const unsigned int messageDelay = 1000;

//----------------------------------------------------------------------------------------------------------------------
// Variables
//----------------------------------------------------------------------------------------------------------------------

//Wlan module status
int status = WL_IDLE_STATUS;

//Sensor ticks
volatile unsigned int hallSensorTicks = 0;

//Json Generator. Size calculated with: https://arduinojson.org/v6/assistant/
StaticJsonDocument<38> doc;

//----------------------------------------------------------------------------------------------------------------------
// Setup, Loop, Interrupts
//----------------------------------------------------------------------------------------------------------------------

void setup() {
    //Initialize Serial
    Serial.begin(9600);

    //Wait for Serial
    while (!Serial) {}

    Serial.println(F("Serial is initialized."));

    //Set the led pinMode
    Serial.println(F("Initializing pinModes..."));
    pinMode(ledPin, OUTPUT);
    pinMode(hallSensorPin, INPUT);
    Serial.println(F("PinModes initialized."));

    if (!checkWifi()) {
        while (true) {};
    }

    //Connect to wifi
    connectToWifi();
    printNetworkInformation();

    //Attach Interrupt
    attachInterrupt(digitalPinToInterrupt(hallSensorPin), hallSensorInterrupt, FALLING);
//    LowPower.attachInterruptWakeup(hallSensorPin, hallSensorInterrupt, CHANGE);
}


void loop() {
    delay(messageDelay);
    bool cancelExecution = false;

    unsigned long startTime = millis();

    Serial.println(F("--------------------------------------------------"));
    Serial.print(F("Amount of ticks: "));
    Serial.println(hallSensorTicks);

    //Store the value and remove the amount from the variable
    unsigned int tmpAmountTicks = hallSensorTicks;
    hallSensorTicks -= tmpAmountTicks;

    //If no ticks occurred, stop execution
    if (tmpAmountTicks == 0) {
        Serial.println(F("No hall sensor ticks registered."));
        cancelExecution = true;
    }

    //Check the connection state
    if (!cancelExecution && connectToWifi()) {
        Serial.println(F("New Connection established. Reset values."));
        hallSensorTicks = 0;
        cancelExecution = true;
    }

    //TODO change to !cancleExecution
    if (true) {
        buildJson(vehicleType, tmpAmountTicks);
        Serial.print(F("Generated Json: "));
        serializeJson(doc, Serial);
        Serial.println();
    }

    unsigned long endTime = millis();
    Serial.print("Loop execution time (ms): ");
    Serial.println(endTime - startTime);

}

void hallSensorInterrupt() {
    hallSensorTicks++;
}

//----------------------------------------------------------------------------------------------------------------------
// Private methods
//----------------------------------------------------------------------------------------------------------------------

/**
 * check and print the status of the wifi module.
 * @return true if the wifi module is found and can be used
 */
bool checkWifi() {
    //Check if Wifi module exists
    Serial.println(F("Check status of wifi module..."));
    if (WiFi.status() == WL_NO_MODULE) {
        Serial.println(F("Communication with WiFi module failed! Execution is stopped!"));
        return false;
    } else {
        Serial.println(F("Wifi module found."));
    }

    //Check firmware version
    String fv = WiFi.firmwareVersion();
    if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
        Serial.println(F("Please upgrade the firmware"));
    }

    return true;
}

/**
 * Connect to the specified wifi network.
 * If a connection is already established, the connection process will be skipped
 * @return true if a new connection was made, false if the module was already connected
 */
bool connectToWifi() {
    //True if the a connection has to be made
    bool connectionRequired = false;

    status = WiFi.status();
    while (status != WL_CONNECTED) {
        connectionRequired = true;
        Serial.print(F("Attempting to connect to WPA SSID: "));
        Serial.println(ssid);
        status = WiFi.begin(ssid, pass);
        // wait 10 seconds for connection:
        delay(10000);
    }

    //Print statement only if the connection is new
    if (connectionRequired) {
        Serial.println(F("Connection established."));
    }

    return connectionRequired;
}

/**
 * print the network information
 */
void printNetworkInformation() {
    // print your board's IP address:
    Serial.println();
    Serial.println(F("--- Wifi und Network Information ---"));

    // print the SSID of the network you're attached to:
    Serial.print(F("SSID: "));
    Serial.println(WiFi.SSID());

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print(F("Signal strength (RSSI):"));
    Serial.println(rssi);

    // print the encryption type:
    byte encryption = WiFi.encryptionType();
    Serial.print(F("Encryption Type:"));
    Serial.println(encryption, HEX);
    Serial.println();

    IPAddress ip = WiFi.localIP();
    Serial.print(F("IP Address: "));
    Serial.println(ip);

    Serial.println(F("------------------------------------"));
    Serial.println();
}

/**
 * add the json values in the json document
 * @param id of the vehicle type
 * @param hallSensorTicks the amount of hall sensor ticks
 */
void buildJson(int id, int hallSensorTicks) {
    doc["id"] = id;
    doc["th"] = hallSensorTicks;
}





