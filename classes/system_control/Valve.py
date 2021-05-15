from classes.system_control.Unit import Unit


class Valve(Unit):
   def __init__(self, p_id, content):
      super().__init__(p_id, content['state'])

   