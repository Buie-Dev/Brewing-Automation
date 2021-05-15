
from support import config
from support import auto
from support import mqtt
import time
import json

stages = []
temps = {}
flows = {}
pots = {}

valves = {}
plugs = {}

def on_message(client, userdata, msg):
   
   msg.payload = msg.payload.decode("utf-8")
   print(msg.payload)
   sub_topics = config.mqtt['topic']['subscribe']
  
   content = json.loads(str(msg.payload))
   if msg.topic == sub_topics['sensor_in']:
      content['type']
      if content['type'] == 'temp':
         auto.set_temp(content, temps)
      elif content['type'] == 'flow':
         auto.set_flow(content, flows, pots)
   else:
      content = content['state']['desired']
      if msg.topic == sub_topics['autorun_in']:
         auto.set_autorun(content, stages, pots)
      elif msg.topic == sub_topics['autorun_get']:
         auto.set_autorun(content, stages, pots)
         mqtt.unsubscribe(client, sub_topics['autorun_get'])
      elif msg.topic == sub_topics['plug_in']:
         auto.set_plugs(content, plugs)
      elif msg.topic == sub_topics['valve_in']:
         auto.set_valves(content, valves)


print("Auto Brew Loading...")
time.sleep(1)
auto.check_internet()
mqtt.on_message = on_message
client = mqtt.connect_mqtt()
client.loop_start()


while True:
   for stage in stages:
      if stage.completed:
         print("stage:{} is completed".format(stage.get_name()))
         continue

      if not stage.started:
   
         if not auto.check_condition(stage.get_start_conds(), stages, temps, flows, pots):
            continue

         print("Stage: {} Started".format(stage.get_name()))
         stage.started = True
         for cond in stage.get_finish_conds():
            if cond.get_type() == 'time':
               print("Starting timer")
               cond.start_timer()

         

         print("Setting Start Plugs and Valves")
         auto.change_plugs(client, stage.get_start_plugs())
         auto.change_valves(client, stage.get_start_valves())
         
        
      if auto.check_condition(stage.get_finish_conds(), stages, temps, flows, pots):

         print("Stage: {} Finished".format(stage.get_name()))
         stage.completed = True

         print("Setting Finish Plugs and Valves")
         if len(stage.get_maintain_conds()) > 0:
            print("Running Maintain Conditions")
         else:
            print("No Maintain COndition Found")
         auto.change_plugs(client, stage.get_finish_plugs())
         auto.change_valves(client, stage.get_finish_valves())
         continue

      auto.run_maintain(client, stage, temps, flows, plugs, valves)

   if (auto.brew_complete(stages)):
      print ("Brew Complete")
      auto.update_brew_done(client)
        
   time.sleep(.2) # allows timne for other things to run


 