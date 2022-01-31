#!/usr/bin/python3
'''find occurrences tree from a given list of noleafs'''
import logging

def FindOccurencesFromNoLeafs(listofnoleafs):
	'''return occurrence number for each leaf associated with its position on the xml and the XSD label'''
#	print(listofnoleafs)
	if len(listofnoleafs)<1:
		logging.debug(f'LLLL list of noleafs null')
		return [[]]
	elif len(listofnoleafs)==1:
		#0 name,1 pathlen,2 number, 3 position,4 label,5 path
		#return 2,3,4,5
		name=listofnoleafs[0].get_name()
		path=listofnoleafs[0].get_path()
		pathlen=len(path)
		number=0
		position=listofnoleafs[0].get_positioninXML()
		label=listofnoleafs[0].get_id()
		logging.debug(f'LLLL list of noleafs with one element')
		return [[number,position,label,path]]
	else:
		listofnamepath=[]
		prevname=listofnoleafs[0].get_name()
		prevpath=listofnoleafs[0].get_path()
		prevpathlen=len(prevpath)
		position=listofnoleafs[0].get_positioninXML()
		prevnumber=0
#		prevlabel=listofnoleafs[0].get_annotation()['XSD label']
		prevlabel=listofnoleafs[0].get_id()
#		print("AAA")
		listofnamepath.append([prevname,prevpathlen,prevnumber,position,prevlabel,prevpath])
		logging.debug(f'listofnamepath {prevname},{prevpathlen},{prevnumber},{position},{prevlabel},{prevpath}')

		for l in listofnoleafs[1:]:
#			print(l)
			name=l.get_name()
			path=l.get_path()
			position=l.get_positioninXML()
			pathlen=len(path)
			logging.debug(f'WQ path={path} prevpath={prevpath}')
			number=get_number(name,prevname,pathlen,prevpathlen,prevnumber,listofnamepath)
			#label=l.get_annotation()['XSD label']
			label=l.get_id()
			listofnamepath.append([name,pathlen,number,position,label,path])
			logging.debug(f'listofnamepath {name},{pathlen},{number},{position},{label},{path}')
			prevname=name
			prevpath=path
			prevpathlen=pathlen
			prevnumber=number
			prevlabel=label
		listofnamepath.sort(key = lambda x: x[3])

		logging.debug(f'LLLL len list occurrences {len(listofnamepath)}')

		return [[i[2],i[3],i[4],i[5]] for i in listofnamepath]


def get_number(name,prevname,pathlen,prevpathlen,prevnumber,listofnamepath):
	if (name==prevname):
		return prevnumber+1
	else:
		logging.debug(f'WW name={name} prevname={prevname} pathlen={pathlen} prevpathlen={prevpathlen} prevnumber={prevnumber}')
		if(pathlen>prevpathlen):
			#I'm moving right
			return 0
		elif(pathlen==prevpathlen):
			for i in reversed(listofnamepath):
				logging.debug(f'i[0]={i[0]} i[1]={i[1]}')
				if (i[1]<pathlen):
					#I'm moving left to find the previous one
					return 0
				elif(i[0]==name):
					return i[2]+1
			return 0 #same pathlen but different path
			#logging.debug(f"I shouldn't be here {name} {prevname}")
		else:
			for i in reversed(listofnamepath):
				if(i[1]==pathlen and i[0]==name):
					return i[2]+1
			return 0

