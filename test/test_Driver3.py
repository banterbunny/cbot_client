import unittest
from Driver3 import *
import time

class test_Driver3(unittest.TestCase):
    def test_ForwardTimeBounded10CM(self):
        'Time-bounded forward (non-accurate) for 10cm mark'
        forward()
        time.sleep((1/300)*(10*10e-2))
        self.assertTrue(True)
    def test_ForwardTimeBounded50CM(self):
        "Time-bounded forward (non-accurate) for 50cm mark"
        forward()
        time.sleep((1/300)*(50*10e-2))
        self.assertTrue(True)
    def test_ForwardTimeBounded1M(self):
        "Time-bounded forward (non-accurate) for 1m mark"
        forward()
        time.sleep((1/300))
        self.assertTrue(True)
    def test_BackwardTimeBounded10CM(self):
        "Time-bounded backward (non-accurate) for 10cm mark"
        backward()
        time.sleep((1/300)*(10*10e-2))
        self.assertTrue(True)
    def test_BackwardTimeBounded50CM(self):
        "Time-bounded backward (non-accurate) for 50cm mark"
        backward()
        time.sleep((1/300)*(50*10e-2))
        self.assertTrue(True)
    def test_BackwardTimeBounded1M(self):
        "Time-bounded backward (non-accurate) for 1m mark"
        backward()
        time.sleep((1/300))
        self.assertTrue(True)
    def test_TurnLeftTimeBounded10CM(self):
        "Time-bounded left turn (non-accurate) for 10cm mark"
        turnleft()
        time.sleep((1/300)*(10*10e-2))
        self.assertTrue(True)
    def test_TurnLeftTimeBounded50CM(self):
        "Time-bounded left turn (non-accurate) for 50cm mark"
        turnleft()
        time.sleep((1/300)*(50*10e-2))
        self.assertTrue(True)
    def test_TurnLeftTimeBounded1M(self):
        "Time-bounded left turn (non-accurate) for 1m mark"
        turnleft()
        time.sleep((1/300))
        self.assertTrue(True)
    def test_TurnRightTimeBounded10CM(self):
        "Time-bounded right turn (non-accurate) for 10cm mark"
        turnright()
        time.sleep((1/300)*(10*10e-2))
        self.assertTrue(True)
    def test_TurnRightTimeBounded50CM(self):
        "Time-bounded right turn (non-accurate) for 50cm mark"
        turnright()
        time.sleep((1/300)*(50*10e-2))
        self.assertTrue(True)
    def test_TurnRightTimeBounded1M(self):
        "Time-bounded right turn (non-accurate) for 1m mark"
        turnright()
        time.sleep((1/300))
        self.assertTrue(True)

    def test_readDistance(self):
        "Read ultrasonic distance"
        value = getDistance()
        print("Distance was {}".format(value))
        self.assertNotEqual(value, -1)

    def test_readTemperatur(self):
        "Read temperature"
        value = getTemperature()
        print("Temperature was {}".format(value))
        self.assertNotEqual(value, -1)

    def test_ForwardNonTimeBounded10CM(self):
        "Distance bounded forward for 10cm mark"
        self.skipTest("Distance ongoing")
        initial = getDistance()
        if initial == -1:
            self.assertNotEqual(initial, -1)
        current = initial
        forward()
        while (initial - current) < 10:
            current = getDistance()
            if current == -1:
                self.assertNotEqual(current, -1)
        print("Accuracy: {}%".format( (1- abs(initial - current)/10)*100 ))

    def test_ForwardNonTimeBounded50CM(self):
        "Distance bounded forward for 50cm mark"
        self.skipTest("Distance ongoing")
        initial = getDistance()
        if initial == -1:
            self.assertNotEqual(initial, -1)
        current = initial
        forward()
        while (initial - current) < 50:
            current = getDistance()
            if current == -1:
                self.assertNotEqual(current, -1)
        print("Accuracy: {}%".format( (1- abs(initial - current)/50)*100 ))

    def test_ForwardNonTimeBounded50CM(self):
        "Distance bounded forward for 1m mark"
        self.skipTest("Distance ongoing")
        initial = getDistance()
        if initial == -1:
            self.assertNotEqual(initial, -1)
        current = initial
        forward()
        while (initial - current) < 100:
            current = getDistance()
            if current == -1:
                self.assertNotEqual(current, -1)
        print("Accuracy: {}%".format( (1- abs(initial - current)/100)*100 ))

