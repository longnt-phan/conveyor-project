# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:26:07 2024
@author: LongPhan

This file have definitions of four classes:
1. Conveyor
2. RotatingConveyor (built upon Conveyor class | replacing conveyor-and-table group)
3. Sensor
4. Box

"""
import time
##### CLASSES #####
all_conveyors = [] # Global list to store all conveyor instances
all_sensors = []  # Global list to store all sensor instances
all_boxes = []    # Global list to store all box instances

class Conveyor:
    counter = 0  # Class-level counter to keep track of instances

    def __init__(self, length, speed=0.5, conveyor_angle=0.0):
        Conveyor.counter += 1
        self.name = f"Conveyor{Conveyor.counter}"  # Automatic naming
        self.length = length # m
        self.conveyor_angle = conveyor_angle #degree, in world coordinate
        self.speed = speed # m/s
        self.num_sensors = 0 # Number of sensors on the conveyor
        self.sensor_names = [] # Name of all sensors on the conveyors
        self.sensor_locations = [] # Locations of all sensors on the conveyor
        self.statusMove = False # Default status is off
        self.feedConveyor = [] # Feed conveyors that are connected to this conveyor
        self.exitConveyor = [] # Exit conveyors that are connected to this conveyor
        self.width = 0.7 # m | Width of the conveyor. 0.7m by default
        self.num_boxes = 0 # Number of boxes on the conveyor
        self.box_locations = [] # Location of boxes on the conveyor
        all_conveyors.append(self.name) # Adding conveyor name to the conveyor master list 

    def setSpeed(self, speed):
        # This function set speed for the conveyor
        self.speed = speed
        print(f"{self.name}'s speed is set to {speed} m/s")
        
    def setLength(self, length):
        # This function set length of the conveyor
        self.length = length
        print(f"{self.name}'s length is set to {length} m")
        
    def setWidth(self, width):
        # This function set width of the conveyor
        self.width = width
        print(f"{self.name}'s width is set to {width} m")        

    def moveConveyor(self):
        # This function sets the moving status of the conveyor to True
        self.statusMove = True
        print(f"{self.name} starts moving")
    
    def stopConveyor(self):
        # This function sets the moving status of the conveyor to False
        self.statusMove = False
        print(f"{self.name} stops moving")

    def connectExitConveyor(self, conveyor):
        # This function connects an exit conveyor to the existing conveyor
        self.exitConveyor.append(conveyor.name)
        
    def connectFeedConveyor(self, conveyor):
        # This function connects a feed conveyor to the existing conveyor
        self.feedConveyor.append(conveyor.name)
        
    def disconnectExitConveyor(self, conveyor):
        # This function disconnects an exit conveyor to the existing conveyor
        if conveyor.name in self.exitConveyor:
            self.exitConveyor.remove(conveyor.name)
        else:
            print(f"{conveyor.name} is not connected to {self.name} as exit conveyor")
        
    def disconnectFeedConveyor(self, conveyor):
        # This function disconnects a feed conveyor to the existing conveyor
        if conveyor.name in self.feedConveyor:
            self.feedConveyor.remove(conveyor.name)
        else:
            print(f"{conveyor.name} is not connected to {self.name} as feed conveyor")
        
        
class RotatingConveyor(Conveyor):
    def __init__(self, length, speed=1.0, conveyor_angle=0.0, rotation_speed=45):
        super().__init__(length, speed)
        self.rotation_angle = 0 # Default value is 0
        self.rotation_speed = rotation_speed #deg/s
        self.statusRotate = False  # Default status is not rotating

    def rotate(self, rotation_angle):
        # This function simulates the rotating action
        # While rotating, the conveyor's rotate status remains True
        # The status return False when the rotation stops, and the conveyor's angle is updated
        self.rotation_angle = rotation_angle
        if self.statusRotate == True:
            print("Conveyor is still rotating")
        elif self.statusRotate == False:
            self.statusRotate = True
            time.sleep(abs(rotation_angle)/self.rotation_speed) # Simulate rotating time
            self.conveyor_angle += rotation_angle #new angle of the conveyor after rotating
            self.rotation_angle = 0.0 #rotation angle reset.
            self.statusRotate = False
        # print("\n")
            
    def stopRotation(self):
        # This function serves as an emergency action - to stop the conveyor immediately
        self.statusRotate = False
        print(f"{self.name} stops rotating.")
        

class Sensor:
    counter = 0
    def __init__(self, location):
        Sensor.counter += 1
        self.name = f"Sensor{Sensor.counter}"  # Automatic naming
        self.location = location # Location of the sensor on the conveyor 
        self.linked_conveyor = None  # Conveyor that the sensor is placed on
        self.status = False # Status of the conveyor. Return True when there is an object go through and False otherwise
        all_sensors.append(self.name) # Adding sensor name to the sensor master list 
        
    def addSensorToConveyor(self, conveyor):
        # This function links the sensor to a conveyor
        self.linked_conveyor = conveyor
        conveyor.num_sensors += 1
        conveyor.sensor_names.append(self.name)
        conveyor.sensor_locations.append(self.location)
        conveyor.sensor_locations.sort()  # Sort the locations in ascending order
        
    def delete(self):
        # This function deletes the sensor from any conveyor
        if self.linked_conveyor:
            conveyor = self.linked_conveyor
            conveyor.sensor_locations.remove(self.location)
            conveyor.sensor_names.remove(self.name)
            conveyor.num_sensors -= 1
            print(f"Sensor {self.name} removed from {conveyor.name}.")
            del self
        else:
            print("Sensor is not linked to any conveyor.")
        

class Box:
    counter = 0
    def __init__(self, length, width):
        Box.counter += 1
        self.name = f"Box{Box.counter}"  # Automatic naming
        self.length = length # Length of the box
        self.width = width # Width of the box
        self.location = None # Location of the box on the conveyor it is on
        self.linked_conveyor = None # Conveyor that the box is on
        self.frequency = 0 # A time variable associates with the box feed rate. 
        all_boxes.append(self.name) # Adding box name to the box master list 
        
    def addBoxToConveyor(self, conveyor, location):
        # This function adds a box to a conveyor at a given location
        # It first checks if the box size is fit in the conveyor
        # Then it updates its info on the classes box and conveyor.
        if self.length > conveyor.length:
            print(f"{self.name}'s length does not fit the {conveyor.name}'s length ")
        else:
            if self.width > conveyor.width:
                print(f"{self.name}'s width does not fit the {conveyor.name}'s width ")
            else:
                self.linked_conveyor = conveyor
                self.location = location
                conveyor.num_boxes += 1
                conveyor.box_locations.append(self.location)
                conveyor.box_locations.sort()  # Sort the locations in ascending order        
        
    def removeBoxFromConveyor(self, conveyor):
        # This function removes a box from a conveyor
        if self.linked_conveyor != conveyor:
            print("Box must belong to a conveyor before be removed from one")
        else: 
            conveyor.num_boxes -= 1
            conveyor.box_locations.remove(self.location)
            conveyor.box_locations.sort()  # Sort the locations in ascending order        
            self.linked_conveyor = None
            self.location = None