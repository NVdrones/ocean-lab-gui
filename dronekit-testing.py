#setup drone kit
import dronekit
import time

vehicle = connect('com12', baud=57600, wait_ready=true)

print("Basic pre-arm checks")
# Don't try to arm until autopilot is ready
while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)

print("Arming motors")
# Copter should arm in GUIDED mode
vehicle.mode    = VehicleMode("GUIDED")
vehicle.armed   = True

# Confirm vehicle armed before attempting to take off
while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)


print("armed that shit")

vehicle.armed = False

while vehicle.armed:
	print("waiting to disarm")
	time.sleep(1)

print("disarmed that shit")