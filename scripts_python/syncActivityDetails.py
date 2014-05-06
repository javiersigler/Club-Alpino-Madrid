__author__ = 'fjsg'

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from mongoengine import *

connect('app24921821', host='localhost')

class Activity(Document):
    id = LongField(required=True, primary_key=True)
    href = LongField()
    fromDate = DateTimeField()
    toDate = DateTimeField()
    title = StringField()
    type = StringField()
    tipo_de_transporte = StringField()
    gastos_de_compartir_coche = StringField()
    distancia_del_recorrido = StringField()
    pernocta = StringField()
    número_de_actividad = StringField()
    desnivel_positivo = StringField()
    lugar = StringField()
    reserva_alojamiento = StringField()
    tiempo_de_duración = StringField()
    desnivel_negativo = StringField()
    tipo_de_dificultad = StringField()
    fecha_de_celebración = StringField()
    participantes = StringField()
    tipo_de_actividad = StringField()
    fecha_límite_de_registro = StringField()
    thumbnail = StringField()

keys = set()
def insertActivityDetails(activity):
    activity.delete()
    print( 'id: ' + str(activity.id) + ', href: ' + str(activity.href))
    html = urlopen('http://www.clubalpino.es/joomla/index.php?option=com_clubalpino&task=info&id=' + str(activity.href))
    htmlBody = html.read()

    soup = BeautifulSoup(htmlBody)
    soup = soup.find("div", { "class" : "ficha_tecnica" })
    array = soup.get_text('\n', strip=True).split('\n')
    map = {array[i].replace(' ', '_').lower(): array[i+1] for i in range(0, len(array), 2)}
    print(map)

    for key, value in map.items():
        keys.add(key)
        setattr(activity, key, value)

    activity.save(force_insert=True, clean=False)


activity = Activity()
for item in Activity.objects:
    insertActivityDetails(item)
    time.sleep(0.1)

print(keys)