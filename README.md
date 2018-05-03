# 15-112-Term-Project

This is my term project for 15-112 Fundamentals of Programming and Computer Science, Spring 2018, at Carnegie Mellon University. This project uses a Leap Motion for theatrical lighting control. Users can move their hands to change the intensity, color, and position of lights. Sequences can be recorded and played back. This is implemented with the grandMA2 lighting console and software.

### Requirements

* Python 2.7
* [grandMA2 console](http://www.malighting.com/)
* [Leap Motion SDK](https://developer.leapmotion.com/sdk/v2/)
* [Leap Motion App](https://www.leapmotion.com/setup/desktop/osx)
* [RtMidi-python](https://github.com/superquadratic/rtmidi-python)

### Instructions

Connect the Leap Motion via USB, and connect the grandMA2 over Ethernet or MIDI cable. 

Run init.py. Lights can be added by clicking the buttons in the 'add new' column. The different options are for different types of lights: 'light' will allow access to only the intensity, so can be used for any light on a dimmer, 'intelligent' adds RGB color mixing for LEDs, and 'moving' adds control of position values for moving lights. 

Lights can now be controlled by selecting the light, and selecting the attribute you would like to change. The text in the middle of the screen shows the values for the current light. After selecting 'intensity', raise and lower your hand over the Leap Motion to control the intensity value. After selecting 'color', raise your hand with your fingertips pointing towards the computer screen. Twist your wrist to fade through a rainbow of colors and select the color you want. After selecting 'position', point with your index finger in a direction, and the moving lights will match the direction. 

To begin recording a sequence, press 'r'. Then change any lights that you want. To finish recording, press 'r' again. The sequence will appear with a number, click the number to play the sequence again. 