#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np
import  matplotlib.pyplot as plt
import sys
import math

import matplotlib.pyplot as plt #Librera para graficar
from matplotlib import animation
import threading

global posicionFinal, tiempo,posVREPx,posVREPy,posODOx,posODOy, velODOr, velODOl
global kp,kalpha,kbeta
global actualX, actualY, actualTheta, rho, alpha, beta, nrho,nbeta,nalpha, posVREPrho

actualX=0
actualY=0
actualTheta=0
rho=0
alpha=0.5
beta=0
nrho=0
nalpha=0
nbeta=0
posVREPrho=[]
kp=0.3
kalpha=0.8
kbeta=-0.1 
posicionFinal=[-2,-2,-3*np.pi/4] #Posicion predeterminada si usuario no ingresa pos final
tiempo=[] #tiempo de simulacion 


global variableX
global variableY

variableX=[]
variableY=[]







def callbackTime(timeVREP): #funcion para llamar tiempo de topico
    global tiempo
    tiempo=append(float(timeVREP.data))


    


def callbackPos(posVREP): #funcion para obtener posicion segun topico
    global posVREPx, posVREPy, angleVREP
    posVREPx.append(posVREP.linear.x)
    posVREPy.append(posVREP.linear.y)
    angleVREP.append(angleVREP.angular.z)

def posActual(posVREP):
  global actualX, actualY, actualTheta, deltaX, deltaY,rho,alpha,beta
  actualX=posVREP.linear.x
  actualY=posVREP.linear.y
  actualTheta=posVREP.angular.z
  deltaX=posicionFinal[0]-actualX
  deltaY=posicionFinal[1]-actualY
  rho=np.sqrt((deltaX**2)+(deltaY**2))
  alpha=-actualTheta+math.atan2(deltaY,deltaX)
  beta=-actualTheta-alpha
  print(deltaX)


def callback(data):
  global variableX
  global variableY
  variableX.append(data.linear.x)
  variableY.append(data.linear.y)
def graficar(i):
  global variableX
  global variableY
  plt.cla() #Se borra informacin anterior al ploteo actual
  plt.plot(variableX,variableY) #Plotea las variables
  plt.axis([-1,1,-1,1]) #Define lmites en X y en Y
def anima():
  objeto=animation.FuncAnimation(plt.figure(1),graficar,10000) #plt.gcf get currently figure Animar las figuras por parmetro de manera iterativa
  plt.show()


def subs():
  rospy.init_node("turtle_bot_position", anonymous=True)
  rospy.Subscriber("turtlebot_position",Twist,callback) 
  hilo2=threading.Thread(target=anima)
  hilo2.start()
  rospy.spin()

def errors():
  global tiempo
  global posVREPrho
  plot(tiempo, posVREPrho)







def control():
  global posicionFinal, rho, alpha, beta, nrho, nalhpa, nbeta, posVREPrho
  

  rospy.Subscriber('turtlebot_position', Twist, posActual)
  rospy.Subscriber('simulationTime', Float32, callbackTime)
  
  pub=rospy.Publisher('turtlebot_cmdVel',Twist,queue_size=10)
  rospy.init_node('punto3', anonymous=True) #inicializacion de nodo
  variable=Twist()


  #pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)
  
  rate = rospy.Rate(10) #10hz
  
  args=rospy.myargv(argv=sys.argv)


  while not rospy.is_shutdown():
    
    #print(variable)


    if len(args)!=0:
      posicionFinal[0]=float(args[1])
      posicionFinal[1]=float(args[2])
      posicionFinal[2]=float(args[3])

      #Actualizando Rho y Alpha
      nrho=-kp*rho*np.cos(alpha)
      nalpha=kp*np.sin(alpha)-kalpha*alpha-kbeta*beta

      #Publicar Vel lineal y angular en el topico
      variable.linear.x=nrho*1300
      variable.angular.z=(kp*np.sin(alpha)-kalpha*alpha)*1300
      
      #
      

      #Ajusta Beta despues de que el robot llegue a la pos final
      if rho==0 and alpha==0:
        beta=-kp*np.sin(alpha)
      rho=nrho
      alpha=nalpha
      posVREPrho.append(rho)
    else:
      #Actualizando Rho y Alpha
      #nrho=-kp*rho*math.cos(alpha)
      nalpha=kp*math.sin(alpha)-kalpha*alpha-kbeta*beta

      #Publicar Vel lineal y angular en el topico
      variable.linear=0
      variable.angular=15

      #Ajusta Beta despues de que el robot llegue a la pos final
      if rho==0 and alpha==0:
        beta=-kp*math.sin(alpha)
      rho=nrho
      alpha=nalpha
    pub.publish(variable)
    rate.sleep()


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


if __name__ == '__main__':
  subs()
  control()
  errors()
  