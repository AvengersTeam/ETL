import xml.etree.ElementTree as ET
import lxml.etree as etree

#search for a keyword in a xml file. if we find an element that matches the keyword (eg. keyword = 'Andres Bello') 
#then it returns the uri defined in the element's tag 'rdf:about'
def getUri(self, keyword, filepath):
	for event, element in ET.iterparse( filepath, events=( 'start', 'end', 'start-ns', 'end-ns' ) ):
	    with searchInTree(tree = element, keyword = keyword) as result:
	    	if result:
	    		uri = result.find( ".//*[@tag='rdf:about']" )
	    		if uri == None or uri.text == None: raise
	    		return uri.text
	    
#returns the tree element wich contains the given keyword
def searchInTree(self, tree, keyword):
	for subtree in tree:
		if keyword in subtree.attrib.values():
			return self
	#should we be unlucky enough to get no results :c
	for subtree in tree:
		if searchInTree(tree = subtree, keyword = keyword):
			return subtree