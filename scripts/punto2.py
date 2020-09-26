#!/usr/bin/env python
from std_msgs.msg import String, Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import  matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import threading
import rospy
import sys

global tiempoCero, i, numVel,vels,tiempo
i = 0
tiempoCero = 0
l = 0.23  # metros

ruta = '/home/jsgonzalez15/robotica_ws/src/taller2_9/resources/'
nombre = sys.argv[1]
vels = np.loadtxt(ruta+nombre+'.txt')

numVel = vels[0,0]

# angulo inicial
theta = [-np.pi]

#---
tiempo = [0]
posVREPx = []
posVREPy = []
posODOx = [0]
posODOy = [0]
#---

def callbackTime(data):
  global tiempoCero, i, numVel,vels
  tiempo.append(data.data)
  if tiempoCero == 0:
    tiempoCero = data.data
  if i < numVel:
    dt = 0.1
    Vr = 0.1*vels[i+1,0]
    Vl = 0.1*vels[i+1,1]
    posODOx.append( posODOx[-1] + 0.5*(Vr+Vl)*np.cos(theta[-1])*dt )
    posODOy.append( posODOy[-1] + 0.5*(Vr+Vl)*np.sin(theta[-1])*dt )
    theta.append( theta[-1] + 1/l*(Vr-Vl)*dt)
    tiempoVel = data.data - tiempoCero
    if tiempoVel >= vels[i+1,2]:
      i+=1
      tiempoCero = 0
      print(len(tiempo))
      print(len(posODOx))
      print(posODOx)

def callbackPos(pos):
  global posVREPx, posVREPy
  posVREPx.append(pos.linear.x)
  posVREPy.append(pos.linear.y)

def graficar(i):
  plt.cla() #Se borra informacion anterior al ploteo actual
  plt.plot(posVREPx,posVREPy,'b')
  plt.plot(posODOx, posODOy, 'g')
  plt.axis([-2.5,2.5,-2.5,2.5]) #Define limites en X y en Y

def realTime():
  objeto=animation.FuncAnimation(plt.figure(1),graficar,10000) #plt.gcf get currently figure Animar las figuras por parametro de manera iterativa
  plt.show()

def tYl():
  global tiempoCero, i, numVel,vels,tiempo,posODOx,posODOy
  rospy.init_node('punto2_talker', anonymous=True)

  rospy.Subscriber('turtlebot_position', Twist, callbackPos)
  rospy.Subscriber('simulationTime', Float32, callbackTime)
  pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)
  RTgraph = threading.Thread(target=realTime)
  RTgraph.start()

  rate = rospy.Rate(10) #10hz
  while not rospy.is_shutdown():
    msg = Float32MultiArray()
    if i<numVel:
      msg.data = [vels[i+1,0], vels[i+1,1]]
    else:
      msg.data = [0, 0]
    pub.publish(msg)
    rate.sleep()

if __name__ == '__main__':
  try:
    tYl()
  except rospy.ROSInterruptException:
    pass