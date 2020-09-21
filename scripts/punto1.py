#!/usr/bin/env python3
#import rospy
import matplotlib.pyplot as plt #Libreria para graficar
import numpy as np
from matplotlib import animation
import threading
 
laserdata=np.loadtxt('laserscan.dat') #lectura de archivo con mediciones del sensor
num_data=len(laserdata) #size de medicion
theta=np.linspace(-np.pi/2, np.pi/2, num_data) #angulos medidos
posicionx=laserdata*np.cos(theta) #posicionx equivalente de medicion
posiciony=laserdata*np.sin(theta) #posiciony equivalente de medicion

verLOCAL=True #variable para ver figura local o global
verLASER=False #variable para ver laser en figura

'''----------------------------------------------------------------------------'''
'''----------------Transformacion de coordenadas a marco global----------------'''
'''----------------------------------------------------------------------------'''

robotXglobal=1 #coordenada x del robot con respecto a marco global
robotYglobal=0.5 #coordenada y del robot con respecto a marco global
gThetar=np.pi/4 #angulo de marco del robot con resp...
#Matriz de transformacion globalRobot
gRr=np.array([[np.cos(gThetar),-np.sin(gThetar),robotXglobal],[np.sin(gThetar),np.cos(gThetar),robotYglobal],[0,0,1]])

sensorXrobot=0.2  #coordenada x del sensor con respecto a marco robot
sensorYrobot=0 #coordenada y del sensor con respecto a marco robot
rThetas=0 #angulo de marco del sensor con resp...

#Matriz de transformacion robotSensor
rRs=np.array([[np.cos(rThetas),-np.sin(rThetas),sensorXrobot],[np.sin(rThetas),np.cos(rThetas),sensorYrobot],[0,0,1]])
sensorXglobal= np.dot(np.dot(gRr,rRs),np.array([[0],[0],[1]]))[0] #PosicionX global del sensor
sensorYglobal= np.dot(np.dot(gRr,rRs),np.array([[0],[0],[1]]))[1] #PosicionY global del sensor

arrayX=np.array(posicionx) #transformacion a arrays para analisis
arrayY=np.array(posiciony)
posicionXglobal=[] #posicion en coordenadas globales
posicionYglobal=[]
#incluir lineas de sensado 
lineaSensadax=[0]
lineaSensaday=[0]
for i in range(len(posicionx)):
    #Transformacion a coordenadas globales de posicion i/esima
    transfActual=np.dot(np.dot(gRr,rRs),np.array([[posicionx[i]],[posiciony[i]],[1]]))
    posicionXglobal.append(transfActual[0]) #guardado de transformacion coordenada X
    posicionYglobal.append(transfActual[1]) #guardado de transformacion coordenada y
    if verLOCAL:
        lineaSensadax.append(posicionx[i])
        lineaSensaday.append(posiciony[i])
        lineaSensadax.append(0)
        lineaSensaday.append(0)
    else:
        lineaSensadax.append(posicionXglobal[i])
        lineaSensaday.append(posicionYglobal[i])
        lineaSensadax.append(sensorXglobal)
        lineaSensaday.append(sensorYglobal)

if verLASER:
    plt.plot(lineaSensadax,lineaSensaday,'r--',LineWidth=0.2,label='rayoSensor') #grafica de lineas de sensado

if verLOCAL:
    plt.scatter(posicionx,posiciony,s=1,label='medicionSensor') #plotea la medicion en el marco del sensor
    plt.scatter(0,0,marker='x',label='posicionSensor',c='r') #plotea la posicion del sensor local
    plt.scatter(-sensorXrobot,-sensorYrobot,marker='x',label='posicionRobot',c='b') #plotea la posicion del sensor globalmente
    plt.title('Mediciones Sensor')
    plt.xlabel('x marco local sensor (m)')
    plt.ylabel('y marco local sensor (m)')
    plt.legend()
    figure=plt.gcf()
    figure.set_size_inches(10,6)
    if verLASER:
        plt.savefig('medicionSensorLocalLineas.jpeg',dpi=100) #guardado figura local con rayosLaser
    else:
        plt.savefig('medicionSensorLocal.jpeg',dpi=100) #guardado figura local sin rayosLaser
else:
    plt.scatter(posicionXglobal,posicionYglobal,s=1,label='medicionSensorGlobal') #plotea la medicion en el marco global
    plt.scatter(sensorXglobal,sensorYglobal,marker='x',label='posicionSensorGlobal',c='r') #plotea la posicion del sensor globalmente
    plt.scatter(robotXglobal,robotYglobal,marker='x',label='posicionRobotGlobal',c='b') #plotea la posicion del robot globalmente
    plt.title('Mediciones Sensor')
    plt.xlabel('x marco global (m)')
    plt.ylabel('y marco global (m)')
    plt.legend()
    figure=plt.gcf()
    figure.set_size_inches(10,6)
    if verLASER:
        plt.savefig('medicionSensorGlobalLineas.jpeg',dpi=100) #guardado figura global con rayosLaser
    else:
        plt.savefig('medicionSensorGlobal.jpeg',dpi=100) #guardado figura global sin rayosLaser
plt.show()


