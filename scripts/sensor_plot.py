#!/usr/bin/env python3
import rospy 
import sys 
from std_msgs.msg import String
from geometry_msgs.msg import Twist
#from taller2_9 import 
from pynput import keyboard


global ruta
global archivo
global estado
global name
global velocidad
global linealX,linealY,linealZ,angularX,angularY,angularZ

ruta= "/home/robotica/robotica_ws/src/taller2_9"
archivo=""
estado=True
name=""


linealX=[]
linealY=[]
linealZ=[]
angularX=[]
angularY=[]
angularZ=[]

velocidades=0
velRight=[]
velLeft=[]
tiempo=[]

def lectura(texto):
	global velocidades,velRight,velLeft,tiempo
	velocidades=int(texto[1])
	clasi=""
	for linea in texto[2:]:
		clasi=linea.split()
		velRight.append(clasi[1])
		velLeft.append(clasi[2])
		tiempo.append(clasi[3])


			



	

#2do punto
def callback(data):
	global velRight, velLeft 


#def on_press(key):
    


#def on_release(key):
    
    	

    	



def nodo():

	rospy.init_node("sensor_plot", anonymous=True) #Inicializo el nodo
	#rospy.Subscriber("turtlebot_position",Twist,callback)	
	#pub=rospy.Publisher('turtlebot_wheelsVel.',Twist,queue_size=10) #Conecta con el tópico turtlebot_cmdVel
	rate=rospy.Rate(10) #Cantidad de datos por segundo que va a publicar
	rospy.spin()
	

	#variable=Twist() #Variable de tipo "Twist" >> 1er vector linear, 2do vector ángular. Cada uno con {x,y,z}
	#hilo1=keyboard.Listener(on_press=on_press,on_release=on_release) #Habilitando hilo para ejecutar las funciones en paralelo
    #hilo1.start()


if __name__ == '__main__':
	argv=
	args =rospy.myargv(argv==sys.argv)
	if len(args) != 2:
		print ("ERROR: No se ha proveido ningún archivo")

	f=open(ruta + args[1],"r")
	name=readlines(f)
	print(name)

	nodo()
	
