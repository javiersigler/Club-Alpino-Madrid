__author__ = 'fjsg'

from urllib.request import urlopen
import urllib
import json
import time
from mongoengine import *

connect('javierca', host='localhost')

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
    print( 'id: ' + str(activity.id))
    ip = "82.158.56.212"
    query = activity.lugar
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+ urllib.parse.quote_plus(query) + '&rsz=1&userip='+ ip;
    raw = urlopen(url)
    raw = raw.read().decode(encoding='UTF-8');
    thumbnail = json.loads(raw)
    activity.thumbnail = thumbnail['responseData']['results'][0]['tbUrl']
    print(activity.thumbnail)

    activity.save(force_insert=True, clean=False)


activity = Activity()
for item in Activity.objects:
    insertActivityDetails(item)
    time.sleep(0.1)

print(keys)