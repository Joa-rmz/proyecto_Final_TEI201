"""Versión simulada de gpiozero para probar agrosafe.py sin Raspberry."""
import random, time
class _Dev:
    def __init__(self,*a,**k): pass
    def __enter__(self): return self
    def __exit__(self,*a): pass
class DigitalOutputDevice(_Dev):
    def __init__(self,*a,**k): self.value=False; self.on_times=[]
    def on(self): self.value=True; self.on_times.append(time.monotonic())
    def off(self): self.value=False
class MotionSensor(_Dev):
    def __init__(self,*a,**k): self.motion_detected=False
class DistanceSensor(_Dev):
    def __init__(self,*a,**k): self.cm=100.0
    @property
    def distance(self): return max(0.0,(self.cm+random.uniform(-1,1)))/100
