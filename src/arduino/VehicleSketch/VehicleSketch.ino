// Low Power library that is currently not working properly
//#include <ArduinoLowPower.h>
#include <WiFiNINA.h>

//----------------------------------------------------------------------------------------------------------------------
// Pins
//----------------------------------------------------------------------------------------------------------------------

const int ledPin = 7;
const int hallSensorPin = 6;

//----------------------------------------------------------------------------------------------------------------------
// Wlan Config
//----------------------------------------------------------------------------------------------------------------------

//Network ssid and password
char ssid[] = "RaspberryWlan";
char pass[] = "raspi1234";

//----------------------------------------------------------------------------------------------------------------------
// Variables
//----------------------------------------------------------------------------------------------------------------------

//Wlan module status
int status = WL_IDLE_STATUS;

volatile int hallSensorTicks = 0;

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
    Serial.print(F("Total amount of ticks: "));
    Serial.println(hallSensorTicks);
    delay(1000);
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

