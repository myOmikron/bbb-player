#!/usr/bin/env python3
"""
This script processes all recordings in the todo directory.
It is intended to be called via cron on reboot to clean up unfinished recordings.
"""

import os, subprocess

hostname = subprocess.run(['hostname', '--fqdn'], stdout=subprocess.PIPE).stdout.decode('utf-8')

for file in os.listdir('/var/bigbluebutton/todo'):
    subprocess.run(['python3', '/home/bbb-player/bbb-player/bbb_player/worker/main.py', '-i', file, '-H', hostname])

