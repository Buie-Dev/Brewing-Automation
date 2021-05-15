from classes.conditions.Condition import Condition

class AfterStage(Condition):

   def __init__(self, cond_type, stage_id):
      super().__init__(cond_type)
      self.__stage_id = stage_id

   def get_after_stage(self):
      return self.__stage_id
   
   def check_after_stage(self, stages):
      for stage in stages:
         if stage.get_id() == self.get_after_stage():
            return stage.completed