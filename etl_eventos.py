# -*- coding: cp1252 -*-
import re
import json
# debe ser bajado por pip
from unidecode import unidecode
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time
from parsers import nameParser

def formattedCountryString(country_string):
    return country_string.replace(' ','_').strip().lower()

BASE_URI = 'http://datos.uchile.cl/'

dic = {
    'xmlns:owl': BASE_URI + 'ontologia/',
    'xmlns:dct': 'http://purl.org/dc/terms/',
    'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xmlns:schema': 'http://schema.org'
}

output = {
    'event_root' : ET.Element( 'rdf:RDF', dic ) #Base element for events
    #'year_root' : ET.Element( 'rdf:RDF', dic ) #Years
}

countriesSet = set([])
citiesSet = set([])

#leer los json y cargarlos en los conjuntos

with open('localizations/paises.json') as data_file:    
    data = json.load(data_file)
for key in data.keys():
    countriesSet.add(unidecode(data[key]))
with open('localizations/ciudades_chile.json') as data_file:    
    data = json.load(data_file)
for d in data:
    citiesSet.add(unidecode(d))

i = 0
for event, elem in ET.iterparse( 'input/autoridades-eventos.xml', events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
    if event != 'end' or elem.tag != 'authority': continue
    authority = elem
    authIDElement = authority.find('authorityID')

    if authIDElement == None or authIDElement.text == None: continue
    authID = authIDElement.text

    nameElement = authority.find( ".//*[@tag='111']" )
    if nameElement == None or nameElement.text == None: continue
    
    marcEntryTextArray = nameElement.text.split('|')
    if len(marcEntryTextArray) == 1: continue

    eventElement = ET.SubElement( output['event_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'recurso/evento/' + authID} )

    # caso nombre
    name = ""
    for part in marcEntryTextArray:
        name = name + part[1:]
    # crear elemento nombre
    nameElement = ET.SubElement(eventElement, 'dct:title')
    nameElement.text = name

    # caso nombre alternativo
    altNameElement = authority.find( ".//*[@tag='670']" )
    if altNameElement != None:
        altName = altNameElement.text
        altName = altName[2:]
        altNameElement = ET.SubElement(eventElement, 'dct:alternative')
        altNameElement.text = altName

    for entry in marcEntryTextArray:
        if entry == '': continue
        # caso fechas
        if entry[0] == 'd':
            # arreglo de fechas
            year = entry[1:]
            # saco todos los caracteres que no son números
            year = re.sub("[^0-9]", "", year)
            # se agrega fecha al elemento
            yearElement = ET.SubElement(eventElement, 'schema:startDate', {'rdf:datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'})
            yearElement.text = year
        # caso localidad
        
        if entry[0] == 'c':
            locationString = ""
            # unidecodear entry
            try:
                entry = unidecode(entry)
            except Warning:
                # caso en que el nombre de la autoridad contiene caracteres que no pueden ser decodificados
                continue
            # se busca el nombre de la ciudad o país para estandarizarlo
            found = False
            for city in citiesSet:
                if entry.find(city) != -1:
                    locationString = city
                    found = True
                    break
            if not found:
                for country in countriesSet:
                    if entry.find(country) != -1:
                        locationString = country
                        found = True
                        break
            # armar el elemento xml para el rdf
            if found:
                locationUri = BASE_URI + 'localidad/' + formattedCountryString(locationString)
                locationElement = ET.SubElement(eventElement, 'dct:spatial', {'rdf:resource': locationUri})
    elem.clear()
    i += 1

print i
ET.ElementTree( output['event_root'] ).write( 'output/eventos.rdf', 'utf-8' )
#ET.ElementTree( output['year_root'] ).write( 'output/fechas.rdf', 'utf-8' )
with open( 'output/eventos.rdf', 'r' ) as ini, open( 'output/eventos_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
#with open( 'output/fechas.rdf', 'r' ) as ini, open( 'output/fechas_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
