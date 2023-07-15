import os
import sys
import time

BASE = os.path.dirname(__file__)
if 'PSMOVEAPI_LIBRARY_PATH' not in os.environ:
    os.environ['PSMOVEAPI_LIBRARY_PATH'] = os.path.join("modules", "MoveController", BASE, 'psmoveapi', 'bin')
sys.path.insert(0, os.path.join(BASE, 'bindings', 'python'))
from modules.MoveController.psmoveapi.bindings.python import psmoveapi

class Buttons:
    def __init__(self):
        self.triangle = False
        self.square = False
        self.circle = False
        self.cross = False
        self.move = False
        self.select = False
        self.start = False

class MoveController(psmoveapi.PSMoveAPI):
    def __init__(self):
        super().__init__()
        self.gyro = psmoveapi.Vec3()
        self.acc = psmoveapi.Vec3()
        self.color = psmoveapi.RGB()
        self.trig = 0
        self.buttons = Buttons()

    def UpdateSensors(self):
        self.update()

    def UpdateColor(self, activated):
        if activated:
            self.color = psmoveapi.RGB(0, 1, 1)
        else:
            self.color = psmoveapi.RGB(0, 0, 0)

    def on_connect(self, controller):
        controller.connection_time = time.time()
        print('Controller connected:', controller, controller.connection_time)
        print("Battery: ", controller.battery)

    def on_update(self, controller):
        # sensors
        self.gyro = controller.gyroscope
        self.acc = controller.accelerometer
        self.trig = controller.trigger

        # color
        controller.color = self.color

        # buttons
        if controller.now_pressed(psmoveapi.Button.TRIANGLE): self.buttons.triangle = True
        if controller.now_released(psmoveapi.Button.TRIANGLE): self.buttons.triangle = False
        if controller.now_pressed(psmoveapi.Button.SQUARE): self.buttons.square = True
        if controller.now_released(psmoveapi.Button.SQUARE): self.buttons.square = False
        if controller.now_pressed(psmoveapi.Button.CIRCLE): self.buttons.circle = True
        if controller.now_released(psmoveapi.Button.CIRCLE): self.buttons.circle = False
        if controller.now_pressed(psmoveapi.Button.CROSS): self.buttons.cross = True
        if controller.now_released(psmoveapi.Button.CROSS): self.buttons.cross = False
        if controller.now_pressed(psmoveapi.Button.MOVE): self.buttons.move = True
        if controller.now_released(psmoveapi.Button.MOVE): self.buttons.move = False
        if controller.now_pressed(psmoveapi.Button.SELECT): self.buttons.select = True
        if controller.now_released(psmoveapi.Button.SELECT): self.buttons.select = False
        if controller.now_pressed(psmoveapi.Button.START): self.buttons.start = True
        if controller.now_released(psmoveapi.Button.START): self.buttons.start = False

    def on_disconnect(self, controller):
        print('Controller disconnected:', controller)
