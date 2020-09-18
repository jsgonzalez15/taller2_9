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

'''----------------Transformacion de coordenadas a marco global----------------'''
robotXglobal=1 #coordenada x del robot con respecto a marco global
robotYglobal=0.5 #coordenada y del robot con respecto a marco global
gThetar=np.pi/4 #angulo de marco del robot con resp...
gRr=np.array([[np.cos(gThetar),-np.sin(gThetar),robotXglobal],[np.sin(gThetar),np.cos(gThetar),robotYglobal],[0,0,1]])

sensorXrobot=0.2  #coordenada x del sensor con respecto a marco robot
sensorYrobot=0 #coordenada y del sensor con respecto a marco robot
rThetas=0 #angulo de marco del sensor con resp...
rRs=np.array([[np.cos(rThetas),-np.sin(rThetas),sensorXrobot],[np.sin(rThetas),np.cos(rThetas),sensorYrobot],[0,0,1]])
sensorXglobal= np.dot(np.dot(gRr,rRs),np.array([[0],[0],[1]]))[0]
sensorYglobal= np.dot(np.dot(gRr,rRs),np.array([[0],[0],[1]]))[1]

arrayX=np.array(posicionx) #transformacion a arrays para analisis
arrayY=np.array(posiciony)
posicionXglobal=[] #posicion en coordenadas globales
posicionYglobal=[]
#incluir lineas de sensado 
lineaSensadax=[0]
lineaSensaday=[0]
for i in range(len(posicionx)):
    transfActual=np.dot(np.dot(gRr,rRs),np.array([[posicionx[i]],[posiciony[i]],[1]]))
    posicionXglobal.append(transfActual[0])
    posicionYglobal.append(transfActual[1])
    lineaSensadax.append(posicionx[i])
    lineaSensaday.append(posiciony[i])
    lineaSensadax.append(0)
    lineaSensaday.append(0)
    '''
    lineaSensadax.append(posicionXglobal[i])
    lineaSensaday.append(posicionYglobal[i])
    lineaSensadax.append(sensorXglobal)
    lineaSensaday.append(sensorYglobal)
    '''
#plt.plot(lineaSensadax,lineaSensaday,'r--',LineWidth=0.2,label='rayoSensor') #grafica de lineas de sensado'''

#plt.scatter(theta,laserdata) #Plotea la lectura

plt.scatter(posicionx,posiciony,s=1,label='medicionSensor') #plotea la medicion en el marco del sensor
plt.scatter(0,0,marker='x',label='posicionSensor',c='r') #plotea la posicion del sensor local
plt.scatter(-sensorXrobot,-sensorYrobot,marker='x',label='posicionRobot',c='b') #plotea la posicion del sensor globalmente

print(posicionXglobal)
print(posicionYglobal)

'''
plt.scatter(posicionXglobal,posicionYglobal,s=1,label='medicionSensorGlobal') #plotea la medicion en el marco global
plt.scatter(sensorXglobal,sensorYglobal,marker='x',label='posicionSensorGlobal',c='r') #plotea la posicion del sensor globalmente
plt.scatter(robotXglobal,robotYglobal,marker='x',label='posicionRobotGlobal',c='b') #plotea la posicion del robot globalmente
'''
plt.title('Mediciones Sensor')
#plt.xlabel('x marco global (m)')
#plt.ylabel('y marco global (m)')
plt.xlabel('x marco local sensor (m)')
plt.ylabel('y marco local sensor (m)')

#plt.axis([-1,1,-1,1]) #Define limites en X y en Y
plt.legend()
#plt.grid()
figure=plt.gcf()
figure.set_size_inches(10,6)

#plt.savefig('medicionSensorInercial.jpeg',dpi=100)
#plt.savefig('medicionSensorInercialLineas.jpeg',dpi=100)
#plt.savefig('medicionSensorGlobal.jpeg',dpi=100)
#plt.savefig('medicionSensorGlobalLineas.jpeg',dpi=100)
plt.show()


