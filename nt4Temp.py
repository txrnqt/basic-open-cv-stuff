#!/usr/bin/env python3
import ntcore
import time
import numpy as np
import cv2 as cv
from enum import Enum
import os

class pose3D: 
    def __init__(self, x, y, z, theata):
        x: float
        y: float
        z: float
        theata: float

inst = ntcore.NetworkTableInstance.getDefault()
table = inst.getTable("gamePeiceFind")
algaePose = table.getDoubleTopic("algaePose").publish(pose3D(0.0, 0.0, 0.0, 0.0))
isConnected = table.getBooleanTopic("isConnected").publish(True)
inst.startClient4("gamePeiceFind")
inst.setServerTeam(5572)

while True:
    algaePose.set(pose3D(0.0,0.0,0.0,0.0))
    isConnected.set(True)