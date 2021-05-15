from classes.conditions.Condition import Condition

class Heat(Condition):

   def __init__(self, cond_type, cutoff, sensor, element = 'Heat'):
      super().__init__(cond_type)
      self.__cutoff = cutoff
      self.__sensor = sensor
      self.__element = element
   
   def get_cutoff(self):
      return self.__cutoff
   
   def get_sensor(self):
      return self.__sensor
   
   def get_element(self):
      return self.__element

   def check_temp(self, temps):
      if self.get_sensor() not in temps:
         return False
      state = temps[self.get_sensor()].state
      if self.get_element() == 'Heat':
         return (state >= self.get_cutoff())
      else:
         return (state <= self.get_cutoff())

   def control_temp(self, temps):
     
      if self.get_sensor() not in temps:
         return False
      if temps[self.get_sensor()].state < self.get_cutoff():
         return 1
      elif temps[self.get_sensor()].state > self.get_cutoff():
         return -1
      return 0
   
      
