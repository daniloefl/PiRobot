import RPi.GPIO as GPIO
import time

class Robot:
  def __init__(self):
    self.pinMotorAForwards = 10
    self.pinMotorABackwards = 9
    self.pinMotorBForwards = 8
    self.pinMotorBBackwards = 7

    self.pinTrigger = 17
    self.pinEcho = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # set the GPIO pin mode
    GPIO.setup(self.pinMotorAForwards, GPIO.OUT)
    GPIO.setup(self.pinMotorABackwards, GPIO.OUT)
    GPIO.setup(self.pinMotorBForwards, GPIO.OUT)
    GPIO.setup(self.pinMotorBBackwards, GPIO.OUT)

    GPIO.setup(self.pinTrigger, GPIO.OUT)
    GPIO.setup(self.pinEcho, GPIO.IN)

    self.stop()

  # turn all motors off
  def stop(self):
    GPIO.output(self.pinMotorAForwards, 0)
    GPIO.output(self.pinMotorABackwards, 0)
    GPIO.output(self.pinMotorBForwards, 0)
    GPIO.output(self.pinMotorBBackwards, 0)

  # all motors forwards
  def forwards(self):
    GPIO.output(self.pinMotorAForwards, 1)
    GPIO.output(self.pinMotorABackwards, 0)
    GPIO.output(self.pinMotorBForwards, 1)
    GPIO.output(self.pinMotorBBackwards, 0)

  # all motors backwards
  def backwards(self):
    GPIO.output(self.pinMotorAForwards, 0)
    GPIO.output(self.pinMotorABackwards, 1)
    GPIO.output(self.pinMotorBForwards, 0)
    GPIO.output(self.pinMotorBBackwards, 1)

  # turn left
  def left(self):
    GPIO.output(self.pinMotorAForwards, 0)
    GPIO.output(self.pinMotorABackwards, 1)
    GPIO.output(self.pinMotorBForwards, 1)
    GPIO.output(self.pinMotorBBackwards, 0)

  # turn right
  def right(self):
    GPIO.output(self.pinMotorAForwards, 1)
    GPIO.output(self.pinMotorABackwards, 0)
    GPIO.output(self.pinMotorBForwards, 0)
    GPIO.output(self.pinMotorBBackwards, 1)

  def distance(self):
    # set trigger low
    GPIO.output(self.pinTrigger, False)
    time.sleep(0.5)

    # send 10 us pulse to trigger
    GPIO.output(self.pinTrigger, True)
    time.sleep(10e-6)
    GPIO.output(self.pinTrigger, False)

    # count delay in echo
    StartTime = time.time()

    # wait until echo is high to start counting
    while GPIO.input(self.pinEcho) == 0:
      StartTime = time.time()

    # stop counting when echo goes low
    while GPIO.input(self.pinEcho) == 1:
      StopTime = time.time()
      # if the sensor is too close, the echo is not captured
      # escape this
      if StopTime - StartTime >= 40e-3:
        #print("Too close!")
        StopTime = StartTime
        break
    # Calculate echo delay
    ElapsedTime = StopTime - StartTime
    # Estimate distance assuming sound speed in air
    Distance = ElapsedTime * 343.26 # m/s
    # Divide by two, since it will travel back and forwards
    Distance *= 0.5
    time.sleep(0.5)
    return Distance


  def cleanup(self):
    GPIO.cleanup()
  
