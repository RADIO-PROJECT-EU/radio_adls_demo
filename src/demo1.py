#!/usr/bin/env python
import os
import rospy
from time import sleep
import subprocess, shlex
from laser_analysis.msg import Analysis4MetersMsg

if __name__ == '__main__':
    print '\033[94m Welcome to RADIO ADL Demonstration. \033[0m'
    sleep(2)
    command = "roslaunch radio_adls_demo walking.launch"
    command = shlex.split(command)
    subprocess.Popen(command, stderr=subprocess.PIPE)
    sleep(2)
    print '\033[94m Starting 4m walk measurement... \033[0m'

    stop = False
    mode = 0

    while not stop:
        sleep(8)
        nodes = os.popen("rosnode list").readlines()
        found = False
        for node in nodes:
            if "laser" in node and mode == 0:
                found = True
                break
            elif "motion_analysis" in node and (mode == 1 or mode == 2):
                found = True
                break
            elif "fusion" in node and mode == 3:
                found = True
                break

        if not found:
            if mode == 0:
                command = "roslaunch radio_adls_demo pill_intake.launch"
                command = shlex.split(command)
                subprocess.Popen(command, stderr=subprocess.PIPE)
                sleep(2)
                print '\033[94m Starting pill intake recognition... \033[0m'
                mode = 1
            elif mode == 1:
                command = "roslaunch radio_adls_demo bed_event.launch"
                command = shlex.split(command)
                subprocess.Popen(command, stderr=subprocess.PIPE)
                sleep(2)
                print '\033[94m Starting bed transfer measurement... \033[0m'
                mode = 2
            elif mode == 2:
                command = "roslaunch radio_adls_demo tracking.launch"
                command = shlex.split(command)
                subprocess.Popen(command, stderr=subprocess.PIPE)
                sleep(2)
                print '\033[94m Starting human tracking... \033[0m'
                mode = 3
            elif mode == 3:
                stop = True
    print '\033[94m That was all! Goodbye! \033[0m'
