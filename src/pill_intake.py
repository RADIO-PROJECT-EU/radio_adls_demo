#!/usr/bin/env python
import rospy
from time import sleep
import subprocess, shlex
from datetime import datetime
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from motion_analysis_msgs.msg import AnswerWithHeader

sub = None
ost_pub = None
image_sub = None


def imageCallback(msg):
    global image_sub, ost_pub
    sleep(5)
    ost_pub.publish(2)
    image_sub.unregister()

def eventCallback(msg):
    global sub
    dt = datetime.now()
    first_time = False
    print "\033[92m Pill intake date and time: " + datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")+"\033[0m"
    #timestamp = datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")
    command = "curl -silent -i -XPOST 'http://localhost:8086/write?db=radiodb' --data-binary 'adl_table,event_type='Pill_intake' duration="+str(1)+"'"
    command = shlex.split(command)
    subprocess.Popen(command, stdout=subprocess.PIPE)
    sub.unregister()


if __name__ == '__main__':
    rospy.init_node('radio_pill_demo')
    sub = rospy.Subscriber('/motion_analysis/event/object_tampered', AnswerWithHeader, eventCallback)
    ost_pub = rospy.Publisher('/motion_analysis/object_state', Int32, queue_size=1)
    image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, imageCallback)

    while not rospy.is_shutdown():
        rospy.spin()