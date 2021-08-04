#!/usr/bin/python3
'''find an element in the BHPatient tree and return its index or not found'''
import xml.etree.ElementTree as ET
import logging
from composition.leaf import ActualLeaf,ActualNoLeaf


def mefinder(myleaf,listofitems):
	annotation=myleaf.get_annotation()
#	if (myleaf.get_id()=='date_of_start_of_targeted_therapy'):
#		print("*********************")
#		print("--------------------")
#		print(myleaf.get_annotation())
#		print(myleaf.get_annotation()['XSD label'])
	indexes=[]
	if ('XSD label' in annotation):
		logging.debug(f"looking for {annotation['XSD label']}")
		for index,(a,b,c), in enumerate(listofitems):
			if a==annotation['XSD label']:
				indexes.append(index)
		return indexes
	return indexes

def all_items(bhtree,ns):
	return [(remove_ns(elem.tag,ns),elem.text,elem.attrib) for elem in bhtree.iter()]

def remove_ns(tag,ns):
	return tag.replace(ns,'')

def meventfinder(myleaf,listofitems):
	annotation=myleaf.get_annotation()
#	if (myleaf.get_id()=='date_of_start_of_targeted_therapy'):
#		print("*********************")
#		print("--------------------")
#		print(myleaf.get_annotation())
#		print(myleaf.get_annotation()['XSD label'])
	indexes=[]
	if ('XSD label' in annotation):
#		logging.debug(f"looking for {annotation['XSD label']}")
		for index,(a,b,c), in enumerate(listofitems):
#			logging.debug(index)
			for k in c:
				logging.debug(f'c[k] {c[k]}')
				if c[k]==annotation['XSD label']:
					indexes.append(index)
#					logging.debug(f'FOUNDDDDDDDDD {index}')
		return indexes
	return indexes


def mtimefinder(annotation,listofitems):
	time="10/12/2008"
	logging.debug(f"TIME: listofitems {listofitems}")
	logging.debug(f"TIME: {annotation}")
	if ('XSD label' in annotation):
		logging.debug(f"TIME:looking for {annotation['XSD label']}")
		for item in listofitems: #c contains attribute name and eventtype. ex {'name': '10/11/2008', 'eventtype': 'Pharmacotherapy'}
			logging.debug(f"TIME:item {item}")
			if("eventtype" in item[2]):
				if item[2]["eventtype"]==annotation['XSD label']:
					time=item[2]["name"]
					return time
	return time


def fill_default_items_crc(ll,listofActualLeafs,listofNodes,defaultLanguage,all_items_patient_i):
	from composition.utils import findclosestActual
	if(ll.get_id() == "language"):
		language={}
		language['code']=defaultLanguage
		language['terminology']="ISO_639-1"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		logging.debug(f"language {ll.get_path()} ")
		listofActualLeafs.append(ActualLeaf(ll,language,closestposition))
		return True
	elif(ll.get_id() == "encoding"):
		encoding={}
		encoding['code']="UTF-8"
		encoding['terminology']="IANA_character-sets"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,encoding,closestposition))
		return True
	elif(ll.get_id()=="composer" and ll.get_path().count('/')==2):
		composer={}
		composer['name']='Unknown'
		listofActualLeafs.append(ActualLeaf(ll,composer,0))
		return True
	elif(ll.get_id()=="territory" and ll.get_path().count('/')==2):
		territory={}
		territory['code']='EU'
		territory['terminology']="ISO_3166-1"
		listofActualLeafs.append(ActualLeaf(ll,territory,0))
		return True
	elif(ll.get_id()=="category" and ll.get_path().count('/')==2):
		category={}
		category['code']="433"
		category['value']="event"
		category['terminology']="openehr"
		logging.debug(f"CATEGORY {ll.get_path()} {category}")
		listofActualLeafs.append(ActualLeaf(ll,category,0))
		return True
	elif(ll.get_id()=="time"):
		#find one word shorter path
		path=ll.get_path()
		lastslash=path.rfind('/')
		shortpath=path[0:lastslash]
		logging.debug(f"TIME: {path} {shortpath}")
		annotation={}
		for n in listofNodes:
			if(n.get_path()==shortpath):
				annotation=n.get_annotation()
				break
		time=mtimefinder(annotation,all_items_patient_i)
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,time,closestposition))
		return True	
	elif(ll.get_id()=="setting" and ll.get_path().count('/')==3):
		setting={}
		setting['code']="238"
		setting['terminology']="openehr"
		setting['value']="other care"
		listofActualLeafs.append(ActualLeaf(ll,setting,0))
		return True
	elif(ll.get_id()=="from_event"):
		fe=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,fe,closestposition))
		return True
	elif(ll.get_id()=="primary_diagnosis"):
			primd=ll.get_acceptable_values()[0]["defaultValue"]
			listofActualLeafs.append(ActualLeaf(ll,primd,0))
			return True
	elif(ll.get_id()=="metastasis_diagnosis"):
			metd=ll.get_acceptable_values()[0]["defaultValue"]
			listofActualLeafs.append(ActualLeaf(ll,metd,0))
			return True
	elif(ll.get_id()=="test_name"):
		testname=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,testname,closestposition))
		return True
	elif(ll.get_id()=="procedure_name"):
		procedurename=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,procedurename,closestposition))
		return True			
	elif(ll.get_id()=="therapy"):
		therapy=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,therapy,closestposition))
		return True					
	elif(ll.get_id()=="problem_diagnosis_name"):
		pdn=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,pdn,closestposition))
		return True			
	elif(ll.get_id()=="variant_name"):
		vn=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,vn,closestposition))
		return True
	elif(ll.get_id()=="health_risk"):
		hr=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,hr,closestposition))
		return True
#INSTANTIATE AD HOC LEAFS
	elif(ll.get_id()=="ism_transition"):
		ll.path=ll.path+"/current_state"
		cstate={}
		cstate["value"]="completed"
		cstate["terminology"]="openehr"
		cstate["code"]="532"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,cstate,closestposition))
		return True
	elif(ll.get_path()=="/crc_cohort/context/start_time"):
			starttime="2021-05-25T15:48:35.35Z"
			listofActualLeafs.append(ActualLeaf(ll,starttime,0))
			return True
	elif(ll.get_id()=="date_of_end_of_radiation_therapy"):
		dert="P15W"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,dert,closestposition))	
		return True
	else:
		return False
