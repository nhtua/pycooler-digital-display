#!/bin/bash


#1. generate cooler-display.service from template
#2. copy file into systemd service directory
cp cooler-display.service /etc/systemd/system
chown root:root /etc/systemd/system/cooler-display.service
chmod 644 /etc/systemd/system/cooler-display.service

systemctl daemon-reload
systemctl enable cooler-display
systemctl start cooler-display
