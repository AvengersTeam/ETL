# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

base_uri = 'http://datos.uchile.cl/'

# Base element for "portafolio andes bello"
output_obra_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_manifestacion_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',                                            
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_expresion_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

birthYearDict = {}
deathYearDict = {}

i = 0

input_tree = ET.parse('input/Portfolio-Andres-bello.xml')
input_root = input_tree.getroot()

for asset in input_root.iterfind("asset"):
    i+=1
    if i>1:     
        ID = asset.find('id').text
        print ID
        #crear instancia de obra
        obraElement = ET.SubElement(output_obra_root, 'owl:Obra', {'rdf:about': base_uri + 'recurso/obra/' + ID})
        #agregar los subjects, puede haber mas de 1
        for subject in asset.iterfind(".//*[@name='Subject']"):
            for value in subject.findall('value'):
                subjectElement = ET.SubElement(obraElement, 'dc:subject')
                subjectElement.text = value.text
                #print ET.tostring(subjectElement, "utf-8").decode('utf-8')
        #agregar titulo alternativo
        alternativeElement = ET.SubElement(obraElement, 'dct:alternative')
        #agregar fecha(?)
        issuedElement = ET.SubElement(obraElement, 'dct:issued')
        
        #crear instancia de expresion
        expresionElement = ET.SubElement(output_expresion_root, 'owl:Expresion', {'rdf:about': base_uri + 'recurso/expresion/'+ID})
        
        
        #crear instancia de Manifestacion
        manifestacionElement = ET.SubElement(output_manifestacion_root, 'owl:Manifestacion', {'rdf:about': base_uri + 'recurso/manifestacion/'+ID})
        right = asset.find(".//*[@name='Rights']")
        rightElement = ET.SubElement(manifestacionElement, 'dc:rights')
        rightElement.text = right.find('value').text
        publisher = asset.find(".//*[@name='Publisher']")
        publisherElement = ET.SubElement(manifestacionElement, 'dc:publisher')
        if publisher !=None:
            publisherElement.text = publisher.find('value').text
        source = asset.find(".//*[@name='Source']")
        sourceElement = ET.SubElement(manifestacionElement, 'dc:source')
        if source !=None:
            sourceElement.text = source.find('value').text
            
output_obra_tree = ET.ElementTree(output_obra_root)
output_obra_tree.write('output/obra.rdf', 'utf-8')

output_manifestacion_tree = ET.ElementTree(output_manifestacion_root)
output_manifestacion_tree.write('output/manifestacion.rdf', 'utf-8')
#output_year_tree = ET.ElementTree(output_year_root)
#output_year_tree.write('output/fechas.rdf', 'utf-8')
