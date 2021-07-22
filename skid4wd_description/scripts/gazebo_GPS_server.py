#!/usr/bin/env python3

## Read gazebo robot position, add noise convert to LAT, LON,
## add to some lat0, lon0 in decimal degree and publish to
## new gps topic

import configparser
from skid4wd_description.msg import geo_loc
import os
import sys
from numpy import random as grandom
import rospy
from gazebo_msgs.srv import GetModelState
from math import sin, cos, atan2
from tf.transformations import euler_from_quaternion

class gazibo_get_pos:
    def show_gazebo_model_position(self):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            object_coordinates = model_coordinates("skid4wd", "")
            z_position = object_coordinates.pose.position.z
            y_position = object_coordinates.pose.position.y
            x_position = object_coordinates.pose.position.x
            angles= object_coordinates.pose.orientation.z
            anglec= object_coordinates.pose.orientation.w
            orientation_list = [object_coordinates.pose.orientation.x, object_coordinates.pose.orientation.y, object_coordinates.pose.orientation.z, object_coordinates.pose.orientation.w]
            (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
            angle=yaw
            #angle=atan2(anglec,angles)*2

        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
            x_position = 0
            y_position = 0
            angle = 0
            z_position = 0

        return x_position, y_position, z_position, angle

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def gazebo_gps_publisher():
    #Load coordinate system from .ini file
    dir_path = get_script_path()+"/gps_init.INI"

    config = configparser.ConfigParser()
    config.read(dir_path)
    
    rospy.loginfo("GPS server started")
   
    lat0= config.getfloat('zero','lat0')    # -> "/path/name/"
    lon0= config.getfloat('zero','lon0')
    h0= config.getfloat('zero','h0')
    angle0 = config.getfloat('zero','angle0')
    freq= config.getfloat('zero','freq')

    sigma_xy=config.getfloat('noise','xy')
    sigma_z=config.getfloat('noise','z')
    sigma_angle=config.getfloat('noise','angle')

    #config['DEFAULT']['path'] = '/var/shared/'    # update
    #config['DEFAULT']['default_message'] = 'Hey! help me!!'   # create

    #with open('FILE.INI', 'w') as configfile:    # save
    #config.write(configfile)

    pub= rospy.Publisher('gps', geo_loc, queue_size=1000)
    rospy.init_node('gazebo_gps_publisher_node', anonymous=True)
    rate = rospy.Rate(freq) # 10hz

    lat=lat0
    lon=lon0
    h=h0
    angle=angle0

    Pos = gazibo_get_pos()

    while not rospy.is_shutdown():
        #Adding noise
        s_xy1= grandom.normal(0, sigma_xy, 1)
        s_xy2= grandom.normal(0, sigma_xy, 1)
        s_z = grandom.normal(0, sigma_z, 1)
        s_angle = grandom.normal(0, sigma_angle, 1)

        msg=geo_loc()

        #Gtting gazebo position
        x,y,z,angle=Pos.show_gazebo_model_position()
        #print ("(x,y,z)=(",x,y,z,")") #TOOD DEBUG_print
        #Converting position do lat/lon
        xtemp=x*cos(angle0)-y*sin(angle0)
        ytemp=y*cos(angle0)+x*sin(angle0)

        x=xtemp
        y=ytemp

        x=x*0.00001/1.11
        y=y*0.00001/1.11
        #Combine

        msg.lat=lat+s_xy1+x
        msg.lon=lon+s_xy2+y
        msg.h_meter=h+s_z
        msg.angle=angle+s_angle

        #Publishing
        #rospy.loginfo(msg) #DEBUG
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        gazebo_gps_publisher()
    except rospy.ROSInterruptException:
        pass