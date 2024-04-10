# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:26:07 2024
@author: LongPhan

This file includes APIs related to:
1. Conveyor
2. RotatingConveyor
3. Sensor
4. Box
5. Get information
6. Safety features and Handling exceptions

"""
from Models import Conveyor, RotatingConveyor, Sensor, Box
from Models import all_conveyors, all_sensors, all_boxes

import time

##### APIs #####
## Conveyor Base
def createConveyor(length, speed, conveyor_angle):
    print(f"Creating a {length}m conveyor")
    return Conveyor(length, speed, conveyor_angle)

def removeConveyor(conveyor):
    return # also as input to confirm remove sensors

def moveConveyor(conveyor):
    conveyor.moveConveyor()

def stopConveyor(conveyor):
    conveyor.stopConveyor()

def setSpeedConveyor(conveyor, speed):
    conveyor.setSpeed(speed)
    
def connectConveyor(feedConveyor, exitConveyor):
    # This function connect a feed conveyor to an exit conveyor and updates info of both conveyors
    feedConveyor.connectExitConveyor(exitConveyor)
    exitConveyor.connectFeedConveyor(feedConveyor)
    print(f"{exitConveyor.name} is connected to {feedConveyor.name} as exit conveyor")

def disconnectConveyor(feedConveyor, exitConveyor):
    # This function disconnect a feed conveyor from an exit conveyor and updates info of both conveyors
    feedConveyor.disconnectExitConveyor(exitConveyor)
    exitConveyor.disconnectFeedConveyor(feedConveyor)
    print(f"Exit conveyor - {exitConveyor.name} disconnected from {feedConveyor.name}")


## RotatingConveyor
def createRotatingConveyor(length, speed, conveyor_angle, rotation_speed):
    print(f"Creating a {length}m rotating conveyor")
    return RotatingConveyor(length, speed, conveyor_angle, rotation_speed)

def rotateConveyor(conveyor, angle):
    # This function simulates the rotating action of the rotary conveyor
    # It takes the conveyor instance and the rotation angle,
    # and call the class' functions rotate
    if isinstance(conveyor, RotatingConveyor):
        print(f"{conveyor.name} starts rotating {angle} degree")
        conveyor.rotate(angle)
        print(f"{conveyor.name} finished rotating {angle} degree")
        # conveyor.stopRotation()
        # print("\n")
    else:
        print("Only class RotatingConveyor can rotate \n")


## Sensor
def createSensor(conveyor, location):
    # This function creates and adds a sensor on a conveyor at a given location.
    if location < 0:
        print("Sensor's location must bigger than zero","\n","creating sensor failed","\n")
        return None
    elif location > conveyor.length:
        print("Sensor's location is beyond the conveyor length \ncreating sensor failed \n")
        return None
    else:
        sensor = Sensor(location)
        sensor.addSensorToConveyor(conveyor)
        print(f'{sensor.name} created on {conveyor.name} at location {location}')
        return sensor
    
def deleteSensor(sensor):
    sensor.delete()


## Box
def createBox(box_length, box_width):
    print(f"Box {box_length}(L)x{box_width}(W) created")
    return Box(box_length, box_width)

def addBoxToConveyor(box, conveyor, location):
    # This function create a box on a conveyor at a specific location
    # It checks if the location is suitable, then execute the class function addBoxToConveyor
    # This class function updates the box location, 
    # links the box to the conveyor, and updates the conveyor with all the box's info
     
    print(f"Creating box on {conveyor.name} at location {location}")
    if location < 0:
        print("Box's location must be positive","\n","creating box failed","\n")
        return None
    elif location > conveyor.length:
        print("Box's location is beyond the conveyor length \ncreating box failed \n")
        return None
    else:   
        box.addBoxToConveyor(conveyor, location)
        print(f"{box.name} added to {conveyor.name} at location {location} \n")

def removeBoxFromConveyor(box, conveyor):
    box.removeBoxFromConveyor(conveyor)
    print(f"{box.name} removed from {conveyor.name}")
    
def transitionBox(box, feedConveyor, exitConveyor, new_location):
    box.removeBoxFromConveyor(feedConveyor)
    box.addBoxToConveyor(exitConveyor, new_location)   
    
def moveToSensor(box, conveyor, sensor):
    # This function simulates the process of box being delivered to a sensor by and on a conveyor.
    # It first check if the conveyor is running, then simulate the process using time function.
    # The box starts moving from it location.
    # When the box reaches the sensor, sensor status will return True,
    # and the conveyor is ordered to stop.
    # The function updates the box location on box class and conveyor class.
    
    # Checking class correctness
    if not isinstance(box, Box):
        print("The first object is not of type Box")
        return
    if not isinstance(conveyor, (Conveyor, RotatingConveyor)):
        print("The second object is not of type of Conveyor or RotatingConveyor")
        return
    if not isinstance(sensor, Sensor):
        print("The third object is not of type Sensor")
        return
    
    if conveyor.statusMove == False:
        print("Conveyor must be running")
    elif conveyor.statusMove == True:
        print(f"{box.name} starts moving on {conveyor.name} from location {box.location}")
        t0 = (sensor.location - box.location + (box.length/2))/conveyor.speed # time for box1 to reach sensor1
        conveyor.box_locations.remove(box.location) # remove previous location of box on conveyor
        time.sleep(t0) # simulate travel time
        box.location = sensor.location - (box.length/2) # update new box location on box instance
        conveyor.box_locations.append(box.location) # update new box location on conveyor instance
        sensor.status = True # update sensor status
        print(f"{box.name} reached {sensor.name}")
        stopConveyor(conveyor) # order the conveyor to stop
    
    
### Info
def getListAllObject():
    # This function prints all objects created
    print("List of conveyors:")
    for conveyor in all_conveyors:
        print(conveyor)
        
    print("List of sensors:")
    for sensor in all_sensors:
        print(sensor)
        
    print("List of boxes:")
    for box in all_boxes:
        print(box)

def getInfoConveyor(conveyor):
    # This function prints information of a conveyor
    if isinstance(conveyor, (Conveyor, RotatingConveyor)):
        print('INFO', conveyor.name)
        print('length:', conveyor.length, "m")
        print('Conveyor angle (world coordinate):',conveyor.conveyor_angle, "deg")
        print('Moving status:', conveyor.statusMove)
        print('Speed when moving:', conveyor.speed, "m/s")
        print('Number of sensor:', conveyor.num_sensors)
        print("List of sensor:", conveyor.sensor_names)
        print('Sensor locations:', conveyor.sensor_locations)
        print("Feed conveyors:", conveyor.feedConveyor)
        print("Exit conveyors:", conveyor.exitConveyor)
        print("Number of box:", conveyor.num_boxes)
        print("Box location (mid-point):", conveyor.box_locations)
        if isinstance(conveyor, RotatingConveyor):
            print("Rotation status:", conveyor.statusRotate)
            # print("Rotation angle:", conveyor.rotation_angle, "deg")
            print("Rotation speed:", conveyor.rotation_speed, "deg/s")
            print('\n')
        elif isinstance(conveyor, Conveyor):
            print('\n')
    else:
        print("The object is not of type Conveyor or RotatingConveyor.")
        

def getInfoSensor(sensor):
    # This function prints information of a sensor
    if not isinstance(sensor, Sensor):
        print("The object is not of type Sensor")
        return
    else:
        print('INFO', sensor.name)
        print('Status:', sensor.status)
        print('Linked conveyor:', sensor.linked_conveyor.name)
        print('Location on conveyor:', sensor.location)
        print("\n")
    
def getInfoBox(box):
    # This function prints information of a box
    if not isinstance(box, Box):
        print("The object is not of type of Box")
        return
    else:
        print("INFO", box.name)
        print("Box length", box.length)
        print("Box width", box.width)
        if box.linked_conveyor is not None:
            print("Linked conveyor:", box.linked_conveyor.name)
        else:
            print("Linked conveyor: n/a")
        if box.location is not None:
            print("Location on conveyor (mid-point):", box.location)
        else:
            print("Location on conveyor (mid-point): n/a")
        print("\n")
        

# Safety features and exceptions (to be further developed and finalized)

def timeoutSensor(timeout, sensor, conveyor):
    # This function moniters sensor and stops the conveyor after certain set time if there is no changes in the sensor status.
    # One scenario can be apply for is at sensor1. If after certain time no box reach sensor1,
    # The conveyor1 should automatically stop.
    prev_status = sensor.status
    timeCounterStart = time.time()  # Start the timer before the loop
    #main code here, monitoring sensor status

    while (time.time() - timeCounterStart) < timeout:  # Check if the timeout hasn't elapsed
        if sensor.status != prev_status:
            # Reset the timer if there's a change in sensor status
            timeCounterStart = time.time()
            prev_status = sensor.status
        else:
            # If the timeout elapses without any change in status, stop the conveyor
            if (time.time() - timeCounterStart) > timeout:
                stopConveyor(conveyor)
                print(f"No box detected at {sensor} after {timeout}s. Conveyor {conveyor} stopped due to timeout")
                break  # Exit the loop after stopping the conveyor
    
#accident sensor True. Time windows
def debounce_sensor(sensor, time_window):
    # This function handles scenarios where the sensor status briefly turns true but should be considered noise.
    # It ignores brief changes in the sensor status that occur within a specified time window.
    # It is useful in scenarios where workers can sometimes accidentally drop items on the sensor, 
    # making it return True for a very short period of time
    
    # Detail explaination of the function:
    # time_window represents the duration within which changes in sensor status are ignored.
    # The function continuously checks the sensor status in a loop.
    # If the sensor status changes, the timer is reset (start_time = current_time) to start counting from the moment of the status change.
    # If the sensor status remains true for the specified time_window, it returns True, indicating a valid detection.
    # If the sensor status is false or changes before the time_window elapses, it immediately returns False, indicating that the detection should be ignored as noise.
    start_time = time.time()
    prev_status = sensor.status

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if sensor.status != prev_status:
            # Reset the timer if there's a change in sensor status
            start_time = current_time
            prev_status = sensor.status

        if sensor.status:
            # If the sensor status is true, check if it has remained true for the time window
            if elapsed_time >= time_window:
                return True
        else:
            # If the sensor status is false, immediately return false
            return False

