import simpy
import random
random.seed(0)

Procesos={}
IO={}
CPU={}
Tiempo={}
TInicial={}
intervalo=0

env=simpy.Environment()
initial_ram = simpy.Container(env, 100, init=100)
initial_cpu = simpy.Resource(env, capacity=2)
initial_procesos = 200
def proceso(nombre, env, memoria, llegada, tiempo_CPU, usoRam):

    yield env.timeout(llegada)
    print('%s proceso en cola NEW --> %d cantidad ram requerida %d' % (nombre, env.now, usoRam))
    memoria.get(usoRam)
    procesoEnUso=Procesos.get(nombre)
    CPU[nombre]=procesoEnUso
    print('%s proceso en cola READY --> %d Cantidad de ram %d' % (nombre, env.now, usoRam))
    with initial_cpu.request() as req:
        yield req
        tiempo_CPU=tiempo_CPU-3
    if tiempo_CPU<=0:
        print('%s proceso ha salido de la cola RUNNING --> %s' %(nombre, env.now))
        tFinal=env.now
        tInicial=TInicial[nombre]
        prom=tFinal-tInicial
        Tiempo[nombre]=[prom]
        memoria.put(usoRam)
        CPU.pop(nombre)
        for i in range(len(Tiempo)):
            key1=list(Tiempo.items())[i][0]
            print(Tiempo[key1])
    elif tiempo_CPU>0:
        n1=random.randint(1, 2)
        if n1==1:
            procesoEnUso=CPU.get(nombre)
            nombre=procesoEnUso[0]
            env=procesoEnUso[1]
            memoria=procesoEnUso[2]
            llegada=procesoEnUso[3]
            tiempo_CPU=tiempo_CPU
            usoRam=procesoEnUso[5]
            env.process(proceso(nombre, env, memoria, llegada, tiempo_CPU, usoRam))
        else:
            IO[nombre]=CPU.get(nombre)

    while len(IO)>0:
        if len(IO)>=1:
            n2=random.randint(1,2)
            if n2==1:
                key2=list(IO.items())[0][0]
                print('%s proceso en cola Ready --> %s' % (nombre, env.now))
                procesoEnUso=IO.get(key2)
                nombre = procesoEnUso[0]
                env = procesoEnUso[1]
                memoria = procesoEnUso[2]
                llegada = procesoEnUso[3]
                tiempo_CPU = tiempo_CPU
                usoRam = procesoEnUso[5]
                IO.pop(key2)
                env.process(proceso(nombre, env, memoria, llegada, tiempo_CPU, usoRam))



for i in range(initial_procesos):
    llegada=intervalo
    tiempo_CPU = random.randint(1, 10)
    UsoRam = random.randint(1, 10)
    iString=str(i)
    Procesos["Proceso "+ iString]=["Proceso "+iString, env, initial_ram, llegada, tiempo_CPU, UsoRam]
    intervalo+=1

for i in range(len(Procesos)):
    iString=str(i)
    Proceso_en_uso=Procesos.get("Proceso "+iString)
    nombre=Proceso_en_uso[0]
    env=Proceso_en_uso[1]
    memoria=Proceso_en_uso[2]
    llegada=Proceso_en_uso[3]
    tiempo_CPU=Proceso_en_uso[4]
    UsoRam=Proceso_en_uso[5]
    TInicial[nombre]=llegada
    env.process(proceso(nombre, env, memoria, llegada, tiempo_CPU, UsoRam))

env.run()
