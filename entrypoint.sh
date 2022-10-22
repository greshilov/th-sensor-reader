#!/bin/bash

# start services

service dbus start
service bluetooth start


bluetoothctl power off
bluetoothctl power on

sleep 3s

python main.py
