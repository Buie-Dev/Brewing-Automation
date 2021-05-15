
from classes.sensors.Sensor import Sensor

class Temperature(Sensor):

   def __init__(self, s_id, state):
      super().__init__(s_id, 'temp', state)


   def __str__(self):
    
      return 'Temperature:\n{}'.format(super().__str__())



   