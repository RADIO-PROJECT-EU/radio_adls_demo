#!/usr/bin/env python
import rospy
import getpass
from time import sleep
import subprocess, shlex
from laser_analysis.msg import Analysis4MetersMsg


def eventCallback(msg):
    print '\033[94m 4m walking approximation: ' + str(msg.time_needed) + ' seconds.\033[0m'
    #timestamp = datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")
    command = "curl -silent -i -XPOST 'http://localhost:8086/write?db=radiodb' --data-binary 'adl_table,event_type='4m_walking' duration="+str(msg.time_needed)+"'"
    command = shlex.split(command)
    subprocess.Popen(command, stdout=subprocess.PIPE)


def init():
    sleep(6)
    command = "rosbag play -s 45 -q /home/"+getpass.getuser()+"/ss1_lsA_sc1B_ru15_cg_v.bag"
    command = shlex.split(command)
    subprocess.Popen(command, stdout=subprocess.PIPE)


if __name__ == '__main__':
    rospy.init_node('radio_walking_demo')
    rospy.Subscriber('/laser_analysis/results4meters', Analysis4MetersMsg, eventCallback)
    init()

    while not rospy.is_shutdown():
        rospy.spin()