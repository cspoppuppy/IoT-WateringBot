# Plant Watering Bot

![WaterBot](https://github.com/cspoppuppy/PlantWatering/blob/master/WaterBot.JPG)

* Automatically water plant on schedule
* Enable extra watering using a switch
* Log watering history



Extended functions - Water detector. When water is running low:
* Prevent pump running 
* Flash LED light
* Send message to mobile (via Twilio)

-------------------------------------------------------------------------------------
## Hardware

* [Raspberry Pi Zero WH](https://thepihut.com/products/raspberry-pi-zero-w) 
* [Water Pump (3-6V, max 200mA)](https://uk.banggood.com/Excellway-Mini-Micro-Submersible-Motor-Pump-Water-Pumps-DC-3-6V-100LH-Low-p-1249338.html?rmmds=search&ID=514182&cur_warehouse=CN) 
* USB to micro USB cable
* Switch
* Transistor (BC109)
* Diode
* Resistors (1x 10kΩ & 1x 220Ω)
* Jumper wires

-------------------------------------------------------------------------------------
## Software

* [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/)
* [BanelaEtcher](https://www.balena.io/etcher/)
* [Putty](https://www.putty.org/)
* [Bonjour](https://support.apple.com/kb/DL999?locale=en_GB)
* [Notepad++](https://notepad-plus-plus.org/downloads/)
* Python (included in Raspian)

-------------------------------------------------------------------------------------
## Implementation

### Step 1: [Setup Raspberry Pi Zero WH](https://github.com/cspoppuppy/PlantWatering/wiki/Setup-Raspberry-Pi-(headless))


### Step 2: [Assemble Circuit](https://github.com/cspoppuppy/PlantWatering/wiki/Assemble-Circuit)


### Step 3: [Control pump using Python](https://github.com/cspoppuppy/PlantWatering/wiki/Control-pump-using-Python)

-------------------------------------------------------------------------------------
## Extended Functions

### Water detector circuit

### [WaterPump_v2.py](https://github.com/cspoppuppy/PlantWatering/blob/master/WaterPump_v2.py)
