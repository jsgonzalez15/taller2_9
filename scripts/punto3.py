#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np
import  matplotlib.pyplot as plt
import sys
import math
import argparse, copy

global posicionFinal, tiempo,posVREPx,posVREPy,posODOx,posODOy, velODOr, velODOl
global kp,kalpha,kbeta
global actualX, actualY, actualTheta

actualX=0
actualY=0
actualTheta=np.pi

kp=1
kalpha=1.5
kbeta=-1 
posicionFinal=[-2,-2,-3*np.pi/4] #Posicion predeterminada si usuario no ingresa pos final
tiempo=0 #tiempo de simulacion 
#posVREPx,posVREPy=Twist() #posiciones segun topico de VREP
#posODOx,posODOy=[0] #posiciones segun estimacion por odometria
#velODOr, velODOl=[0] #velocidades de control segun nueva posicion deseada estimada por odometria

parser = argparse.ArgumentParser()
parser.add_argument("-x","--PosicionX", help="Ingrese la coordenada x de su objetivo")
parser.add_argument("-y","--PosicionY", help="Ingrese la coordenada y de su objetivo")
parser.add_argument("-a","--Angulo", help="Ingrese la coordenada Theta de su objetivo")
args1 = parser.parse_args()

print(args1)

if args1.PosicionX:
  print( '{}{}'.format("Coordenada X: ",args1.PosicionX))
  objX = float(args1.PosicionX)

if args1.PosicionY:
  print( '{}{}'.format("Coordenada Y: ",args1.PosicionY))
  objY = float(args1.PosicionY)
if args1.Angulo:
  print( '{}{}'.format("Angulo theta: ",float(args1.Angulo)*math.pi/180))
  objTeta = float(args1.Angulo)*math.pi/180
  print(objTeta)







def callbackTime(timeVREP): #funcion para llamar tiempo de topico
    global tiempo
    timeVREP=timeVREP.data
    dt=timeVREP-tiempo
    tiempo=timeVREP


def callbackPos(posVREP): #funcion para obtener posicion segun topico
    global posVREPx, posVREPy, angleVREP
    posVREPx.append(posVREP.linear.x)
    posVREPy.append(posVREP.linear.y)
    angleVREP.append(angleVREP.angular.z)

def posActual(posVREP):
  global actualX, actualY, actualTheta, deltaX, deltaY,rho,alpha,beta
  actualX=posVREP.linear.x
  actualY=posVREO.linear.y
  actualTheta=posVREP.angular.z
  deltaX=posicionFinal[1]-actualX
  deltaY=posicionFinal[2]-actualY
  rho=math.sqrt((deltaX**2)+(deltaY**2))
  alpha=-actualTheta+math.atan2(deltaY,deltaX)
  beta=-actualTheta-alpha






def control():
  global posicionFinal, rho, alpha, beta, nrho, nalhpa, nbeta, args1
  rospy.init_node('punto3', anonymous=True) #inicializacion de nodo

  rospy.Subscriber('turtlebot_position', Twist, posActual)
  #rospy.Subscriber('simulationTime', Float32, callbackTime)
  pub=rospy.Publisher('turtlebot_cmdVel',Twist,queue_size=10)
  variable=Twist()


  #pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)
  
  rate = rospy.Rate(10) #10hz
  


      

  while not rospy.is_shutdown():
      
    if args1!=none:
      posicionFinal[1]=sys.argv[1]
      posicionFinal[2]=sys.argv[2]
      posicionFinal[3]=sys.argv[3]

      #Actualizando Rho y Alpha
      nrho=-kp*rho*cos(alpha)
      nalpha=kp*sin(alpha)-kalpha*alpha-kbeta*beta

      #Publicar Vel lineal y angular en el topico
      variable.linear=nrho
      variable.angular=(kp*sin(alpha)-kalpha*alpha)

      #Ajusta Beta despues de que el robot llegue a la pos final
      if rho==0 and alpha==0:
        beta=-kp*sin(alpha)
      rho=nrho
      alpha=nalpha

    else:
      #Actualizando Rho y Alpha
      nrho=-kp*rho*cos(alpha)
      nalpha=kp*sin(alpha)-kalpha*alpha-kbeta*beta

      #Publicar Vel lineal y angular en el topico
      variable.linear=nrho
      variable.angular=(kp*sin(alpha)-kalpha*alpha)

      #Aplica control de lazo cerrado
      if rho==0 and alpha==0:
        beta=-kp*sin(alpha)
      rho=nrho
      alpha=nalpha


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
  control()