from m5stack import *
from m5ui import *
from uiflow import *
lcd.setRotation(0)
import imu
import time
import hat

setScreenColor(0x000000)

hat_bugc0 = hat.get(hat.BUGC)

Power = None
Enable = None
Kp = None
Target = None
Ki = None
Kd = None
I = None
PreP = None
PreTime = NoneNow = None
Time = None
Dt = None
P = None
D = None

imu0 = imu.IMU()


def buttonA_wasPressed():
  global Power, Enable, kp, Target, Ki, Kd, I, PreP, PreTime, Now, Time, Dt, P, D
  if Enable == 0:
    Enable = 1
    #Target = imu0.ypr[1]
    Target = -94.16
  
  else:
    Enable = 0
  pass
btnA.wasPressed(buttonA_wasPressed)


axp.setLcdBrightness(0)
Enable = 0
Kp = 14
Ki = 14
Kd = 0.003

Power = 0
I = 0
PreP = 0
PreTime = time.ticks_ms()
while True:
  if Enable == 1:
    Now = Target - (imu0.ypr[1])
    if -60 < Now and Now < 60:
      Time = time.ticks_ms()
      Dt = (Time - PreTime) / 250
      PreTime = Time
      P = Now / 90
      I = I + P * Dt
      D = (P - PreP) / Dt
      PreP = P
      Power = Kd * D + Kp * P + Ki * I
      Power = Power * 25
      hat_bugc0.SetAllPulse(Power * -1, Power, 0, 0)
      #if abs(I) > 1:
      #  I = 0
      M5Led.on()
    else:
      Power = 0
      I = 0
      hat_bugc0.SetAllPulse(0, 0, 0, 0)
      M5Led.off()
  else:
    hat_bugc0.SetAllPulse(0, 0, 0, 0)
    M5Led.off()