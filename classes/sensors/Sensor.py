class Sensor:
    
   
   
   def __init__(self, s_id, sensor, state): 
      self._id = s_id
      self._sensor = sensor
      self.state = state
      
      
   def get_id(self):
      return self._id
   
   def get_sensor(self):
      return self._sensor


   def __str__(self):
      return '   ID: {}\n   State: {}'.format(self.get_id(), self.state)
  