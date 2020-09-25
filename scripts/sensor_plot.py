#!/usr/bin/env python3
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
# from taller2_9 import
from pynput import keyboard

global ruta
global archivo
global estado
global name
global velocidad
global linealX, linealY, linealZ, angularX, angularY, angularZ

estado = True
name = ""

linealX = []
linealY = []
linealZ = []
angularX = []
angularY = []
angularZ = []

# 2do punto


def callback(data):
	global linealX, linealY, linealZ, angularX, angularY, angularZ
	linealX.append(data.linear.x)
	linealY.append(data.linear.y)
	linealZ.append(data.linear.z)
	angularX.append(data.angular.x)
	angularY.append(data.angular.y)
	angularZ.append(data.angular.z)

# def on_press(key):

# def on_release(key):

def nodo():
	rospy.init_node("sensor_plot", anonymous=True)
    args = sys.argv[1]
    ruta= "/home/robotica/catkin_ws/src/taller2_9/resources/"
    archivo=np.loadtxt(ruta+args)
    print(archivo)
	# rospy.Subscriber("turtlebot_position",Twist,callback)	
	# pub=rospy.Publisher('turtlebot_wheelsVel.',Twist,queue_size=10) #Conecta con el tópico turtlebot_cmdVel
	rate=rospy.Rate(10) #Cantidad de datos por segundo que va a publicar
	rospy.spin()
	

	# variable=Twist() #Variable de tipo "Twist" >> 1er vector linear, 2do vector ángular. Cada uno con {x,y,z}
	# hilo1=keyboard.Listener(on_press=on_press,on_release=on_release) #Habilitando hilo para ejecutar las funciones en paralelo
    # hilo1.start()


if __name__ == '__main__':
	argv=
	args =rospy.myargv(argv==sys.argv)
	nodo()
	f=open(ruta + args[1])
	name=readlines(f)
	print(name)
