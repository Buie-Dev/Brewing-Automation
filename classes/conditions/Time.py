from classes.conditions.Condition import Condition
import time

class Time(Condition):
   start = 0
   def __init__(self, cond_type, time):
      super().__init__(cond_type)
      self.__seconds = time * 60
      self.remaining = self.__seconds
      
      
   def get_cutoff(self):
      return self.__seconds

   def check_time(self):
      if (time.time() - self.start < self.get_cutoff()):
         self.remaining = time.time() - self.start
         return False
      return True
   
   def start_timer(self):
      if self.start == 0:
         self.start = time.time()