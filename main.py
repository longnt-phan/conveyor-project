# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:26:07 2024
@author: LongPhan

Technical Assignment
Visual Components's Application for Master Thesis Worker Position

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

"""

from Models import Conveyor, RotatingConveyor, Sensor, Box
from Apis import createConveyor, connectConveyor, setSpeedConveyor, moveConveyor, stopConveyor # import conveyor-related APIs
from Apis import createRotatingConveyor, rotateConveyor # import rotating-conveyor-related APIs
from Apis import createSensor # import sensor-related APIs
from Apis import createBox, addBoxToConveyor, removeBoxFromConveyor, moveToSensor, transitionBox # import box-related APIs
from Apis import getListAllObject, getInfoConveyor, getInfoSensor, getInfoBox

import time


def getInfoAll(c1,c2,c3,s1,s2,s3,b1,b2):
    # This case-specific function prints information of all objects in the given case
    print("--------------------SYSTEM INFO--------------------")
    getInfoConveyor(c1)
    getInfoConveyor(c2)
    getInfoConveyor(c3)
    getInfoSensor(s1)
    getInfoSensor(s2)
    getInfoSensor(s3)
    getInfoBox(b1)
    getInfoBox(b2)
    print("---------------------------------------------------")
    

##### CONTROL LOGIC #####
def condition_transferBox(Conveyor1, Conveyor2, Sensor1, Sensor2):
    # This case-specific function checks all conditions before transfering a box from one conveyor to another conveyor
    
    # Check class correctness
    if not isinstance(Conveyor1, (Conveyor, RotatingConveyor)):
        print("Conveyor1 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(Conveyor2, (Conveyor, RotatingConveyor)):
        print("Conveyor2 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(Sensor1, Sensor):
        print("Sensor1 must be an instance of Sensor")
        return
    if not isinstance(Sensor2, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    
    print("\n")
    print(f"Starts checking box-transfering condition between {Conveyor1.name} and {Conveyor2.name}:")
    if Conveyor1.statusMove != False: # Check if the conveyor belt is moving or not
        print(f"{Conveyor1.name} is moving, stop before transfering")
    elif Conveyor1.statusMove == False:
        print(f"{Conveyor1.name} is not moving")
        if Sensor1.status == False: #Check if there is a box available to transfer
            print(f"Box at {Conveyor1.name} is not available to transfer")
        elif Sensor1.status == True:
            print(f"Box at {Conveyor1.name} is available to transfer")
            if Conveyor2.name not in Conveyor1.exitConveyor: #Check if two conveyor is connected to each other, and if C2 is the exit conveyor of C1
                print(f"{Conveyor1.name} and {Conveyor2.name} is not connected")
            elif Conveyor2.name in Conveyor1.exitConveyor:
                print(f"{Conveyor1.name} and {Conveyor2.name} is connected")
                if Conveyor1.conveyor_angle != Conveyor2.conveyor_angle: # Check if two conveyor is in straight line
                    print(f"{Conveyor1.name} and {Conveyor2.name} are not in a straight line")
                elif Conveyor1.conveyor_angle == Conveyor2.conveyor_angle:
                    print(f"{Conveyor1.name} and {Conveyor2.name} are in a straight line")
                    if Sensor2.status == True: # Check if the destination conveyor is avalible (at S2) to transfer boxes
                        print(f"{Conveyor2.name} is occupied")
                    elif Sensor2.status == False:
                        print(f"{Conveyor2.name} is available")
                        print("All conditions are met to transfer box \n")
                        return True
                    else:
                        print("error")

def transferBox_C1toC2(box1,box2,conveyor1,conveyor2,sensor1,sensor2):
    # This function simulate the box transfering process between conveyor 1 and rotation conveyor 2.
    # It first check the if inital condition is met: both conveyors belt are moving.
    # Then it simulate the box transfering process with time function.
    # The function orders conveyor 2 to stop when the box reaches sensor2.
    # Similarly, it orders conveyor 1 to stop when a new box reaches sensor1.
    # To prevent conveyor1 stops before the box reaches conveyor2,
    # one condidition is set to prevent this scenario, with suggestions to change for the user.
    
    # Check class correctness
    if not isinstance(box1, Box):
        print("box must be an instance of Box")
        return
    if not isinstance(conveyor1, (Conveyor, RotatingConveyor)):
        print("Conveyor1 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(conveyor2, (Conveyor, RotatingConveyor)):
        print("Conveyor2 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(sensor1, Sensor):
        print("Sensor1 must be an instance of Sensor")
        return
    if not isinstance(sensor2, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    
    # Check initial condition: both conveyors are moving
    if not conveyor1.statusMove == True and conveyor2.statusMove == True:
        print("Both {conveyor1.name} and {conveyor2.name} must running")
    else:
        # t1: Time the whole box pass through sensor1 completely
        # t2: Time until new box reach sensor 1. t2 is the dependency of t1
        # t3: Time the box's mid point passing Sensor and reach the end of C1 (or the start of C2)
        # t4: Time box starts travel on Conveyor2 and its surface reaches Sensor 2. t4 is the dependency of t3
        # t1 and t3 start at the same time stamp   
        t1 = box1.length/conveyor1.speed #
        t2 = box1.frequency # 
        t3 = (conveyor1.length - sensor1.location + (box1.length/2))/conveyor1.speed 
        t4 = (sensor2.location - (box1.length/2))/conveyor2.speed # Time box starts travel on C2 and its surface reaches S2

        # Second condition: Prevent conveyor1 stop before box reach conveyor2
        if (t1 + t2) < t3: 
            print(f"New box will reach {sensor1.name} before {box1.name} reach {conveyor2.name}")
            print(f"This will make {conveyor1.name} stop before {box1.name} reach {conveyor2.name}")
            print("Please consider reduce box feeding rate and/or increase the covneyor speed and/or move up the S1 position")
            return None
        elif (t1 + t2) > t3:
            print("\n")
            print(f"Starts transfering {box1.name} from {conveyor1.name} to {conveyor2.name}")
            time.sleep(t3) # Simulate Time box's mid point passing Sensor and reach the end of C1 (or the start of C2)
            transitionBox(box1, conveyor1, conveyor2, 0)
            print(f"{box1.name}'s mid point reached {conveyor2.name}")
            
            if (t1 + t2 - t3) > t4: # meaning box will reach sensor 2 before new box reach sensor 1
                moveToSensor(box1, conveyor2, sensor2) # box reaches sensor2 on conveyor 2, and the conveyor 2 is ordered to stop
                time.sleep(t1 + t2 - t3 - t4)
                addBoxToConveyor(box2, conveyor1, (sensor1.location - (box2.length/2))) # New box2 reach the sensor1 from the feeder
                print(f"{box2.name} reached {sensor1.name} on {conveyor1.name}")
                stopConveyor(conveyor1)
            elif (t1 + t2 - t3) < t4: # meaning new box reach sensor 1 before previous box will reach sensor 2. Same set of action as above, just different order.
                time.sleep(t1 + t2 - t3)
                addBoxToConveyor(box2, conveyor1, (sensor1.location - (box2.length/2)))
                print(f"{box2.name} reached {sensor1.name} on {conveyor1.name}")
                stopConveyor(conveyor1)
                box1.location = conveyor2.speed*(t1 + t2 - t3)
                moveToSensor(box1, conveyor2, sensor2)
        print("\n")
        return

def condition_rotateConveyor_delivery(Conveyor1, rotatingConveyor, Sensor2):
    # This case-specific function checks all conditions before rotating the conveyor 2 to connect with conveyor 3
    
    # Check class correctness
    if not isinstance(Conveyor1, (Conveyor, RotatingConveyor)):
        print(f"{Conveyor1.name} must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(rotatingConveyor, RotatingConveyor):
        print(f"{rotatingConveyor.name} must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(Sensor2, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    
    print(f"Starts checking rotating condition of {rotatingConveyor.name}")    
    if Conveyor1.statusMove != False: # Check if the conveyor belt is moving or not
        print(f"{Conveyor1.name} is moving, stop before rotating {rotatingConveyor.name}")
    elif Conveyor1.statusMove == False:
        print(f"{Conveyor1.name} is not moving")
        if rotatingConveyor.statusMove != False: # Check if the conveyor belt is moving or not
            print(f"{rotatingConveyor.name} is moving, stop before rotating")
        elif rotatingConveyor.statusMove == False:
            print(f"{rotatingConveyor.name} is not moving")
            if Sensor2.status == False:
                print(f"No box detected at {Sensor2.name}")
            elif Sensor2.status == True:
                print(f"Box detected at {Sensor2.name}")
                print(f"All conditions are met to rotate {rotatingConveyor.name}")
                print("\n")
                return True
            else:
                print("error")

def transferBox_C2toC3(box,conveyor1,conveyor2,sensor1,sensor2):
    # This case-specific function simulates the box-transfering process from Conveyor2 to Conveyor3
    # It first simulating the time needed to (1) reach the end of Conveyor2, 
    # (2) reach the Sensor3, and (3) passed through Sensor3 completely
    # It then updates the box information in box and conveyor classes.
    
    # Check class correctness
    if not isinstance(box, Box):
        print("box must be an instance of Box")
        return
    if not isinstance(conveyor1, (Conveyor, RotatingConveyor)):
        print("Conveyor1 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(conveyor2, (Conveyor, RotatingConveyor)):
        print("Conveyor2 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(sensor1, Sensor):
        print("Sensor1 must be an instance of Sensor")
        return
    if not isinstance(sensor2, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    
    print("\n")
    # t0: Time for the whole box pass through sensor1
    # t1: Time for box surface to reach the end of conveyor1
    # t2: Time for box surface reaches sensor2 on conveyor 2. Box's travel speed is set to conveyor2's speed once the box reaches conveyor2 for simplicity.
    # t3: Time for the whole box pass through sensor2. Box's travel speed is set to conveyor2's speed for simplicity.
    # l0 = conveyor1.length - sensor1.location
    # t0 = l0/conveyor1.speed + (box.length - l0)/conveyor2.speed
    t1 = (conveyor1.length - sensor1.location)/conveyor1.speed
    t2 = sensor2.location/conveyor2.speed
    t3 = box.length/conveyor2.speed
    
    print(f"Start transfering {box.name} from {conveyor1.name} to {conveyor2.name}")
    
    time.sleep(t1)
    print(f"{box.name} reached the end of {conveyor1.name}")
    
    time.sleep(t2)
    sensor2.status = True
    print(f"{box.name} reached {sensor2.name}")

    time.sleep(t3*1.1) #+10% time to ensure the box pass through completely
    sensor2.status = False # The whole box pass through sensor2,
    sensor1.status = False # meaning the box also pass through sensor1 completely
    print(f"{box.name} passed through {sensor2.name} completely")
    
    new_box_location = conveyor2.speed*(t2 + t3*1.1) - (box.length/2)
    transitionBox(box, conveyor1, conveyor2, new_box_location)


def condition_postTransfer (sensor1, sensor2, feedConveyor, exitConveyor):
    # This function checks if the box was transfered successfully from Conveyor2 to Conveyor3
    
    if not isinstance(sensor1, Sensor):
        print("Sensor1 must be an instance of Sensor")
        return
    if not isinstance(sensor2, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    if not isinstance(feedConveyor, (Conveyor, RotatingConveyor)):
        print("Conveyor1 must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(exitConveyor, (Conveyor, RotatingConveyor)):
        print("Conveyor2 must be an instance of Conveyor or RotatingConveyor")
        return
    
    # another condition can be added here regarding the set time between
    # two sensors returning True to ensure that the box pass sucessfully
    print("\n")
    if sensor1.status == True:
        print(f"Box is still on {sensor1.linked_conveyor.name}")
    elif sensor1.status == False:
        if sensor2.status == True:
            print(f"Box is still on {sensor2.linked_conveyor.name}")
        elif sensor2.status == False:
            if feedConveyor.statusMove == False:
                print(f"{feedConveyor.name} is already stops")
            elif feedConveyor.statusMove == True:
                if exitConveyor.statusMove == False:
                    print(f"{exitConveyor.name} is already stops")
                elif exitConveyor.statusMove == True:
                    print("All conditions are met")
                    return True

def condition_rotateConveyor_return(rotatingConveyor, sensor):
    # This case-specific function checks all conditions before rotating the conveyor 2 to connect with conveyor 1
    
    # Check class correctness
    if not isinstance(rotatingConveyor, RotatingConveyor):
        print(f"{rotatingConveyor.name} must be an instance of Conveyor or RotatingConveyor")
        return
    if not isinstance(sensor, Sensor):
        print("Sensor2 must be an instance of Sensor")
        return
    
    print(f"Starts checking rotating condition of {rotatingConveyor.name}")    
    if rotatingConveyor.statusMove != False: # Check if the conveyor belt is moving or not
        print(f"{rotatingConveyor.name} is moving, stop before rotating {rotatingConveyor.name}")
    elif rotatingConveyor.statusMove == False:
        print(f"{rotatingConveyor.name} is not moving")
        if sensor.status == True:
            print(f"Box detected at {sensor.name}. Deliver before return")
        elif sensor.status == False:
            print(f"No box detected at {sensor.name}")
            print(f"All conditions are met to rotate {rotatingConveyor.name}")
            print("\n")
            return True
        else:
            print("error")                

##### MAIN PROGRAM #####
def main():
    ### Set up initial prompt ###
    print("Setting up initial objects and conditions")
    ## create instances of components ##
    conveyor1 = createConveyor(length=3,speed=1.5, conveyor_angle=0.0)
    conveyor2r = createRotatingConveyor(length=2, speed=1.5,conveyor_angle=0.0, rotation_speed=45)
    conveyor3 = createConveyor(length=3, speed=1.5, conveyor_angle=90)
    sensor1 = createSensor(conveyor1, 2.8)
    sensor2 = createSensor(conveyor2r, 1.8)
    sensor3 = createSensor(conveyor3, 0.2)
    box1 = createBox(0.5,0.5)
    box2 = createBox(0.5,0.5)
    
    ## connect conveyors ##
    connectConveyor(conveyor1, conveyor2r)
    connectConveyor(conveyor2r, conveyor3)
    
    ## set up conveyor1 moving status ##
    moveConveyor(conveyor1)
    
    ## set up other conditions ##
    setSpeedConveyor(conveyor2r, 1)
    getInfoConveyor(conveyor2r)
    box_frequency = 1.7 # a new box appear after each x second
    box1.frequency = box_frequency
    print("Finish setting up initial objects and conditions \n")
        
    
    ### Simulation ###
    print("Simulation starts")
    
    ## add first box to conveyor 1
    addBoxToConveyor(box1, conveyor1, 0)
        
    # first box reach sensor1
    moveToSensor(box1, conveyor1, sensor1)
          
    # to comment on all process
    # Check condition for box-transfering from conveyor1 to conveyor2 then execute
    if condition_transferBox(conveyor1, conveyor2r, sensor1, sensor2) == True:
        moveConveyor(conveyor2r)
        moveConveyor(conveyor1)
        # Simulate the Box transfering profess, including stopConveyor functions
        transferBox_C1toC2(box1, box2, conveyor1, conveyor2r, sensor1, sensor2)
    else: return False
    
    # Check condition before rotate the conveyor and then execute        
    if condition_rotateConveyor_delivery(conveyor1, conveyor2r, sensor2) == True:
        rotateConveyor(conveyor2r,90)
    else: return False

    # Check if rotation was successful and conditions are met to transfer box
    if condition_transferBox(conveyor2r, conveyor3, sensor2, sensor3) == True:
        moveConveyor(conveyor3)
        moveConveyor(conveyor2r)
        
        # Simulate the box-transfering process, from conveyor2 to conveyor3
        transferBox_C2toC3(box1, conveyor2r, conveyor3, sensor2, sensor3)
    else: return False
    
    # Check if box was successfully delivered from conveyor2 to conveyor3
    if condition_postTransfer(sensor2, sensor3, conveyor2r,conveyor3) == True:
        stopConveyor(conveyor2r)
        stopConveyor(conveyor3)
    else: return False
        
    # Check condition before rotate the conveyor and then execute        
    if condition_rotateConveyor_return(conveyor2r, sensor2) == True:
        rotateConveyor(conveyor2r,-90)
    else: return False
        
    # Box1 is removed from conveyor3, simulating the box being delivered after certain time.
    removeBoxFromConveyor(box1,conveyor3)
    
    # A new box added to conveyor1, simulating a constant flow of box in a simple way.
    box3 = createBox(0.5, 0.5)
    addBoxToConveyor(box3, conveyor1, sensor1.location - box_frequency*conveyor1.speed)
    
    # Check condition be
    if condition_transferBox(conveyor1, conveyor2r, sensor1, sensor2) == True:
        print("Ready to deliver a new box!")
    else: return False
    
    ## info check ###
    print("\n")
    getListAllObject()
    getInfoAll(conveyor1, conveyor2r, conveyor3, sensor1, sensor2, sensor3, box1, box2)

if __name__ == "__main__":
    main()