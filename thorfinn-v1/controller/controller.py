#!/usr/bin/env python3

import yaml
from rich import print

from gpiozero import DigitalOutputDevice
import paho.mqtt.client as mqtt


def get_config():
    with open("/boot/config.yml") as file:
        return yaml.safe_load(file)


# Get config
config = get_config()
print("Config:", config)


# Get locks
locks = []

for item in config["locks"]:
    locks.append(DigitalOutputDevice(item["pin"], , active_high=False))

print("Locks:", locks)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("devices/" + config["mqtt"]["client"] + "/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    topic = msg.topic.split("/")

    if topic[2] == "locks":
        print("--> Locks")

        i = int(topic[3])
        print("ID:", i)

        lock = locks[i]

        print(lock)

        print("Blink!")
        lock.blink(on_time=0.5, off_time=0.5, n=1)


def main():

    client = mqtt.Client(config["mqtt"]["client"])

    client.username_pw_set(config["mqtt"]["username"], password=config["mqtt"]["password"])

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("canute.bednarski.dev", 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
