#!/usr/bin/env python
import cv2
import rospy
import subprocess, shlex
from datetime import datetime
from std_msgs.msg import String
from sensor_msgs.msg import Image
from ros_visual_msgs.msg import FusionMsg
from cv_bridge import CvBridge, CvBridgeError

sitting = False
stood_up = False
start_time = None
new_rec = False
boxes = []
bridge = None

def eventCallback(msg):
    global stood_up, start_time, started_walking, sitting
    if msg.data == "sit" and not stood_up:
        dt = datetime.now()
        start_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
        sitting = True
    elif msg.data == "stand" and sitting and not stood_up:
        stood_up = True
        dt = datetime.now()
        end_time = dt.minute*60000000 + dt.second*1000000 + dt.microsecond
        print '\033[92m Sit to stand duration: ' + str((end_time-start_time)/1000000.0) + ' seconds.\033[0m'
        #timestamp = datetime.today().strftime("%d-%m-%Y")+" "+dt.strftime("%H:%M:%S")
        command = "curl -silent -i -XPOST 'http://localhost:8086/write?db=radiodb' --data-binary 'adl_table,event_type='Sitting-Standing' duration="+str((end_time-start_time)/1000000.0)+"'"
        command = shlex.split(command)
        subprocess.Popen(command, stdout=subprocess.PIPE)

def rectangleCallback(msg):
    global new_rec, boxes
    if len(msg.boxes) > 0:
        new_rec = True
        boxes = []
        for i in msg.boxes:
            boxes.append(i)

def imageCallback(image):
    global new_rec, boxes, bridge
    try:
        cv_image = bridge.imgmsg_to_cv2(image, "bgr8")
    except CvBridgeError as e:
        return 0

    (rows,cols,channels) = cv_image.shape
    if new_rec:
        new_rec = False
        for i in boxes:
            x1 = int(i.rect.x)
            y1 = int(i.rect.y)
            x2 = x1 + int(i.rect.width)
            y2 = y1 + int(i.rect.height)
            cv2.rectangle(cv_image, (x1, y1), (x2, y2), (255, 0, 0), 0, 8)
    cv2.imshow("Human Tracking", cv_image)
    cv2.waitKey(3)


if __name__ == '__main__':
    rospy.init_node('radio_chair_demo')
    rospy.Subscriber('/fusion/results', FusionMsg, rectangleCallback)
    classifier = rospy.get_param('/radio_adls_demo/classifier', False)
    bridge = CvBridge()
    rospy.Subscriber('/camera/rgb/image_raw', Image, imageCallback)
    if classifier:
        rospy.Subscriber('/classifier/result', String, eventCallback)

    while not rospy.is_shutdown():
        rospy.spin()