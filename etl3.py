# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time

base_uri = 'http://datos.uchile.cl/'

# Base element for "portafolio andes bello"
output_obra_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_manifestacion_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_expresion_root = ET.Element('rdf:RDF', {'xmlns:owl': base_uri + 'ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
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
        #agregar titulo
        title = asset.find(".//*[@name='Title']")
        titleElement = ET.SubElement(obraElement, 'dc:title')
        titleElement.text = title.find('value').text
        #agregar titulo alternativo
        alternative = asset.find(".//*[@name='NAME']")
        alternativeElement = ET.SubElement(obraElement, 'dct:alternative')        
        alternativeElement.text = alternative.find('value').text
        #agregar fecha(?)
        issued = asset.find(".//*[@name='Date']")
        issuedElement = ET.SubElement(obraElement, 'dct:issued')
        if issued !=None:
            issuedElement.text = issued.find('value').text
        ET.SubElement(obraElement, 'rdf:type', {'rdf:resource': 'frbrer:C1001'})
            
        #crear instancia de expresion
        expresionElement = ET.SubElement(output_expresion_root, 'owl:Expresion', {'rdf:about': base_uri + 'recurso/expresion/'+ID})
        ET.SubElement(expresionElement, 'rdf:type', {'rdf:resource': 'frbrer:C1002'})
        
        
        
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
        ET.SubElement(manifestacionElement, 'rdf:type', {'rdf:resource': 'frbrer:C1003'})
            
output_obra_tree = ET.ElementTree(output_obra_root)
output_obra_tree.write('output/obra.rdf', 'utf-8')

output_expresion_tree = ET.ElementTree(output_expresion_root)
output_expresion_tree.write('output/expresion.rdf', 'utf-8')

output_manifestacion_tree = ET.ElementTree(output_manifestacion_root)
output_manifestacion_tree.write('output/manifestacion.rdf', 'utf-8')

with open( 'output/obra.rdf', 'r' ) as ini, open( 'output/obra_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
with open( 'output/expresion.rdf', 'r' ) as ini, open( 'output/expresion_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
with open( 'output/manifestacion.rdf', 'r' ) as ini, open( 'output/manifestacion_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
