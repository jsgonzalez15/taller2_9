#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np
import  matplotlib.pyplot as plt
import sys

global tiempoCero, i, numVel,vels
i = 0
tiempoCero = 0

ruta = "/home/jsgonzalez15/robotica_ws/src/taller2_9/resources/"
nombre = sys.argv[1]
vels = np.loadtxt(ruta+nombre+'.txt')

numVel = vels[0,0]

# posicion inicial
x = [0]
y = [0]
theta = [-np.pi]

#---
tiempo = []
posVREPx = []
posVREPy = []
posODOx = [0]
posODOy = [0]
#---

def callbackTime(data):
  global tiempoCero, i, numVel,vels
  odometria(data.data)
  tiempo.append(data.data)
  if tiempoCero == 0:
    tiempoCero = data.data
  if i < numVel:
    tiempoVel = data.data - tiempoCero
    if tiempoVel >= vels[i+1,2]:
      i+=1
      tiempoCero = 0
      print(len(tiempo))

def callbackPos(pos):
  posVREPx.append(pos.linear.x)
  posVREPy.append(pos.linear.y)

def tYl():
  global tiempoCero, i, numVel,vels
  rospy.init_node('punto2_talker', anonymous=True)

  rospy.Subscriber('turtlebot_position', Twist, callbackPos)
  rospy.Subscriber('simulationTime', Float32, callbackTime)
  pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)

  rate = rospy.Rate(10) #10hz
  while not rospy.is_shutdown():
    msg = Float32MultiArray()
    if i<numVel:
      msg.data = [vels[i+1,0], vels[i+1,1]]
    else:
      msg.data = [0, 0]
      plt.plot(posODOx,posODOy)
      plt.show()
    pub.publish(msg)
    rate.sleep()

def odometria(newTime):
  dt = newTime - tiempo[-1]
  Vr = vels[i+1,0]
  Vl = vels[i+1,1]
  posODOx.append( x[-1] + 0.5*(Vr+Vl)*np.cos(theta[-1])*dt )
  posODOy.append( y[-1] + 0.5*(Vr+Vl)*np.sin(theta[-1])*dt )
  

if __name__ == '__main__':
  try:
    tYl()
  except rospy.ROSInterruptException:
    pass
