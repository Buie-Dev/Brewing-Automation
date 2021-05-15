
def valve_change_percent(control, value):
   flow_rate_margin = 0.07
   change = 0
   diff = control - value
   if (abs(diff) < flow_rate_margin):
      return 0

   if abs(diff) > 1:
      change = 30
   if abs(diff) > .75:
      change = 15
   elif abs(diff) > .5:
      change = 5
   elif abs(diff) > .3:
      change = 1
   elif abs(diff) > .1:
      change = 1

   if diff < 0:
      return change * -1
   return change

