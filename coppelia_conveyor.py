# Copyright (c) 2024 glauberrleite
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from paho.mqtt import client as mqtt

CLIENT_NAME = "conveyor"
        
def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
            # Subscribing to topics of interest
            self.client.subscribe(CLIENT_NAME+"/cmd_vel")
            print("Subscribed to " + CLIENT_NAME+"/cmd_vel")
            self.client.on_message = on_message
        else:
            print("Failed to connect, return code %d\n", reason_code)        

def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Disconnected to MQTT Broker!")
    if reason_code > 0:
        print("Failed to disconnect, return code %d\n", reason_code)
        
def on_message(client, userdata, msg):
    if msg.topic == CLIENT_NAME+"/cmd_vel":
        self.target_vel = msg.payload.decode()
        print("Received new velocity command: " + self.target_vel)

def sysCall_init():
    sim = require('sim')

    self.conveyorHandle = sim.getObject('.')
    self.target_vel = 0.0
    
    # Setting mqtt client and starting connection
    self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_NAME)
    self.client.on_connect = on_connect
    self.client.on_disconnect = on_disconnect
    
    # Getting broker and port from global values that are shared across all simulation objects
    broker = sim.getStringSignal("mqtt_broker")
    port = sim.getInt32Signal("mqtt_port")

    self.client.connect(broker, port)
    self.client.loop(0.01) # For the on_connect callback function to run, it needs a mqtt client loop

def sysCall_actuation():
    self.client.loop(0.01) # Taking time to mqtt client rapidly fetch some messages from subscribed topics
    sim.writeCustomTableData(self.conveyorHandle, '__ctrl__', {"vel":self.target_vel})

def sysCall_sensing():
    # Publishing values
    state = sim.readCustomTableData(self.conveyorHandle,'__state__')
    self.client.publish(CLIENT_NAME+"/vel", state['vel'])
    self.client.publish(CLIENT_NAME+"/pos", state['pos'])

def sysCall_cleanup():
    # Clean disconnect of MQTT client
    self.client.disconnect()