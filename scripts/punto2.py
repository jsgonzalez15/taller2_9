#!/usr/bin/env python
from std_msgs.msg import Float32, Float32MultiArray
from geometry_msgs.msg import Twist
import  matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import threading
import rospy
import sys

# Variables globales
global tiempoCero, i, numVel,vels,tiempo
i = 0
tiempoCero = 0
l = 0.23  # metros

ruta = '/home/jsgonzalez15/robotica_ws/src/taller2_9/resources/'
nombre = sys.argv[1]
vels = np.loadtxt(ruta+nombre+'.txt')
numVel = vels[0,0]

# angulo inicial
theta = [-np.pi/4]

# Datos para las graficas
tiempo = [0]
posVREPx = []
posVREPy = []
posODOx = [0]
posODOy = [0]
#---

# Funcion que recibe el tiempo de simulacion de VREP y
# calcula la odometria del robot y cambia de velocidades
# de acuerco con lo establecido en el archivo txt
def callbackTime(data):
  global tiempoCero, i, numVel,vels
  tiempo.append(data.data)
  if tiempoCero == 0:
    tiempoCero = data.data
  if i < numVel:
    dt = 0.08
    Vr = 0.01*vels[i+1,0] # Se pasa a metros
    Vl = 0.01*vels[i+1,1] # Se pasa a metros
    # Calculo de odometria
    posODOx.append( posODOx[-1] + (0.5*(Vr+Vl)*np.cos(theta[-1])*dt ))
    posODOy.append( posODOy[-1] + (0.5*(Vr+Vl)*np.sin(theta[-1])*dt ))
    theta.append( theta[-1] + 1/l*(Vr-Vl)*dt)

    # Tiempo transcurrido en la velocidad actual
    tiempoVel = data.data - tiempoCero

    if tiempoVel >= vels[i+1,2]:
      i+=1
      tiempoCero = 0

# Funcion que recibe la posicion del robot dada por VREP
# y la almacena para graficarla
def callbackPos(pos):
  global posVREPx, posVREPy
  posVREPx.append(pos.linear.x)
  posVREPy.append(pos.linear.y)

# Datos y propiedades de la grafica en tiempo real
def graficar(i):
  plt.cla() #Se borra informacion anterior al ploteo actual
  plt.plot(posVREPx,posVREPy,'b')
  plt.plot(posODOx, posODOy, 'g')
  plt.axis([-2.5,2.5,-2.5,2.5]) #Define limites en X y en Y

# Funcion que crea la grafica en tiempo real
def realTime():
  objeto=animation.FuncAnimation(plt.figure(1),graficar,10000) #plt.gcf get currently figure Animar las figuras por parametro de manera iterativa
  plt.show()

# Funcion principal que inicializa el nodo y se suscribe o publica segun sea el caso
def tYl():
  global tiempoCero, i, numVel,vels,tiempo,posODOx,posODOy

  # Inicializa el nodo
  rospy.init_node('punto2_talker', anonymous=True)

  # Se suscribe a los topicos de posicion y tiempo de simulacion
  rospy.Subscriber('turtlebot_position', Twist, callbackPos)
  rospy.Subscriber('simulationTime', Float32, callbackTime)

  # Crea el publicador para la velocidad de las ruedas
  pub = rospy.Publisher('turtlebot_wheelsVel', Float32MultiArray, queue_size=10)

  # Crea un hilo para la grafica en tiempo real
  RTgraph = threading.Thread(target=realTime)
  RTgraph.start()

  rate = rospy.Rate(10) #10hz

  # Publica las velocidades dadas por el archivo txt y cuando termina
  # publica velocidades de cero
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
