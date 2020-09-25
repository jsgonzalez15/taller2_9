#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np
import  matplotlib.pyplot as plt
import sys

global posicionFinal, tiempo,posVREPx,posVREPy,posODOx,posODOy, velODOr, velODOl
posicionFinal=[-2,-2,-3*np.pi/4] #Posicion predeterminada si usuario no ingresa pos final
tiempo=0 #tiempo de simulacion 
posVREPx,posVREPy=Twist() #posiciones segun topico de VREP
posODOx,posODOy=[0] #posiciones segun estimacion por odometria
velODOr, velODOl=[0] #velocidades de control segun nueva posicion deseada estimada por odometria

def callbackTime(timeVREP): #funcion para llamar tiempo de topico
    global tiempo
    timeVREP=timeVREP.data
    dt=timeVREP-tiempo
    tiempo=timeVREP


def callbackPos(posVREP): #funcion para obtener posicion segun topico
    global posVREPx, posVREPy
    posVREPx.append(posVREP.linear.x)
    posVREPy.append(posVREP.linear.y)

def control():
  global posicionFinal
  rospy.init_node('punto3_talker', anonymous=True) #inicializacion de nodo

  rospy.Subscriber('turtlebot_position', Twist, callbackPos)
  rospy.Subscriber('simulationTime', Float32, callbackTime)
  pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)

  rate = rospy.Rate(10) #10hz
  '''
  while not rospy.is_shutdown():
    msg = Float32MultiArray()
    if i<numVel:
      msg.data = [vels[i+1,0], vels[i+1,1]]
    else:
      msg.data = [0, 0]
      plt.plot(posODOx,posODOy)
      plt.show()
    pub.publish(msg)
    rate.sleep()'''