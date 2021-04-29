#!/usr/bin/env python3

import json
import yaml
from rich import print


from gpiozero import DigitalOutputDevice
import paho.mqtt.client as mqtt
import json


def get_config():
    with open("/boot/config.yml") as file:
        return yaml.safe_load(file)


# Get config
config = get_config()
print("Config:", config)

shadows = []

# Get locks
locks = []

for i, item in enumerate(config["locks"]):
    locks.append(DigitalOutputDevice(item["pin"], active_high=False))

    shadows.append({"name": item["name"], "class": "lock", "topic": "things/" + config["mqtt"]["client"] + "/" + i + "/set"})

print("Locks:", locks)

status = {"online": True}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("things/" + config["mqtt"]["client"] + "/#")

    client.publish("things/" + config["mqtt"]["client"] + "/status", json.dumps(status))
    client.publish("things/" + config["mqtt"]["client"] + "/shadows", json.dumps(shadows))


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    topic = msg.topic.split("/")

    if topic[2] == "locks":
        print("Module - Locks")

        if topic[4] == "set":
            try:
                lock = locks[topic[3]]

                lock.blink(on_time=0.5, off_time=0.5, n=1)
            except:
                print("No locks with this id!")


def main():
    client = mqtt.Client(config["mqtt"]["client"])

    client.username_pw_set(config["mqtt"]["username"], password=config["mqtt"]["password"])
    client.will_set("things/" + config["mqtt"]["client"] + "/status", json.dumps({"online": False}))

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("canute.bednarski.dev", 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
