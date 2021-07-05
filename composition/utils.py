#!/usr/bin/python3
'''utils'''
from rm.rmclasses import CODE_PHRASE 
import logging

def findclosestActual(listofActualLeafs,path):
	'''returns the position in the xml of the Actual Leaf whose path is closest to the given one'''
	maxnumber=1
	maxpath="/"
	maxpathorigin=""
	maxpositioninXML=0
	for al in listofActualLeafs:
		alpath=al.get_path()
		for ip in range(1,len(alpath)):
			if((alpath[0:ip] in path) and ip>maxnumber and alpath[ip-1:ip]=='/'):
				maxnumber=ip 
				maxpath=alpath[0:ip]
				maxpathorigin=alpath
				maxpositioninXML=al.get_positioninXML()
	logging.debug(f"language path {path} maxpathorigin {maxpathorigin} {maxpositioninXML}")
	return maxpositioninXML



def findclosestPath(listofActualLeafs,path):
	'''find path closest to the one given from a list of Actual Leafs'''
	maxnumber=1
	maxpath="/"
	maxpathorigin=""
	for al in listofActualLeafs:
		alpath=al.get_path()
		for ip in range(1,len(alpath)):
			if((alpath[0:ip] in path) and ip>maxnumber and alpath[ip-1:ip]=='/'):
				maxnumber=ip 
				maxpath=alpath[0:ip]
				maxpathorigin=alpath
	return maxnumber,maxpath,maxpathorigin