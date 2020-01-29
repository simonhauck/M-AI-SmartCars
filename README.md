# M-AI-SmartCars

This project is part of the course "Makers Lab - Things that think" at the Flensburg University of Applied Sciences. 
We had the motto "Flensburg goes green" and should use various prototype techniques to develop a physical prototype 
that should influence the behavior of the users to act more environmentally friendly.

Our project consist of two parts:
1. Two toy vehicles, a car and a bus, on which we track the driven distance
2. A tree that represents the environment

Our goal was to show children, and also adults the effects of driving for the environment. 
When the vehicles drive, the environment gets worse and the branches of the tree hang low. After a certain time the 
environment gets better and the tree recovers. Of course the bus had a less bad influence then the car.

See our video for a demonstration... (not yet done)

## How does it work?

### The vehicles
The vehicles are 3D-printed, and contain each an [Arduino MKR 1010 Wifi](https://store.arduino.cc/arduino-mkr-wifi-1010), 
as well as an hall sensor (to be specific the SS 441A), a 3.7V lipo battery and a boost converter. The last one is 
required because the sensor requires 3.7V and with the battery the arduino delivers only 3.3V (even from the 5V pin).
Furthermore the vehicles contain two visible LEDs to act as headlights and indicators for the state of the arduino 
(Two in one :D).
The arduino connects on startup to a wireless network of the raspberry pi, that will be used to control the tree. More
on that later. The hall sensor detects if the vehicle is moving and sends the amount of ticks to the raspberry pi.

### The tree
The tree is controlled by a raspberry pi and contains an  LED strip and 4 servo motors. The raspberry pi also acts as an
access point to which the arduinos connect. The server is programmed in python with the flask framework and offers
a simple api to send the amount of ticks of the hall sensor. Depending on the vehicle type the generated pollution is
calculated and stored. The pollution affects the tree only for x seconds (x can be specified in the config file), after
that the entry will be deleted. 

To represent the state of the environment all stored pollution values are summed up and the hardware (the servo 
motors and the led strip) is set accordingly. Like a puppet, the branches of the tree will be moved up and down with
the servo motors. The led stripe is light up, with red and green according to the pollution.

## Structure of the repository
The for you probably most import folder is the src folder. This one contains
1. The 2d folder contains the .dxf file to create the tree and the box with the laser cutter
2. The 3d folder contains the models for the car and the bus. Note that we did some follow up manual work to screw 
both parts together and mount the sensor.
3. The arduino folder contains the wiring diagram and the sketch for the arduino
4. the and pi folder contains, (i think you could have guessed that) the wiring diagram and the python files.
The development server can be started with 
```python
sudo flask run --host=0.0.0.0
```

The other folders are just some stuff for our presentation etc.








