# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import lxml.etree as etree

#search for a keyword in a xml file. if we find an element that matches the keyword (eg. keyword = 'Andres Bello') 
#then it returns the uri defined in the element's tag 'rdf:about'
def getAttribute(keyword, filepath, tag, attribute):
	for event, tree in ET.iterparse( filepath, events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
		if event != 'start' or tree.tag != tag: continue
		for child in tree:
			if child.text == keyword:
				return tree.attrib[attribute]
	return None

def getUri(keyword, filepath, tag):
	return getAttribute(
		keyword = keyword, 
		filepath = filepath, 
		tag = tag, 
		attribute = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
		)

#does a getUri search over several documents and returns the first match
def multiDocumentSearch(keyword, filepaths):
	for filepath, tag in filepaths.iteritems():
		result = getUri(keyword = keyword, filepath = filepath, tag = tag)
		if result:
			return result
	return None