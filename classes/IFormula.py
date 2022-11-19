import time
from jetbot import Robot

class IFormula:
    
    def __init__(self, s):
        print('i-Formula started')
        self.robot = Robot()
        self.status = False
        self.speed = s
    
    def stop(self):
        self.robot.stop()
        self.status = False
        
    def forward(self):
        self.robot.forward(self.speed)
        self.status = True
        
    def backward(self):
        self.robot.backward(self.speed)
        self.status = False
        
    def left(self):
        self.robot.left(self.speed)
        time.sleep(self.speed)
        if self.status:
            self.robot.forward(self.speed)
        else:
            self.robot.stop()
    
    def right(self):
        self.robot.right(self.speed)
        time.sleep(self.speed)
        if self.status:
            self.robot.forward(self.speed)
        else:
            self.robot.stop()
    
    def speedchanged(self, s):
        self.speed = float(s)/10
        print(f'Speed changed to {self.speed}')
