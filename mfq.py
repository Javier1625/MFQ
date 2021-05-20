#!/usr/bin/python3
#Simulating Multilevel- Feedback Queue in Python 3.9
#Javier Cañas R.
#mayo de 2021
# Input Format
# <pid> <arrival_time> <burst_time> <priority>
# Output format
# <pid Response_Time Finish_Time Waiting_Time>

#Inicialización
#Data Frame
Lista=[ ]
try:
    import Queue as queue
except ImportError:
    # Python 3
    import queue
from statistics import * 
import sys



################# Valores por defecto###############
INPUT=[(1,0,14,2), (2,7,8,1), (3,3,10,0), (4,5,7,2),(5,1,5,3)]
TQP=4 #quantum de tiempo cola prioridad. Valor por defecto
TQF=4 #quantum de tiempo cola FIFO. Valor por defecto

def printf(format, *args):
    sys.stdout.write(format % args)

import csv

if (sys.argv[1] =='-h'):
            printf("usage: mfq.py [file cvs] [quantum time priority queue] [quantum time RR queue]")
            printf("format csv file: pid, arrival_time, burst_time, priority ")
            exit()

if (len(sys.argv) >1):
    with open(sys.argv[1],'r') as csvfile:
            reader = csv.reader(csvfile,quoting=csv.QUOTE_NONNUMERIC , skipinitialspace=True)
            for row in reader:
                        l=map(int, row)
                        row=tuple(l)
                        Lista.append(row)
            INPUT=Lista
if (len(sys.argv)>2):
            TQP=int(sys.argv[2])
            printf("TQP= %d \n", TQP)

if (len(sys.argv) >3):
            TQF=int(sys.argv[3])
            printf("TQF= %d \n", TQF)
            

##print(Lista)
##if (len(sys.argv) == 4):
##            TQF=int(sys.argv[3])
##            TQP=int(sys.argv[2])
##elif ((len(sys.argv) == 3):
##            TQP=int(sys.argv[2])
##elif (((len(sys.argv) == 2):
##             INPUT=Lista
            

# Variables Globales #
#INPUT=Lista


NP=len(INPUT) #numero de procesos
CLK=0  #Reloj global
#TQP=int(sys.argv[2])


FQ = queue.Queue(NP) #fifo_queue
PQ = queue.PriorityQueue(NP) #priority_queue
CIP=0 #Count Inserted Process
CPU_P=-1
#CPU_P=(0, 0)
CPU_F=-1  #indice cola FIFO
Qt_FIFO=1 #quantum time cola FIFO
FIN=False #Se termino el procesamiento
MAXTIME=60 #maximi tiempo de procesamiento

#reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)


#Funciones #

#Generacion Tabla de Salida
#estructura OUTPUT < PID, response_time,finnish, waiting, Tac>

def Gen_salida(): #np es el numero total de procesos
# <pid, 0> <Response, 1> <Finnish, 2> <Waiting, 3> <T_acumulado, 4>
# Response: arrival-t_ingreso_cpu. Finnish: t_exit. Waiting: arrival-Tac
	S=[]
	for i in range(NP):
		S=S+[[INPUT[i][0], 0,0,0,0]]
	return(S)


def show (E,tipo):
    if (tipo =="entrada"):
        printf("Pid    Arr_t       Burst_t     Prio \n")
    elif (tipo =="salida"):
        printf("Pid  Resp_t     Finn_t      Wait_t \n")
    for i in range(len(E)): 
        printf("%-5d     %-5d     %-5d       %-5d \n", E[i][0], E[i][1], E[i][2], E[i][3])
    if   (tipo =="salidas"):
        printf("Pid    Resp_t    Finn_t     Wait_t    Acut \n")
        for i in range(len(E)): 
            printf("%-5d     %-5d     %-5d       %-5d  \n", E[i][0], E[i][1], E[i][2], E[i][3], E[i][4])
       


def A_time(I):
# Arrival time
    return (INPUT[I][2])

def Prio(I):
#Prioridad
    return (INPUT[I][3])

def Select(t):
    for i in range(NP):
        if(INPUT[i][1] == t):
            return ((Prio(i),i))
    return(-1)

def Set_Accumt(i):
 # Fija tiempo acumulado
    OUTPUT[i][4]=OUTPUT[i][4]+1
   

def Set_resp_time(i):
# Fija tiempo de respuesta
    OUTPUT[i][1]=CLK-INPUT[i][1]

def Set_Finnish_time(i):
# Fija tiempo de respuesta
    OUTPUT[i][2]=CLK+1

def Set_wait_time(i):
    OUTPUT[i][3]=OUTPUT[i][2]-OUTPUT[i][4]-INPUT[i][1] # Waiting time
    

def Pid(i):
    return(INPUT[i][0])

def Tacc(i):
    return(OUTPUT[i][4])

def Quantum_timeP(i):
#determina si se cumplio quantum para cola de prioridad
    if (Tacc(i)==TQP):
        return True
    else:
        return False
    
def Quantum_timeF(i):
#determina si se cumplio quantum para cola de prioridad
    if (Qt_FIFO==TQF):
        return True
    else:
        return False


def Burstime(i):
   if (OUTPUT[i][4]==INPUT[i][2]):
       return True
   else:
       return False

def Mayor_prioridad(pc,pt):
#determina si hay que bajar proceso
    if (pc > pt):
        return(True)
    else:
        return(False) 
    
def PFQ():
        global CPU_F
        global Qt_FIFO
        global FIN
        global CLK
        if (FQ.empty() and FIN):
            return
        if (CPU_F == -1):
            CPU_F=FQ.get()
            Set_Accumt(CPU_F)       
        if(Burstime(CPU_F)):
              Set_Finnish_time(CPU_F)
              Set_wait_time(CPU_F)
              if (FQ.empty()):
                  FIN=True
                  return
              else:          
                  CPU_F=FQ.get() #Se saca el primer elemento de la cola y se actualiza CPU_F
                  Qt_FIFO=0
        if (Quantum_timeF(CPU_F)):
                    FQ.put(CPU_F)
                    CPU_F=FQ.get()
                    Qt_FIFO=0             
        Qt_FIFO=Qt_FIFO+1
        Set_Accumt(CPU_F)
        

OUTPUT=Gen_salida()
  
def PPQ():
    global CIP
    global CPU_P
    tupla=-1
    if (CIP == NP and PQ.empty()):
        return
    if (CIP < NP):
        tupla=Select(CLK)
        if (tupla !=-1):
            CIP=CIP+1
    if ((tupla !=-1) and (PQ.empty())):
        PQ.put(tupla)
        Set_resp_time(tupla[1])
        CPU_P=tupla
        tupla=-1
    elif ((tupla !=-1) and  ( CIP <= NP)):
        if (Mayor_prioridad(CPU_P[0], tupla[0])): #Baja por prioridad
                    aux=PQ.get() #se saca de PQ para instalar en FQ
                    FQ.put(aux[1]) #inserta indice que estaba en PQ
                    PQ.put(tupla)
                    CPU_P=tupla
                    Set_resp_time(CPU_P[1])
                    tupla=-1
        if (Quantum_timeP(CPU_P[1])):
                    aux=PQ.get() #se saca de PQ para instalar en FQ
                    FQ.put(aux[1]) #inserta indice que estaba en PQ (prioridad, i)
                    PQ.put(tupla)
                    CPU_P=tupla
                    Set_resp_time(CPU_P[1])
                    tupla=-1
        else:
                    pass
########### No hay mas inserciones ################## 
    if( Burstime(CPU_P[1])):
              aux=PQ.get() #se saca de PQ para instalar en FQ
              FQ.put(aux[1]) #inserta indice que estaba en PQ (prioridad, i)
              Set_resp_time(CPU_P[1])
              Set_wait_time(CPU_P[1])
              Set_Finnish_time(CPU_P[1])
              if (not(PQ.empty())):
                        CPU_P=PQ.queue[0] #toma el primer elemento de la cola
    if (Quantum_timeP(CPU_P[1])):
                    aux=PQ.get() #se saca de PQ para instalar en FQ
                    FQ.put(aux[1]) #inserta indice que estaba en PQ (prioridad, i)
                    if (not(PQ.empty())):
                        CPU_P=PQ.queue[0] #toma el primer elemento de la cola en CP
                        Set_resp_time(CPU_P[1])
    if (tupla !=-1):
        PQ.put(tupla)
    
    if (not(PQ.empty())):
         Set_Accumt(CPU_P[1])
    

 #Procesamiento estadistico
Rp=[] #tiempo de respuesta
Ft=[] #tiempo de termino
Wt=[] #tiempo de espera
Tat=[] #turn around time

def Estadistica():
    global Rp, Ft, Wt, Tat
    for i in range(NP):
        Rp=Rp+[OUTPUT[i][2]]
        Ft=Ft+[OUTPUT[i][3]]
        Wt=Wt+[OUTPUT[i][4]]
        Tat=Tat+[OUTPUT[i][3]-INPUT[i][1]]
    Rpm=mean(Rp)
    Ftm=mean(Ft)
    Wtm=mean(Wt)
    Tatm=mean(Tat)
    printf("Tiempo de Respuesta Promedio=%.1f \n", Rpm)
    printf("Tiempo de Termino Promedio=%.1f \n", Ftm)
    printf("Tiempo de Espera Promedio=%.1f \n", Wtm)
    printf("Turn Around Time Promedio=%.1f \n", Tatm)
    

for CLK in range (MAXTIME):
    PPQ()
    if (PQ.empty()):
        PFQ()
    if (FIN):
        break
print("       Data Frame Entrada")
show(INPUT, "entrada")
print()
print("       Data Frame Salida")
printf("Quantum time: Cola Prioridad= %d, Cola RR= %d \n", TQP, TQF)
printf("Se termino de procesar en t=%d \n", CLK+1)
show(OUTPUT, "salida")
Estadistica()
    
           



                            

     
