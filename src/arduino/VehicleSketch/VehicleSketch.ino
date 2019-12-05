#include <WiFiNINA.h>
#include <ArduinoJson.h>

#define PRINTLN(...)  {if(useSerial) {Serial.println(__VA_ARGS__);}};
#define PRINTLNF(...)  {if(useSerial) {Serial.println(F(__VA_ARGS__));}};
#define PRINT(...)  {if(useSerial) {Serial.print(__VA_ARGS__);}};
#define PRINTF(...)  {if(useSerial) {Serial.print(F(__VA_ARGS__));}};


//----------------------------------------------------------------------------------------------------------------------
// Config
//----------------------------------------------------------------------------------------------------------------------

//True if usb is connected. If not Serial must be disabled
//This can be done manually or automatically in the code
bool useSerial = true;

//Pins
const int ledPin1 = 2;
const int ledPin2 = 3;
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
const unsigned long messageDelay = 1000;

//----------------------------------------------------------------------------------------------------------------------
// Variables
//----------------------------------------------------------------------------------------------------------------------

//Wlan module status
int status = WL_IDLE_STATUS;

WiFiClient client;

//Sensor ticks
volatile unsigned int hallSensorTicks = 0;

//Json Generator. Size calculated with: https://arduinojson.org/v6/assistant/
StaticJsonDocument<38> doc;

//----------------------------------------------------------------------------------------------------------------------
// Setup, Loop, Interrupts
//----------------------------------------------------------------------------------------------------------------------

void setup() {
    //Set the led pinMode
    pinMode(ledPin1, OUTPUT);
    pinMode(ledPin2, OUTPUT);
    pinMode(hallSensorPin, INPUT);

    //Initialize Serial
    useSerial = initializeSerial(useSerial, 2500);

    if (!checkWifi()) {
        while (true) {};
    }

    //Connect to wifi
    connectToWifi();
    printNetworkInformation();

    turnOnLeds(true);
    PRINTLNF("Setup completed. Continue by activating the hall sensor...");
    while (digitalRead(hallSensorPin) == HIGH) {
        delay(1);
    };
    PRINTLNF("Hall sensor activated.");

    //Attach Interrupt
    PRINTLNF("Attaching Interrupts.");
    attachInterrupt(digitalPinToInterrupt(hallSensorPin), hallSensorInterrupt, FALLING);

    PRINTLNF("Starting Loop...");
}

void loop() {
    delay(messageDelay);
    bool cancelExecution = false;

    unsigned long startTime = millis();

    PRINTLNF("--------------------------------------------------");
    PRINTF("Amount of ticks: ");
    PRINTLN(hallSensorTicks);

    //Store the value and remove the amount from the variable
    unsigned int tmpAmountTicks = hallSensorTicks;
    hallSensorTicks -= tmpAmountTicks;

    //If no ticks occurred, stop execution
    if (tmpAmountTicks == 0) {
        PRINTLNF("No hall sensor ticks registered.");
        cancelExecution = true;
    }

    //Check the connection state
    if (!cancelExecution && connectToWifi()) {
        PRINTLNF("New Connection established. Reset values.");
        hallSensorTicks = 0;
        cancelExecution = true;
    }

    //TODO change to !cancelExecution
    if (!cancelExecution) {
        buildJson(vehicleType, tmpAmountTicks);
        PRINTF("Generated Json: ");
        if (useSerial) {
            serializeJson(doc, Serial);
        }
        PRINTLN();

        postSensorData();
    }

    unsigned long endTime = millis();
    PRINTF("Loop execution time (ms): ");
    PRINTLN(endTime - startTime);

}

void hallSensorInterrupt() {
    hallSensorTicks++;
}

//----------------------------------------------------------------------------------------------------------------------
// Private methods
//----------------------------------------------------------------------------------------------------------------------

/**
 * initialize the serial. If no usb connection is made, the process will terminate after the given delay.
 * @param initSerial true if the serial monitor should be initialized. If the value is false, the process will be skipped
 * @param maxDelay the max time in millis to wait for the serial
 * @return true if serial was initialized and can be used
 */
bool initializeSerial(bool initSerial, unsigned long maxDelay) {
    // If useSerial is false, dont initialize Serial
    if (!initSerial) {
        blinkLeds(10, 100);
        return false;
    }

    Serial.begin(9600);
    unsigned long startTime = millis();
    bool toggleLedState = true;

    while (!Serial) {
        if (millis() >= startTime + maxDelay) {
            Serial.end();
            break;
        }

        toggleLedState = toggleLedsAlternately(toggleLedState);
        delay(500);
    }

    //If Serial should be used blink slow 3 times, if not 10 times fast
    if (Serial) {
        PRINTLNF("Serial is initialized.");
        blinkLeds(3, 1000);
        return true;
    } else {
        blinkLeds(10, 100);
        return false;
    }
}

/**
 * toggle the leds alternately
 * @param state the state of the led
 * @return the toggled state
 */
bool toggleLedsAlternately(bool state) {
    if (state) {
        digitalWrite(ledPin1, LOW);
        digitalWrite(ledPin2, HIGH);
    } else {
        digitalWrite(ledPin1, HIGH);
        digitalWrite(ledPin2, LOW);
    }
    return !state;
}

/**
 * turn both leds on or off
 * @param state true if the leds should be turned on
 * @return the inverted state !state
 */
bool turnOnLeds(bool state) {
    if (state) {
        digitalWrite(ledPin1, HIGH);
        digitalWrite(ledPin2, HIGH);
    } else {
        digitalWrite(ledPin1, LOW);
        digitalWrite(ledPin2, LOW);
    }
    return !state;
}

/**
 * blink both leds the given amount of time with the given interval
 * @param amountBlinks the amount how often both leds blink
 * @param interval the time where the leds are on and off
 */
void blinkLeds(int amountBlinks, unsigned int interval) {
    for (int i = 0; i < amountBlinks * 2; i++) {
        turnOnLeds(i % 2 == 0);
        delay(interval);
    }
}

/**
 * check and print the status of the wifi module.
 * @return true if the wifi module is found and can be used
 */
bool checkWifi() {
    //Check if Wifi module exists
    PRINTLNF("Check status of wifi module...");
    if (WiFi.status() == WL_NO_MODULE) {
        PRINTLNF("Communication with WiFi module failed! Execution is stopped!");
        return false;
    } else {
        PRINTLNF("Wifi module found.");
    }

    //Check firmware version
    String fv = WiFi.firmwareVersion();
    if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
        PRINTLNF("Please upgrade the firmware");
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
        PRINTF("Attempting to connect to WPA SSID: ");
        PRINTLN(ssid);
        status = WiFi.begin(ssid, pass);

        // wait 10 seconds for connection and toggle led
        bool ledState = false;
        for (int i = 0; i < 20; i++) {
            ledState = toggleLedsAlternately(ledState);
            delay(500);
        }
    }

    //Print statement only if the connection is new
    if (connectionRequired) {
        PRINTLNF("Connection established.");
        blinkLeds(1, 1000);
    }

    return connectionRequired;
}

/**
 * print the network information
 */
void printNetworkInformation() {
    // print your board's IP address:
    PRINTLN()
    PRINTLNF("--- Wifi und Network Information ---");

    // print the SSID of the network you're attached to:
    PRINTF("SSID: ");
    PRINTLN(WiFi.SSID());

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    PRINTF("Signal strength (RSSI):");
    PRINTLN(rssi);

    // print the encryption type:
    byte encryption = WiFi.encryptionType();
    PRINTF("Encryption Type:");
    PRINTLN(encryption, HEX);
    PRINTLN();

    IPAddress ip = WiFi.localIP();
    PRINTF("IP Address: ");
    PRINTLN(ip);

    PRINTLNF("------------------------------------");
    PRINTLN();
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

/**
 * Post the hall sensor data to the server
 * @return true if the data was sent successfully
 */
bool postSensorData() {
    client.stop();

    if (client.connect(backendIp, backendPort)) {
        PRINTLNF("Connected to server");

        client.println("POST /vehicle HTTP/1.1");
        client.print("Host: ");
        client.println(backendIp);
        client.println("Connection: close");
        client.println("Content-Type: application/json");
        client.print("Content-Length:");
        client.println(measureJson(doc));
        client.println();
        serializeJson(doc, client);
        client.println();

        PRINTLNF("Data sent to server");
        return true;
    } else {
        PRINTLNF("Connection to server failed. Aborting!");
        return false;
    }
}







