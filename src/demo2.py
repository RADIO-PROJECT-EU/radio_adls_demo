#!/usr/bin/env python
import os
import rospy
from time import sleep
import subprocess, shlex
from laser_analysis.msg import Analysis4MetersMsg

if __name__ == '__main__':
    print '\033[94m Welcome to RADIO ADL Demonstration. \033[0m'
    sleep(2)
    command = "roslaunch radio_adls_demo chair_event.launch"
    command = shlex.split(command)
    subprocess.Popen(command, stderr=subprocess.PIPE)
    sleep(2)
    print '\033[94m Starting chair event detection... \033[0m'

    stop = False
    mode = 0

    while not stop:
        sleep(8)
        nodes = os.popen("rosnode list").readlines()
        found = False
        for node in nodes:
            if "fusion" in node and mode == 0:
                found = True
                break

        if not found:
            if mode == 0:
                print '\033[94m Processing audio... \033[0m'
                # run pyAudioAnalysis here
                command = "play /home/osboxes/python_libraries/pyAudioAnalysis/ss1_lsA_sc2_ruekot_cgedia_v.wav"
                command = shlex.split(command)
                subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                sleep(26)
                command = "python /home/osboxes/python_libraries/pyAudioAnalysis/audioAnalysis.py segmentClassifyFile -i /home/osboxes/python_libraries/pyAudioAnalysis/ss1_lsA_sc2_ruekot_cgedia_v.wav --model svm_rbf --modelName /home/osboxes/python_libraries/pyAudioAnalysis/svmRBFRadio4Classes"
                command = shlex.split(command)
                subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print '\033[94m Do you want to play the sound file again? (y/n) \033[0m'
                ans = raw_input()
                if ans == 'y':
                    command = "play /home/osboxes/python_libraries/pyAudioAnalysis/ss1_lsA_sc2_ruekot_cgedia_v.wav"
                    command = shlex.split(command)
                    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    sleep(22)
                mode = 1
            elif mode == 1:
                stop = True
    print '\033[94m That was all! Goodbye! \033[0m'
