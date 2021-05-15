import time
import requests
import json
from support import config
from support import mqtt
from classes.sensors.Temperature import Temperature
from classes.sensors.Flow import Flow
from classes.sensors.Pot import Pot
from classes.conditions.FlowRate import FlowRate
from classes.conditions.Heat import Heat
from classes.conditions.Time import Time
from classes.conditions.FromStart import FromStart
from classes.conditions.AfterStage import AfterStage
from classes.system_control.Valve import Valve
from classes.system_control.Plug import Plug
from classes.Stage import Stage


def check_internet():
    print('Checking Internet Connection...', end='')
    url='http://www.google.com/'
    timeout=5

    while True:
        try:
            _ = requests.get(url, timeout=timeout)
            print('Connected')
            return True
        except requests.ConnectionError:
            print('Not Connected')
            print('Waiting 5 and retry')
            time.sleep(timeout)

def set_temp(content, temps):
    s_id = content['id']
    state = content['value']
    if s_id not in temps:
        temps[s_id] = Temperature(s_id, state)
    else:
        temps[s_id].state = state
def set_flow(content, flows, pots):
    
    s_id = content['id']
    rate = content['rate']
    if s_id not in flows:
        flows[s_id] = Flow(s_id, rate, content['volume'])
    else:
        flows[s_id].state = rate
        flows[s_id].volume = content['volume']
    set_volume(s_id, rate, pots)

def set_volume(s_id, rate, pots):

    gal = .264
    for key, pot in pots.items():
        if pot.get_in_sensor() == s_id:
            pot.volume += (rate / 60 * gal)
        elif pot.get_out_sensor() == s_id:
            pot.volume -= (rate / 60 * gal)
        print(pot)
def set_plugs(content, plugs):
   for key, value in content.items():
      if key in plugs:
         plugs[key].state = value['state']
      else:
         plugs[key] = Plug(key, value)
def set_valves(content, valves):
   for key, value in content.items():
      if key in valves:
         valves[key].state = value['state']
      else:
         valves[key] = Valve(key, value)
def set_pots(data, pots):
    for key, value in data.items():
        pots[key] = (Pot(value))  
def set_autorun(content, stages, pots):
    stages.clear()
    if content['stagesNum'] == 0:
        pots.clear()
        return
    
    set_pots(content['pots'], pots)
    for key, value in content["stages"].items():
        stages.append(Stage(value))

def check_condition(conditions, stages, temps, flows, pots):
    for cond in conditions:
        print(cond.get_type())
        if cond.get_type() == 'start':
            #print("checking start")
            pass
        elif cond.get_type() == 'time' and not cond.check_time():
            #print("checking time")
            return False
        elif cond.get_type() == 'afterStage' and not cond.check_after_stage(stages):
            #print("after stage")
            return False
        elif cond.get_type() == 'temperature' and not cond.check_temp(temps):
            #print("cheking temps")
            return False
        elif cond.get_type() == 'flowRate' and not cond.check_flow(flows):
            #print("cheking Flow")
            return False
        elif cond.get_type() == 'volume' and not cond.check_volume(pots):
            #print("cheking Volume 1")
            return False
      
    return True
def alter_valves(client, stage, change, valves):
   if change == 0:
      return
   state = valves[stage.get_maintain_valves()[0].get_id()].state
   state += change
   if state < 0:
      state = 0
   elif state > 100:
      state = 100

   data = []
   for valve in stage.get_maintain_valves():
      temp = valve
      temp.state = state
      data.append(temp)
   
   change_valves(client, data)
def update_aws(client, data, topic):
   print('Sending AWS')
   desired = {'desired': data}
   full = {'state': desired}
   mqtt.publish(client, topic, json.dumps(full))
def change_units(client, units, topic):
    if len(units) == 0: return
    data = {}
   
    for unit in units:
        final = {}
        final['state'] = unit.state
        data[unit.get_id()] = final
   
    update_aws(client, data, topic) 
def change_plugs(client, units):
   change_units(client, units, config.mqtt['topic']['publish']['plug_update'])
def change_valves(client, units):
   change_units(client, units, config.mqtt['topic']['publish']['valve_update'])
def get_confirmed_plugs(units, plugs, control):
    data = []
    for unit in units:
        temp = unit
        if control == 1:
            if plugs[unit.get_id()].state != 1:
                temp.state = 1
                data.append(temp)
        else:
            if plugs[unit.get_id()].state != 0:
                temp.state = 0
                data.append(temp)
    return data
def brew_complete(stages):
   if len(stages) == 0: return False
   for stage in stages:
      if not stage.completed: return False
   return True
def update_brew_done(client):
    data = {
      'stagesNum': 0,
      'stages': None,
      'pots': None
    }
    update_aws(client, data, config.mqtt['topic']['publish']['autorun_update'])
def run_maintain(client, stage, temps, flows, plugs, valves):
    for cond in stage.get_maintain_conds():
        if cond.get_type() == 'temperature':
            units = []
            if cond.control_temp(temps) == 1:
                units = get_confirmed_plugs(stage.get_maintain_plugs(), plugs, 1)
            elif cond.control_temp(temps) == -1:
                units = get_confirmed_plugs(stage.get_maintain_plugs(), plugs, 0)
            else:
                continue
            change_plugs(client, units)

            
        elif cond.get_type() == 'flowMatch' or cond.get_type() == 'flowRate':
            if cond.get_checked():
                continue
            change = cond.valve_change_percent(flows)
            alter_valves(client, stage, change, valves)
            cond.set_checked()