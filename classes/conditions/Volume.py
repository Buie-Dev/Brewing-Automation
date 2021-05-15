from classes.conditions.Condition import Condition

class Volume(Condition):

   def __init__(self, cond_type, cutoff, pot, element):
      print("Setting volume cond")
      super().__init__(cond_type)
      self.__cutoff = cutoff
      self.__pot = pot
      self.__element = element
   
   def get_cutoff(self):
      return self.__cutoff
   
   def get_pot(self):
      return self.__pot
   
   def get_element(self):
      return self.__element

   def check_volume(self, pots):
      
      if str(self.get_pot()) not in pots:
         return False
      volume = pots[str(self.get_pot())].volume
      if self.get_element() == 'Fill':
         return self.get_cutoff() <= volume
      else:
         return self.get_cutoff() >= volume