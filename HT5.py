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

for i in range(initial_procesos):
    llegada=intervalo
    cantidad_instrucciones = random.randint(1, 10)
    UsoRam = random.randint(1, 10)
    iString=str(i)
    Procesos["Proceso "+ iString]=["Proceso "+iString, env, initial_ram, llegada, cantidad_instrucciones, UsoRam]
    intervalo+=1

for i in range(len(Procesos)):
    iString=str(i)
    Proceso_en_uso=Procesos.get("Proceso "+iString)
    nombre=Proceso_en_uso[0]
    env=Proceso_en_uso[1]
    memoria=Proceso_en_uso[2]
    llegada=Proceso_en_uso[3]
    cantidad_instrucciones=Proceso_en_uso[4]
    UsoRam=Proceso_en_uso[5]
    Tiempo[nombre]=llegada
    env.process()

env.run()
