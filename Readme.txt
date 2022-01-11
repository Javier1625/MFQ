# MFQ
Esta aplicación implementa una simulación de Múltiples colas realimentadas en Python 3.9.
Es un desarrollo "from the scrath" a partir de las especificaciones del simulador escrito por 
Aneel Balda (https://github.com/aneelbalda/MLFQ/blob/master/mlfq.cpp).
El simulador tiene dos niveles:
Nivel1: Prioridad fija itineración interrumpible
Nivel2: Itineración Round Robin
===========================================================
                        DETALLES DEL SIMULADOR
===========================================================
Cola1
 * Nivel1: La prioridad más alta es 0
 * Quantum inicialmente es 4, pero es configurable
 * Interrumpible: Si un proceso P1 está siendo itinerado y llega P2 con mayor prioridad,
   P1 baja a la cola ROUND ROBIN (Nivel 2) y se itinera P2
   
Cola2
 * Round Robin
 * Quantum inicialmente es 4, pero es configurable
 * Esta cola se procesa solo cuando la Cola 1 está vacía
 * Entonces, la Cola2 tiene menor prioridad que la Cola1
 
Supongamos que la Cola1 está vacía y se está procesando un proceso en Cola2. En este caso
como Cola1 tiene mayor prioridad se itinera Cola1, y cuando ésta está vacía se continua 
con Cola2

El formato de la entrada es:
===========================================================
                      INPUT FORMAT
===========================================================
<pid> <arrival_time> <burst_time> <priority>

===========================================================
                      OUTPUT FORMAT
===========================================================

<pid Response_Time Finish_Time Waiting_Time >


Un ejemplo de entrada es:

===========================================================
                      Sample Input :
===========================================================
1 0 14 2
2 7 8  1
3 3 10 0
4 5 7  2
5 1 5  3

       Data Frame Entrada
Pid    Arr_t       Burst_t     Prio 
1         0         14          2     
2         7         8           1     
3         3         10          0     
4         5         7           2     
5         1         5           3     

       Data Frame Salida
Quantum time: Cola Prioridad= 4, Cola RR= 4 
Se termino de procesar en t=44 
Pid  Resp_t     Finn_t      Wait_t 
1         0         44          30    
2         0         31          16    
3         0         41          28    
4         6         34          22    
5         14        35          29    
Tiempo de Respuesta Promedio=4.0 
Tiempo de Termino Promedio=37.0 
Tiempo de Espera Promedio=25 
Turn Around Time Promedio=33.8 

Este Data Frame es por defecto y se encuentra el el código como lista de tuplas:
INPUT=[(1,0,14,2), (2,7,8,1), (3,3,10,0), (4,5,7,2),(5,1,5,3)]

La entrada se puede obtener de un archivo CSV:
Por ejemplo:

1 , 0 , 14 ,  2     
2 , 7 ,  8 ,  1     
3 , 3 , 10 ,  0     
4 , 5 ,  7 ,  2     
5 , 1 ,  5 ,  3 

javiercanas@MacBook-Pro-de-Javier MFQ_Python % ./mfq.py -h  
usage: mfq.py [file cvs] [quantum time priority queue] [quantum time RR queue]
format csv file: pid, arrival_time, burst_time, priority % 
