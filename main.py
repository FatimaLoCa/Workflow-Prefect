import os
import datetime
from tabulate import tabulate

from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule

index = 0

@task
def leer_solicitud():
    #index = 0
    #se lee una solicitud de compra un archivo de texto
    file = open('solicitudes.txt','r')
    solicitudes = list(enumerate(file))
    global index
    soli = solicitudes[index]
    print(soli)
    file.close()
    index += 1
    return soli

@task 
def validar_solicitud(solicitud):
    #se valida que todos los productos estén disponibles
    #print(solicitud)
    products = {'Cadena' : 50, 
                'Bolso' : 150,
                'Blusa' : 130,
                'Cartera' : 120,
                'Pantalon' : 240,
                'Vestido' : 230,
                'Cinturon' : 100,
                'Reloj' : 300,
                'Camisa' : 130}

    products_s = solicitud[1].split(", ")
    fin = []

    if (len(products_s)-1) == " ":
            return [], ''
    for i in range(0, len(products_s)-1):
        pl = products_s[i].split(" ")
        pl.append(products[pl[1]])
        fin.append(pl)

    name = products_s[len(products_s)-1]

    return (fin, name)


@task
def crear_pedido(datos):
    #Se crea un pedido de compra y se manda a un archivo
    #print(products)
    products = datos[0]
    name = datos[1].replace("\n","")
    if len(products) == 0:
        return "no hay datos"
    
    namef = "Pedido - "+name+".txt"
    
    file = open(namef, "w")
    file.write("Pedido - "+name+"\n")
    #print(tabulate(products, headers = ['Cantidad', 'Producto', 'Precio uni']))
    file.write(tabulate(products, headers = ['Cantidad', 'Producto', 'Precio uni']))
    total = 0
    for i in range(0,len(products)):
        total += (int(products[i][0]) * products[i][2])

    file.write("\n----------------------- TOTAL: "+ str(total))

    file.close()


schedule = IntervalSchedule(interval = datetime.timedelta(seconds = 5))

with Flow("Solicitud y pedido de compra", schedule) as fl:
    s = leer_solicitud()
    v = validar_solicitud(s)
    p = crear_pedido(v)


fl.run()