# Hand Tracking Sensor

## Server

In my architecture, the server is the Raspberry Pi. The Raspberry Pi and the client need to be connected to the same
internet network.

### Prerequisites

I am running [Raspberry Pi OS](https://www.raspberrypi.com/software/). You will need to install:

- [gpiozero](https://gpiozero.readthedocs.io/en/stable/installing.html) using `sudo apt install python3-gpiozero`
- [PiGPIO](https://abyz.me.uk/rpi/pigpio/)

### Running

To run the server:

- Run `sudo pigpiod` to start the PiGPIO daemon.
- Run `python3 server/server.py` to start the server.

## Client

### Prerequisites

Install [OpenCV](https://opencv.org/) and [MediaPipe](https://developers.google.com/mediapipe) for Python with
`python3 -m pip install -r client/requirements.txt`.

### Running

To calibrate the system, run `python3 client/calibrate.py`.

To run the CV system, run `python3 client/cv.py`.
