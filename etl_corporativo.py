# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time
import pprint #for debugg print

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def printCountries():
    for country in countriesSet:
        print "C: " + `country`
# Busca una localidad en el nameString, entre paréntesis. Retorna -1 si no encuentra nada o si los datos son inválidos (contienen caracter ':''), de lo contrario retorna el string de la localidad
def getLocationInParenthesis(nameString):
    start_index = name.find("(")
    # Verificar si nameString contiene paréntesis
    if start_index == -1: 
        return -1
    else:
        # Rescatar el contenido dentro de los parentesis
        name_tail = name[start_index:]
        end_index = name_tail.find(")")
        if end_index != -1:
            loc = name[start_index+1:end_index+start_index]
            # Chequear si loc no tiene numeros
            if not hasNumbers(loc):
                # Chequear que loc no contenga caracter ':'
                if loc.find(":") != -1: return -1
                loc_arr = loc.split(",")
                # Retornar la localidad encontrada, limpia
                return loc_arr[len(loc_arr) - 1].strip()

def createCountriesElements():
    for country in countriesSet:
        locID = country.lower().replace(' ','_').strip()
        print("locID: " + locID)
        countryElement = ET.SubElement( output['location_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'localidad/' + locID} )

BASE_URI = 'http://datos.uchile.cl/'
log_file = open('logs/log_corporativo.rtf', 'w')

dic = {
    'xmlns:owl': BASE_URI + 'ontologia/',
    'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xmlns:foaf': 'http://xmlns.com/foaf/0.1/',
    'xmlns:rdfs': 'http://www.w3.org/TR/rdf-schema/'
}

output = {
    'corporation_root' : ET.Element( 'rdf:RDF', dic ), #Base element for authorities
    'location_root' : ET.Element( 'rdf:RDF', dic ), #Base element for locations
}

pp = pprint.PrettyPrinter(indent=4)

countriesSet = set([])
i = 0
total = 0

# Recorrer todos los nodos para llenar arreglo de paises (que aparecen entre parentesis en los nombres)
# Recorrerlos tambien para guardar registros wb y wa (nombres posteriores y anteriores)
for event, elem in ET.iterparse( 'input/autoridades-corporativos.xml', events=( 'start', 'end' ) ):
    if event != 'end' or elem.tag != 'authority': continue
    # Obtener mark 110 
    authority = elem
    nameElement = authority.find( ".//*[@tag='110']" )
    if nameElement == None or nameElement.text == None: continue
    # Reviso si el nombre contiene una localidad entre parentesis
    name = pp.pformat(nameElement.text)
    locationString = getLocationInParenthesis(name)
    if locationString == -1 or locationString == None or locationString == "Firma": continue
    else: countriesSet.add(locationString)
    # Obtener campos 510
    seeAlsoFroms = authority.findall( "./entries//*[@tag='510']" )
    for seeAlsoFrom in seeAlsoFroms:
        #prevName = pp.pformat(seeAlsoFrom.text)
        print seeAlsoFrom.text
        #if prevName.find('wa') != -1:
        #    print "seeAlso de " + name + " = " + prevName

createCountriesElements()

printCountries()
for event, elem in ET.iterparse( 'input/autoridades-corporativos.xml', events=( 'start', 'end' ) ):
    
    if event != 'end' or elem.tag != 'authority': continue
    total += 1
    authority = elem

    # Obtener ID
    authIDElement = authority.find('authorityID')

    if authIDElement == None or authIDElement.text == None: 
        print('error: autoridad sin Id, iteracion ' +  `total`)
        continue

    authID = authIDElement.text
    corporationElement = ET.SubElement( output['corporation_root'], 'owl:NamedIndividual', {'rdf:about': BASE_URI + 'corporacion/' + authID} )

    # Obtener mark 110 
    nameElement = authority.find( ".//*[@tag='110']" )
    if nameElement == None or nameElement.text == None:
        print('error: autoridad sin Tag 110, iteracion ' +  `total` + ', id = ' + authID)
        continue
    # Verificar que el nombre no contenga caracter ':'
    if nameElement.text.find(":") != -1 :
        print('error: autoridad ID ' + authID + ' contiene caracter ":" en campo 110')
        continue
    nElement = ET.SubElement(corporationElement, 'foaf:name')
    nElement.text = nameElement.text
    nLabelElement = ET.SubElement(corporationElement, 'rdfs:label')
    nLabelElement.text = nameElement.text

    # Obtener Localidad
    name = pp.pformat(nameElement.text)
    locationString = getLocationInParenthesis(name)

    if locationString == None or locationString == -1:
        found = False
        # Buscar localidad dentro del nombre (sin parentesis)
        for country in countriesSet:
            if name.find(country):
                locationString = country
                found = True
                break
    if not found: 
        print ("no esta la localidad en el arreglo de paises") #Arreglar este riesgo utilizando arreglo de todos los paises del mundo
    


    elem.clear()
    i += 1
print "Procesados " + `i` + " de " + `total`

log_file.close()
ET.ElementTree( output['corporation_root'] ).write( 'output/corporaciones.rdf', 'utf-8' )

with open( 'output/corporaciones.rdf', 'r' ) as ini, open( 'output/corporaciones_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )