
class Pot:

   def __init__(self, details):
      self.__id = details['id']
      self.__max = details['maxGal']
      self.__initial = details['iVolume']
      self.__out_sensor = details['outSensor']
      self.__in_sensor = details['inSensor']
      self.__out_valve = details['outValveId']
      self.__in_valve = details['inValveId']
      self.volume = self.__initial
   
   def get_id(self):
      return self.__id
   def get_max(self):
      return self.__max
   def get_initial(self):
      return self.__initial
   def get_out_sensor(self):
      return self.__out_sensor
   def get_in_sensor(self):
      return self.__in_sensor
   def get_out_valve(self):
      return self.__out_valve
   def get_in_valve(self):
      return self.__in_valve
   
   def __str__(self) -> str:
      return "Pot {}: {}".format(self.__id, self.volume)
   
      