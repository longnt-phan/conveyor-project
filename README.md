# conveyor-project
INTRODUCTION
This project represents control code for an automation process - box delivery through a set of conveyors.
The key elements are:
Three conveyors (the 1st and 3rd are perpendicular and connected by the 2nd in the middle),
One rotating table attached to the 2nd conveyor,
and 03 sensors, each placed on a conveyor. 
(In this exercise, the group of Conveyor2 and Table is made to be RotatingConveyor class)

This project was done with the Object-oriented programming (OOP) approach,
combined with the mindset of one developing and using Visual Component software.
Because of this, the code is highly flexible, versatile, and reuseable in many use cases.
For example, one conveyor can have multiple sensors placed on it. 
These sensors are linked to the conveyor they are placed on, and their information
such as their names and locations can be displayed on the conveyor's details.
Another example is that conveyors can have the ability to connect with multiple feed and exit conveyors.
These inbound and outbound connections are one of the conditions to check 
before delivering boxes between two conveyors.

CODE MANAGEMENT AND USAGE
There are three files concerning this project: Models.py, Apis.py, and main.py
1. Models.py includes classes: Conveyor, RotatingConveyor, Sensor, and Box
2. Apis.py includes APIs functions related to classes, plus Info and Safety/Exception-handling functions
3. main.py is case-specific. It includes Control Logic and the main functions.

ASSUMPTION
Some assumptions are made in project:
- The system has no delay
- Sensor detects box precisely at the surface of the box
- Boxes after passing Sensor3 is removed after certain time

CAN BE IMPROVED
The project was completed in a very tight time frame, and the topic is niche in automation field.
Hence, there are certainly many room to improve. Below are just a few:
- Execution of box feeding methods
- Simulation and action functions can be better organized and separated.
- Arrangement of commands. e.g. in class, api, or control logic
- Full and detail description of all files and functions
- Objects management
- Testing for different scenarios to improve the code robustness
- Code generalization
- Code optimization
