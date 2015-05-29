# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time
import pprint #for debugg print
import json
import difflib # Para comparar strings por grado de similitud
import os
from unidecode import unidecode
from datetime import datetime

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def printCountries():
    for country in sorted(countriesSet):
        print "C: " + `country`
# Busca una localidad en el nameString, entre paréntesis. Retorna -1 si no encuentra nada o si los datos son inválidos (contienen caracter ':''), de lo contrario retorna el string de la localidad
def getLocationsInParenthesis(nameString):
    start_index = nameString.find("(")
    # Verificar si nameString contiene paréntesis
    if start_index == -1: 
        return None
    else:
        # Rescatar el contenido dentro de los parentesis
        name_tail = nameString[start_index:]
        end_index = name_tail.find(")")
        if end_index != -1:
            loc = nameString[start_index+1:end_index+start_index]
            # Chequear si loc no tiene numeros
            if not hasNumbers(loc):
                # Chequear que loc no contenga caracter ':'
                if loc.find(":") != -1: return None
                loc_arr = loc.split(",")
                # Retornar la localidad encontrada, limpia
                for l in loc_arr:
                    l = l.strip()
                return loc_arr

def formattedCountryString(country_string):
    return country_string.replace(' ','_').strip().lower()

def createCountriesElements():
    for country in countriesSet:
        locID = formattedCountryString(country)
        #print("locID: " + locID)
        countryElement = ET.SubElement( output['location_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'localidad/' + locID} )


BASE_URI = 'http://datos.uchile.cl/'
log_file = open(os.path.expanduser('~') + '\ETL\logs\log_corporativo.rtf', 'w') 
pp = pprint.PrettyPrinter(indent=4)

wa = {} # Diccionario para guardar las relaciones de tipo "anterior". Ej: Uchile wa UnivChile => Uchile paso a llamarse UnivChile en cierto momento
wb = {} # Diccionario para guardar las relaciones de tipo "posterior". Ej: UnivChile wb UChile => UnivChile antes se llamaba Uchile

dic = {
    'xmlns:owl': BASE_URI + 'ontologia/',
    'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
    'xmlns:rdfs': 'http://www.w3.org/TR/rdf-schema/'
}

output = {
    'corporation_root' : ET.Element( 'rdf:RDF', dic ), #Elemento base para autoridad corporativa
    'location_root' : ET.Element( 'rdf:RDF', dic ), #Elemento base para localidades
}


countriesSet = set([])
i = 0
total = 0
# Rescatar todos los paises del mundo desde archivo Json y agregarselos al countriesSet
with open('localizations/paises.json') as data_file:    
    data = json.load(data_file)
for key in data.keys():
    countriesSet.add(unidecode(data[key]))
with open('localizations/ciudades_chile.json') as data_file:    
    data = json.load(data_file)
for d in data:
    countriesSet.add(unidecode(d))


# Recorrer todos los nodos para completar el  countriesSet (que aparecen entre parentesis en los nombres)
# Recorrer todos los nodos tambien para guardar registros wb y wa (nombres posteriores y anteriores)

for event, elem in ET.iterparse( 'input/autoridades-corporativos.xml', events=( 'start', 'end' ) ):
    
    if event != 'end' or elem.tag != 'authority': continue
    
    authority = elem

    #for child in authority._children:
        #print child.__dict__ , '\n'
        #if child.tag == 'entries':
            #for superchild in child._children:
                #if superchild.attrib['tag'] == '510':
                    #superchild.text[0:3], '\n'

    # Obtener mark 110 
    nameElement = authority.find( ".//*[@tag='110']" )
    if nameElement == None or nameElement.text == None: continue
    name = unidecode(nameElement.text)

    seeAlsoFroms = authority.findall( ".//*[@tag='510']" )
    
    # Obener campo 510
    for seeAlsoFrom in seeAlsoFroms:
        saf = unidecode(seeAlsoFrom.text)
        if saf[0:3] == '|wa':
            wa[name] = saf[3:]
            wb[saf[3:]] = name
            # print saf[3:]
        if saf[0:3] == '|wb':
            wb[name] = saf[3:]
            wa[saf[3:]] = name
            # print saf[3:]

    # Reviso si el nombre contiene una localidad entre parentesis
    '''
    locationArr = getLocationsInParenthesis(name)
    if locationArr is None: continue
    for loc in locationArr:
        if loc == -1 or loc == None or loc == "Firma": continue
        else: countriesSet.add(loc)
    '''

    

createCountriesElements()
printCountries()

for event, elem in ET.iterparse( 'input/autoridades-corporativos.xml', events=( 'start', 'end' ) ):
    
    if event != 'end' or elem.tag != 'authority': continue
    total += 1
    authority = elem

    # Obtener ID
    authIDElement = authority.find('authorityID')

    if authIDElement == None or authIDElement.text == None: 
        date = str(datetime.now())
        log_file.write('['+ date +']: '  + 'error: autoridad sin Id, iteracion ' +  `total` + '\n')
        continue

    authID = authIDElement.text

    corporationElement = ET.SubElement( output['corporation_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'corporacion/' + authID} )

    # Obtener mark 110 
    nameElement = authority.find( ".//*[@tag='110']" )
    if nameElement == None or nameElement.text == None:
        date = str(datetime.now())
        log_file.write('['+ date +']: ' + 'error: autoridad sin Tag 110, iteracion ' +  `total` + ', id = ' + authID + '\n')
        continue
    # Verificar que el nombre no contenga caracter ':' al comienzo
    if nameElement.text[0] == ':' :
        date = str(datetime.now())
        log_file.write('['+ date +']: ' + 'error: autoridad ID ' + authID + ' contiene caracter ":" al comienzo del campo 110' + '\n')
        continue
    nElement = ET.SubElement(corporationElement, 'foaf:name')
    nElement.text = nameElement.text
    nLabelElement = ET.SubElement(corporationElement, 'rdfs:label')
    nLabelElement.text = nameElement.text

    # Obtener Localidad
    name = pp.pformat(nameElement.text)
    

    found = False
   # Buscar localidad dentro del nombre (sin parentesis)
    for country in countriesSet:
        if name.find(country):
            locationString = country
            found = True
            break
   
    if not found:
        date = str(datetime.now())
        log_file.write ('['+ date +']: ' + "error: autoridad id= " + authID + ", nombre= '" + name + "' no contiene nombre de localidad en campo 110" + '\n')

    elem.clear()
    i += 1

print "Procesados " + `i` + " de " + `total`

log_file.close()
ET.ElementTree( output['corporation_root'] ).write( 'output/corporaciones.rdf', 'utf-8' )

with open( 'output/corporaciones.rdf', 'r' ) as ini, open( 'output/corporaciones_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )

# print("ratio!! " + `difflib.SequenceMatcher(None,'no information available','n0 inf0rmation available').ratio()`)

