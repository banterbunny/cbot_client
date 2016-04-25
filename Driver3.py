#!/usr/bin/python3
"""
The Driver3 module
This handles definitions on how to move the Arduino/PBOT jr

Example usage:
>>> import Driver3
>>> forward() # Move the machine forward
>>> backward() # Move the machine backward
>>> turnleft() # Turn the machine to the left
>>> turnright() # Turn the machine to the right
>>> halt() # Stop all motor
>>> getBearing() # Returns bearing in degrees
>>> getDistance() # Returns distance in cm
>>> getTemperature() # Returns ambient temperature
"""
import RPi.GPIO as GPIO
import serial
import smbus
import ctypes
import math

# Disable warnings
GPIO.setwarnings(False)

# Prepare GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

# Prepare serial comm
serialcomm = serial.Serial('/dev/ttyAMA0', timeout=1)

# Prepare I2C
smb = smbus.SMBus(1)

smb.write_byte_data(0x1e, 0x00, 0x18)
smb.write_byte_data(0x1e, 0x01, 0x20)
smb.write_byte_data(0x1e, 0x02, 0x00)


def getBearing():
    """
    Read I2C compass and compute for the heading vector
    :return: Bearing in degrees
    """

    # Get bytes from the I2C compass
    xu = smb.read_byte_data(0x1e, 0x03)
    xl = smb.read_byte_data(0x1e, 0x04)
    zu = smb.read_byte_data(0x1e, 0x05)
    zl = smb.read_byte_data(0x1e, 0x06)
    yu = smb.read_byte_data(0x1e, 0x07)
    yl = smb.read_byte_data(0x1e, 0x08)

    # Bit shift higher bytes and add lower bytes to get value
    x = (xu << 8) + xl
    y = (yu << 8) + yl
    z = (zu << 8) + zl

    # Convert bytes to signed integer (Convert from two's compliment)
    x = ctypes.c_short(x).value
    y = ctypes.c_short(y).value
    z = ctypes.c_short(z).value

    # Compute for vector's angle using its component
    t = math.atan2(y, z) * (180 / math.pi)
    t += 180
    
    return {"x": x, "y": y, "z": z, "t": t}


def getDistance():
    """
    Reads bytes from serial ultrasonic sensor
    :return: The distance from a distant object to the ultrasonic sensor
    """
    serialcomm.write(b'U')
    msb = serialcomm.read()
    lsb = serialcomm.read()
    if msb == b'' or lsb == b'':
        return -1
    distance = (ord(msb) * 256 + ord(lsb)) / 10

    # Recalibrate reading by including temparature
    #  First lets get the constant for STP 20 celsius
    cSTP = 331.3 + (0.606 * 20)
    #  Then get the constant for current temperature
    serialcomm.write(b'P')
    temp = serialcomm.read()
    if temp == b'':
        temp = 20
    else:
        temp = ord(temp) - 45
    cTmp = 331.3 + (0.606 * temp)
    #  Compute for correction factor
    factor = 1 #cTmp / cSTP
    print("Temperature: {}C\nCorrection Factor: {}".format(temp, factor))

    return distance * factor


def getTemperature():
    """
    Reads bytes from serial ultrasonic sensor
    :return: Temperature in degrees
    """
    serialcomm.write(b'P')
    temp = serialcomm.read()
    if temp == b'':
        return -1
    temp = ord(temp) - 45
    return temp


def onLED():
    """
    Turns on indication LED
    :return: None
    """
    GPIO.output(12, GPIO.HIGH)


def offLED():
    """
    Turns off indication LED
    :return:
    """
    GPIO.output(12, GPIO.LOW)


def forward():
    GPIO.output(10, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)


def backward():
    GPIO.output(10, GPIO.LOW)
    GPIO.output(9, GPIO.HIGH)
    GPIO.output(11, GPIO.LOW)


def turnleft():
    GPIO.output(10, GPIO.LOW)
    GPIO.output(9, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)


def turnright():
    GPIO.output(10, GPIO.HIGH)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)


def halt():
    GPIO.output(10, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)


def leftSense():
    return GPIO.input(17)


def centerSense():
    return GPIO.input(27)


def rightSense():
    return GPIO.input(22)
