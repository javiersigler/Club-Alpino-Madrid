__author__ = 'fjsg'

from urllib.request import urlopen
from bs4 import BeautifulSoup
from dateutil import parser
from mongoengine import *
import re

connect('activities', host='localhost')

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

Activity.drop_collection()
html = urlopen('http://www.clubalpino.es/joomla/index.php?option=com_clubalpino')
htmlBody = html.read()

soup = BeautifulSoup(htmlBody)
soup = soup.find(id="main")
activities = set()
for line in soup.find_all('li'):
    activity = Activity()
#    print(str(line.get_text()))
    for span in line.find_all('span'):
        if span['class'] == ["fecha"]:
            date = line.span.string.split(' al ')
            activity.fromDate = parser.parse(date[0])
            if len(date) > 1:
                activity.toDate = parser.parse(date[1])
            else:
                activity.toDate = activity.fromDate
        else:
            activity.type = span.a.string
    activity.href = int(line.a['href'][43:-10])
    ref = line.a.string.strip()

    activity.id = int(re.search('-\s?\d{3,}', ref).group(0).strip('-').strip())
    activity.title = ref.replace(str(activity.id), '').replace('-', '').strip()
    activities.add(activity)
    activity.save(force_insert=True, clean=False)
#   print('from: ' + str(activity.fromDate) + ', to: ' + str(activity.toDate) + ', name: ' + str(activity.title) + ', id: ' + str(activity.id) + ', type: ' + str(activity.type) + ', href: ' + str(activity.href))
