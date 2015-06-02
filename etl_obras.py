# -*- coding: cp1252 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree
import time
#from uriFinder import multiDocumentSearch
from personSearch import makeDictionary, personDictionary
from parsers import nameParser
import sys, os

base_uri = 'http://datos.uchile.cl/recurso'

# Base element for "portafolio andes bello"
output_obra_root = ET.Element('rdf:RDF', {'xmlns:owl': 'http://datos.uchile.cl/ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_manifestacion_root = ET.Element('rdf:RDF', {'xmlns:owl': 'http://datos.uchile.cl/ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})
											
output_expresion_root = ET.Element('rdf:RDF', {'xmlns:owl': 'http://datos.uchile.cl/ontologia/',
                                            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
                                            'xmlns:dct': 'http://purl.org/dc/terms/',
                                            'xmlns:frbrer': 'http://iflastandards.info/ns/fr/frbr/frbrer#',
                                            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'})

i = 0

personDict = makeDictionary(
    filepath = 'output/personas_pretty.rdf', 
    keyTag = '{http://xmlns.com/foaf/0.1/}name', 
    attribute = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
    )

for event, elem  in ET.iterparse('input/Portfolio-Andres-bello.xml',events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
    i+=1
    #print i
    #print elem, event
    if event != 'end' or elem.tag != 'asset': continue
    #print elem.attrib
    if elem.attrib['type'] == 'FOLDER' : continue
    asset = elem    
    ID = asset.find('id').text
    #crear instancia de obra
    obraElement = ET.SubElement(output_obra_root, 'owl:NamedIndividual', {'rdf:about': base_uri + 'obra/' + ID})
    #agregar los subjects, puede haber mas de 1
    for subject in asset.iterfind(".//*[@name='Subject']"):
        for value in subject.findall('value'):
            subjectElement = ET.SubElement(obraElement, 'dc:subject')
            subjectElement.text = value.text
            #print ET.tostring(subjectElement, "utf-8").decode('utf-8')
    #agregar titulo
    #print asset._children[0].text
    title = asset.find(".//*[@name='Title']")
    titleElement = ET.SubElement(obraElement, 'dc:title')
    titleElement.text = title.find('value').text
    #agregar titulo alternativo
    alternative = asset.find(".//*[@name='NAME']")
    alternativeElement = ET.SubElement(obraElement, 'dct:alternative')        
    alternativeElement.text = alternative.find('value').text

    #adding the creator's uri
    creator = asset.find(".//*[@name='Creator']")
    uri = None
    keyword = creator.find('value').text 
    keyword = nameParser(keyword)

    #files with their respective element's tags
    filepaths = {
    'output/personas_pretty.rdf' : '{http://datos.uchile.cl/ontologia/}NamedIndividual',
    'output/corporativo_pretty.rdf': '{http://datos.uchile.cl/ontologia/}NamedIndividual'
    }
    #uri = multiDocumentSearch(keyword = keyword, filepaths = filepaths)
    uri = personDict.get(keyword)
    if uri:
        creatorElement = ET.SubElement(obraElement, 'dct:creator', {'rdf:resource' : uri})

    #agregar fecha(?)
    issued = asset.find(".//*[@name='Date']")
    issuedElement = ET.SubElement(obraElement, 'dct:issued')
    if issued !=None:
        date = issued.find('value').text
        if date[0:6]=="[entre":
            issuedElement.text = date[7:11]+" - "+date[14:18]+" rango estimado"
        else:
            if date[len(date)-1]=='?':
                issuedElement.text = date[0:2]+"00 fecha estimada"
            else:
                issuedElement.text = issued.find('value').text
    #agregar type
    ET.SubElement(obraElement, 'rdf:type', {'rdf:resource': 'frbrer:C1001'})
    #agregar link a expresion
    ET.SubElement(obraElement, 'frbrer:isRealizedThrough', {'rdf:resource': base_uri + 'expresion/'+ID})
            
    #crear instancia de expresion
    expresionElement = ET.SubElement(output_expresion_root, 'owl:NamedIndividual', {'rdf:about': base_uri + 'expresion/'+ID})
    #agregar type
    ET.SubElement(expresionElement, 'rdf:type', {'rdf:resource': 'frbrer:C1002'})
    language = asset.find(".//*[@name='Language']")
    if language != None:
        lang=language.find('value').text
        if lang == 'spa' or lang == 'Español':
            ET.SubElement(expresionElement, 'dc:language', {'rdf:resource':'http://www.lexvo.org/page/iso639-3/spa'})
        if lang == 'eng' or lang == 'Inglés':
            ET.SubElement(expresionElement, 'dc:language', {'rdf:resource':'http://www.lexvo.org/page/iso639-3/eng'})
    #agregar link a obra y manifestacion
    ET.SubElement(expresionElement,'frbrer:isRealizationOf',{'rdf:resource': base_uri + 'obra/' + ID})
    ET.SubElement(expresionElement,'frbrer:isEmbodiedln',{'rdf:resource': base_uri + 'manifestacion/'+ID})
        
    #crear instancia de Manifestacion
    manifestacionElement = ET.SubElement(output_manifestacion_root, 'owl:NamedIndividual', {'rdf:about': base_uri + 'manifestacion/'+ID})
    #agregar derechos
    right = asset.find(".//*[@name='Rights']")
    rightElement = ET.SubElement(manifestacionElement, 'dc:rights')
    rightElement.text = right.find('value').text
    #agregar publicador
    publisher = asset.find(".//*[@name='Publisher']")
    publisherElement = ET.SubElement(manifestacionElement, 'dc:publisher')
    if publisher !=None:
        publisherElement.text = publisher.find('value').text
    #agregar fuente
    source = asset.find(".//*[@name='Source']")
    sourceElement = ET.SubElement(manifestacionElement, 'dc:source')
    if source !=None:
        sourceElement.text = source.find('value').text
    #agregar type (?)
    ET.SubElement(manifestacionElement, 'rdf:type', {'rdf:resource': 'frbrer:C1003'})
    #agregar licensia, cambiar link cuando "aiga" algo
    ET.SubElement(manifestacionElement, 'dct:license', {'rdf:resource':'https://creativecommons.org/publicdomain/zero/1.0/'})
    #revisar si es rdf:resourse u otra cosa
    ET.SubElement(manifestacionElement, 'dct:identifier', {'rdf:resource':'http://bibliotecadigital.uchile.cl/client/sisib/search/detailnonmodal?d=ent%3A%2F%2FSD_ASSET%2F'+ID[:2]+'%2F'+ID+'~ASSET~0~17'})
    #agregar link a expresion
    ET.SubElement(manifestacionElement,'frbrer:isEmbodimentOf',{'rdf:resource': base_uri + 'expresion/'+ID})


print 'fin'   
output_obra_tree = ET.ElementTree(output_obra_root)
output_obra_tree.write('output/obra.rdf', 'utf-8')

output_expresion_tree = ET.ElementTree(output_expresion_root)
output_expresion_tree.write('output/expresion.rdf', 'utf-8')

output_manifestacion_tree = ET.ElementTree(output_manifestacion_root)
output_manifestacion_tree.write('output/manifestacion.rdf', 'utf-8')

with open( 'output/obra.rdf', 'r' ) as ini, open( 'output/obra_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
with open( 'output/expresion.rdf', 'r' ) as ini, open( 'output/expresion_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
with open( 'output/manifestacion.rdf', 'r' ) as ini, open( 'output/manifestacion_pretty.rdf', 'w' ) as out: out.write( etree.tostring( etree.XML( ini.read() ), pretty_print = True, encoding='utf-8' ) )
