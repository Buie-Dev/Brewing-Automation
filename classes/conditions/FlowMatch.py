from classes.conditions.Condition import Condition
from support import unit_control as control
from threading import Timer

class FlowMatch(Condition):
   __checked = False
   def __init__(self, cond_type, m_id, s_id):
      super().__init__(cond_type)
    
      self.__m_id = m_id
      self.__s_id = s_id
   
   def get_sSensor(self):
      return self.__s_id
   
   def get_mSensor(self):
      return self.__m_id
   
   def get_checked(self):
      return self.__checked
   
   def set_checked(self):
      self.__checked = True
      t = Timer(1.0, self.__timer)
      t.start()
   
   def __timer(self):
      self.__checked = False

   def valve_change_percent(self, flows):
      if self.get_mSensor() not in flows or self.get_sSensor() not in flows:
         return 0
      return control.valve_change_percent(flows[self.get_mSensor()].state, flows[self.get_sSensor()].state)
   
   
