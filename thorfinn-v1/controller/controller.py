#!/usr/bin/env python3

import yaml
from rich import print
import paho.mqtt.client as mqtt


def get_config():
    with open("/boot/config.yml") as file:
        return yaml.safe_load(file)


config = get_config()

print("Hello World!", config)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("devices/" + config["mqtt"]["client"] + "/#")

    client.publish("devices/" + config["mqtt"]["client"] + "/info", "Hello!")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def main():

    client = mqtt.Client(config["mqtt"]["client"])

    client.username_pw_set(config["mqtt"]["username"], password=config["mqtt"]["password"])

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("canute.bednarski.dev", 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
