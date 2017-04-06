#!/usr/bin/env python
import rospy
import subprocess, shlex
from datetime import datetime
from sensor_msgs.msg import Image
from motion_analysis_msgs.msg import AnswerWithHeader

stood_up = False
started_walking = False
start_time = None
image_sub = None

def imageCallback(msg):
    global start_time, image_sub
    dt = datetime.now()
    start_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
    image_sub.unregister()


def eventCallback(msg):
    global stood_up, start_time, started_walking
    if msg.event == 1 and not stood_up:
        stood_up = True
        dt = datetime.now()
        end_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
        print '\033[92m Stood up after ' + str((end_time-start_time)/1000000.0) + ' seconds.\033[0m'
        #timestamp = datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")
        command = "curl -silent -i -XPOST 'http://localhost:8086/write?db=radiodb' --data-binary 'adl_table,event_type='Lying-Standing' duration="+str((end_time-start_time)/1000000.0)+"'"
        command = shlex.split(command)
        subprocess.Popen(command, stdout=subprocess.PIPE)
        start_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
    elif msg.event == 2 and stood_up and not started_walking:
        started_walking = True
        dt = datetime.now()
        end_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
        print '\033[92m Started walking after ' + str((end_time-start_time)/1000000.0) + ' seconds.\033[0m'
        #timestamp = datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")
        command = "curl -silent -i -XPOST 'http://localhost:8086/write?db=radiodb' --data-binary 'adl_table,event_type='Standing-Walking' duration="+str((end_time-start_time)/1000000.0)+"'"
        command = shlex.split(command)
        subprocess.Popen(command, stdout=subprocess.PIPE)


if __name__ == '__main__':
    rospy.init_node('radio_bed_demo')
    rospy.Subscriber('/motion_analysis/event/human_transfer', AnswerWithHeader, eventCallback)
    image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, imageCallback)

    while not rospy.is_shutdown():
        rospy.spin()
