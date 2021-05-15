import paho.mqtt.client as mqtt
from support import config
import time



def on_disconnect(client, userdata, rc):
    client.loop_stop()


def subscribe(client, topic):
    print('Subscribing To: ', topic, '...', end='')
    while True:
       result = client.subscribe(topic)
       if result[0] == 0:
           print('Successful')
           break

def unsubscribe(client, topic):
    print('Unsubscribing To: ', topic, '...', end='')
    while True:
        result = client.unsubscribe(topic)
        if result[0] == 0:
            print('Successful')
            break

def publish(client, topic, message):
    print('Publishing To: ', topic)
    print('      Message: ', message)
    client.publish(topic, message)

def on_message(client, userdata, msg):
    print("Message Recieved")
    
    msg.payload = msg.payload.decode('utf-8')
    print(msg.payload)
    return msg.payload


def connect_mqtt():
    print('Connecting to MQTT')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(username = config.mqtt['username'], password = config.mqtt['password'])
    client.connect(config.mqtt['ip'], config.mqtt['port'], config.mqtt['timeout'])
    return client

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    
    sub_topics = config.mqtt['topic']['subscribe']
    pub_topics = config.mqtt['topic']['publish']
    subscribe(client, sub_topics['plug_in'])
    subscribe(client, sub_topics['autorun_in'])
    subscribe(client, sub_topics['autorun_get'])
    subscribe(client, sub_topics['valve_in'])
    subscribe(client, sub_topics['sensor_in'])
    time.sleep(1)
    publish(client, pub_topics['plug_get'], '')
    publish(client, pub_topics['autorun_get'], '')
    publish(client, pub_topics['valve_get'], '')

  



