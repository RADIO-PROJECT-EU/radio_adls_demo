#!/usr/bin/env python
import rospy
import getpass
from time import sleep
import subprocess, shlex
from datetime import datetime
from std_msgs.msg import Int32
from motion_analysis_msgs.msg import AnswerWithHeader

first_time = True
ost_pub = None

def eventCallback(msg):
    global first_time
    if first_time:
        dt = datetime.now()
        first_time = False
        print "\033[92m Pill intake date and time: " + datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")+"\033[0m"

def init():
    global start_time, ost_pub
    sleep(5)

    command = "rosbag play -s 30 -u 20 -q /home/"+getpass.getuser()+"/ss1_lsN_sc4_ru11_cg05_v.bag"
    command = shlex.split(command)
    subprocess.Popen(command)

    sleep(1)

    command = "roslaunch motion_analysis object_event_detection.launch"
    command = shlex.split(command)
    subprocess.Popen(command)

    sleep(5)

    ost_pub.publish(2)


if __name__ == '__main__':
    rospy.init_node('radio_pill_demo')
    rospy.Subscriber('/motion_analysis/event/object_tampered', AnswerWithHeader, eventCallback)
    ost_pub = rospy.Publisher('/motion_analysis/object_state', Int32, queue_size=1)
    init()

    while not rospy.is_shutdown():
        rospy.spin()