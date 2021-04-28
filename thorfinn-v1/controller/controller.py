#!/usr/bin/env python3

import yaml
from rich import print


def get_config():
    with open("/boot/config.yml") as file:
        return yaml.load(file)


print("Hello World!", get_config())
