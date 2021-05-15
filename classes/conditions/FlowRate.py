from support import unit_control as control
from classes.conditions.Condition import Condition
from threading import Timer

class FlowRate(Condition):
   __checked = False
   def __init__(self, cond_type, cutoff, sensor, element = "Increase"):
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

   def get_checked(self):
      return self.__checked
   
   def set_checked(self):
      self.__checked = True
      t = Timer(1.0, self.__timer)
      t.start()
   
   def __timer(self):
      self.__checked = False
   
   def check_flow(self, flows):
      if self.get_sensor() not in flows:
         return False
      state = flows[self.get_sensor()].state

      if self.get_element() == 'Increase':
         return (state >= self.get_cutoff())
      else:
         return (state <= self.get_cutoff())
   
   def valve_change_percent(self, flows): 
      if self.get_sensor() not in flows:
         return 0
      return control.valve_change_percent(self.get_cutoff(), flows[self.get_sensor()].state)
    
  