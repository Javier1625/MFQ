#Simulating Multilevel- Feedback Queue in Python 3.9
# Input Format
# <pid> <arrival_time> <burst_time> <priority>
# Output format
# <pid Response_Time Finish_Time Waiting_Time>

#Inicialización
#Data Frame

DF=[(1,0,14,2), (2,7,8,1), (3,3,10,0), (4,5,7,2),(5,1,5,3)]
NP=len(DF) #numero de procesos
CLK=0  #Reloj global
TQ=4 #quantum de tiempo
count_process=NP
try:
    import Queue as queue
except ImportError:
    # Python 3
    import queue

import sys

def printf(format, *args):
    sys.stdout.write(format % args)
    
FQ = queue.Queue(NP) #fifo_queue
PQ = queue.PriorityQueue(NP) #priority_queue
cpu = () #indica tupla de DF de proceso en CPU
             
#PQ.put=((prioridad,PID))

#Generacion Lista de Salida
#estructura SALIDA < PID, response_time,finnish, waiting, Tac, T_ingresoCPU>

def Gen_salida(df,np): #np es el numero total de procesos
# <pid, 0> <Response, 1> <Finnish, 2> <Waiting, 3> <T_acumulado, 4><T_input_CPU>
# Response: arrival-t_ingreso_cpu. Finnish: t_exit. Waiting: arrival-Tac
	S=[]
	for i in range(np):
		S=S+[[df[i][0], 0,0,0,0,0]]
	return(S)

def quantum_time(tac,tq):
# tac es el tiempo acumulado, tq es la constante quantum_time
    if (tac !=0):
                  if (tac %tq ==0):
                      return True
    return False

SALIDA=Gen_salida(DF,NP)

def Dispatcher(t, np): #t es el tiempo,NP numero procesos
#Si hay un proceso que llega en t, lo inserta en PQ
     global cpu
     global count_process
     for i in range(np):
           if(DF[i][1] == t):
              printf("Ingresa pid= %d, en t= %d \n", DF[i][0], CLK)
              count_process=count_process-1 
              if (PQ.empty()): 
                        PQ.put((DF[i][3], i))
                        SALIDA[i][5]=CLK #se registra tiempo ingreso a cpu
                        count_process=count_process-1
                        cpu=DF[i]
              elif (cpu[3] > DF[i][3]): #el proceso en cabezo de PQ tiene menor prioridad
                            aux=PQ.get() #se saca de PQ y se instala en FQ
                            FQ.put(aux[1]) #inserta indice que staba en PQ (prioridad, i)
                            PQ.put((DF[i][3], i))
                            cpu=DF[i]
                            SALIDA[i][5]=CLK #se registra tiempo ingreso a cpu
                            #count_process=count_process-1 
              else:
                            PQ.put((DF[i][3], i))

def index_pid (pid, np): #retorna el indice en DF de proceso pid
    for i in range(np):
        if (DF[i][0] == pid):
            return i
    return -1
		

def PPQ():  #procesamiento cola de prioridad
    global cpu
    print("Procesando PPQ")
    print(cpu)
    if (not(PQ.empty())): 
        bt= cpu[2] #burst time de proceso running
        pid=cpu[0] #pid del proceso en cpu running
        I=index_pid(pid, NP) #indice de DF de pid. El pid esta en cpu
        print(cpu)
        #printf("Procesando pid= %d, I=%d, en t=%d \n", pid, I, CLK)
        if (SALIDA[I][4] == bt): #verifica si t acumulado es igual a bt								#burst
            SALIDA[I][2]= CLK # Finnish time
            SALIDA[I][1]=DF[I][1]-SALIDA[I][5] #response time
            SALIDA[I][3]=DF[I][1]-SALIDA[I][4] # waiting time
            printf("Termina proceso pid %d, en t= %d \n", pid, CLK) 
            PQ.get()  #se saca proceso de PQ
            if (not(PQ.empty())):
                I=PQ.queue[0][1]  #sin sacar de PQ se obtiene el nuevo pid running
                cpu=DF[I] #se actualiza cpu
                SALIDA[I][5]=CLK #se registra tiempo ingreso a cpu
        elif (quantum_time(SALIDA[I][4], TQ)): #verifica si se cumple quantum
            temp=PQ.get() #sale de la cola de prioridad
            FQ.put(temp[1]) #pasa a cola RR. Se inserta I
            printf("Baja proceso pid %d, en t= %d \n", pid, CLK)
            if (not(PQ.empty())):
                pid=PQ.queue[0][1]  #sin sacar de PQ obtiene el nuevo indice I
                cpu=DF[I] #se actualiza cpu
                SALIDA[I][5]=CLK #se registra tiempo ingreso a cpu             
        else:
            SALIDA[I][4] = SALIDA[I][4] +1 #se actualiza tiempo acumulado
		
n=20
for CLK in range(n):
              Dispatcher(CLK,NP)
              PPQ()
              print(PQ.queue)
              print(FQ.queue)
              print(count_process)
                                             
              

                



                            

     
