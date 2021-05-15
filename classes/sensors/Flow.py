from classes.sensors.Sensor import Sensor

class Flow(Sensor):
   checked = False
   def __init__(self, s_id, state, volume):
     
      super().__init__(s_id, 'flow', state)
      self.volume = volume

   
   def __str__(self):
      return 'Flow:\n{}\n   Volume: {}'.format(super().__str__(), self.volume)