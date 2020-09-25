#!/usr/bin/env python
import rospy 
import sys 
from std_msgs.msg import String,Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np

global ruta,archivo,estado,name
global nVel,rightVel,leftVel,tiempo,n,simTime, initialTime
n=0
initialTime=0
nVel=0
rightVel=Float32(0	)
leftVel=Float32(0)
tiempo=0
simTime=0
global linealX,linealY,linealZ,angularX,angularY,angularZ

ruta= "/home/jsgonzalez15/robotica_ws/src/taller2_9/resources/"
archivo=""
estado=True
name=""


linealX=[]
linealY=[]
linealZ=[]
angularX=[]
angularY=[]
angularZ=[]

#2do punto
def giveMeTime(data):
	global simTime,initialTime
	simTime=data
	if initialTime==0:
		initialTime=simTime

#def on_press(key):
    

#def on_release(key):
    
def lectura(texto,n):
	global nVel,rightVel,leftVel,tiempo
	nVel=texto[0,0]
	if n<nVel:
		rightVel=Float32(texto[n,0])
		leftVel=Float32(texto[n,1])
		tiempo=texto[n,2]
	else:
		rightVel=0
		leftVel=0

def nodo():
	global nVel,rightVel,leftVel,tiempo,simTime,initialTime,n 
	rospy.init_node("sensor_plot", anonymous=True) #Inicializo el nodo
	arg= sys.argv[1]
	f=open(ruta + arg[:])
	comandVel=np.loadtxt(f)

	rospy.Subscriber("simulationTime",Float32,giveMeTime)	
	pub=rospy.Publisher('turtlebot_wheelsVel',Float32MultiArray,queue_size=10) #Conecta con el topico turtlebot_cmdVel
	rate=rospy.Rate(10) #Cantidad de datos por segundo que va a publicar
	rospy.spin()

	if simTime-initialTime>=Float32(tiempo):
		n=n+1
		initialTime=simTime
		lectura(comandVel,n)
	
	variable=Float32MultiArray(leftVel,rightVel) #Variable de tipo "Twist" >> 1er vector linear, 2do vector angular. Cada uno con {x,y,z}
	pub.publish(variable)


if __name__ == '__main__':
	nodo()
