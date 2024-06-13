#!/usr/bin/python3
'''utils'''
from rm.rmclasses import CODE_PHRASE 
import logging
import config
import sys
from crc_cohort.xml_parser import parse_xml,remove_empty_events
from crc_cohort.mapped_element_finder import mefinder,all_items,meventfinder,mtimefinder
#from crc_cohort.mapped_element_finder import fill_default_items_crc  
from crc_cohort.mapped_element_finder import complete_actual_leafs_crc,create_listofnoactualleafs_crc
from crc_cohort.mapped_element_finder import fix_leaf_with_missing_fields_crc
import copy
from pathlib import Path
import re
from composition.leaf import ActualLeaf,ActualNoLeaf

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


def findExactPath(listofleafs,path):
	'''find path closest to the one given from the list of all Leafs'''
	for ll in listofleafs:
		logging.debug(f'findexactpath path={path} ll.getpath={ll.get_path()}')
		if(ll.get_path()==path):
			return ll
	sys.exit(f'error can\'t find {path}' )

def readinput(inputfile):
	if(config.fr==1):
		lop=parse_xml(inputfile)
		for l in lop:
			remove_empty_events(l)
		return lop
#		return parse_xml(inputfile)
	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)
#		return all_pheno_items(patienti)

def retrieve_all_items_patient(patienti,ns):
	if(config.fr==1):
		return all_items(patienti,ns)
	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)
#		return parse_pheno(inputfile)	

def element_finder(ll,all_items_patient_i):
	if(config.fr==1):
		return mefinder(ll,all_items_patient_i)	
	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)
#		return mepheno(ll,all_items_patient_i)			

def get_value(all_items_patient_i,f):
	if(config.fr==1):
		values=[]
		logging.debug(f"BARA {all_items_patient_i[f]}")
		if all_items_patient_i[f][0]=='Location':
			logging.debug('this way')
			value=all_items_patient_i[f][2]['name']
			logging.debug(f'value={value}')
			valuestripped=value
		else:
			logging.debug('that way')
			value=all_items_patient_i[f][1]
			logging.debug(f'value={value}')
			try:
				valuestripped=re.sub(r"[\n\t\s]*", "", value)
			except TypeError as t:
				logging.info(f'typeerror {t} in position {f}')
				logging.info(f'null value inserted')
				logging.info(f'element: {all_items_patient_i[f]}')
				values.append("NULLFLAVOURnodata")
				return values
		if(valuestripped==""):
			#look for values
			somevalue=True
			g=f+1
			value=""
			while(somevalue):
				if(g<len(all_items_patient_i)):
					if(all_items_patient_i[g][0].rstrip(" ")=="Value"):
						value=all_items_patient_i[g][1]
						values.append(value)
					else:
						somevalue=False
				else:
					somevalue=False		
				g=g+1
		else:
			values.append(value)
		return values
	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)


def create_actual_leafs(listofleafs,all_items_patient_i,listofActualLeafs,listofNodes,defaultLanguage):
	nelem=0
	xelem=0
	flist=[]
	for (indexleaf,ll) in enumerate(listofleafs):
		logging.debug(f'leaf ids: {ll.get_id()}')
		flist=element_finder(ll,all_items_patient_i)
#			flist=mefinder(ll,all_items_bh)

		if len(flist) >0 :
			logging.debug(f"SISTERACT {ll.get_path()}  {len(flist)}")
			for f in flist:
				logging.debug("********************************************")
				logging.debug(f'index in bh items {f}, element {all_items_patient_i[f]}')
				logging.debug(f'GJH {ll.get_path()} {all_items_patient_i[f]} {all_items_patient_i[f][1]}')
				if (f+1<len(all_items_patient_i)):
					logging.debug(f'GJH {ll.get_path()} {all_items_patient_i[f+1]} {all_items_patient_i[f+1][1]}')

				#if all_items_bh[f][1] not empty then that's the value
				values=get_value(all_items_patient_i,f)
				logging.debug(f'VALUES values={values} len(values)={len(values)}')
				for i,value in enumerate(values):
					valuebool=False
					if(value==''):
						valuebool=True
					logging.debug(f"BAR i={i} llid={ll.get_id()} value={value}")
					if(i>0):#values after first one
						lltemp=copy.deepcopy(ll)
						tpath=lltemp.get_path()
						lastocc=tpath.rfind(":0")
						logging.debug(f"KK: tpath,lastocc,tpath[lastocc] {tpath} {lastocc} {tpath[lastocc]}")
						#works till i=9
						if(lastocc != -1):
							npath=tpath[0:lastocc+1]+str(i)+tpath[lastocc+2:]
							logging.debug(f"KK: tpath, {npath} ")
						lltemp.set_path(npath)
						listofActualLeafs.append(ActualLeaf(lltemp,value,f,valuebool))
					else:
						listofActualLeafs.append(ActualLeaf(ll,value,f,valuebool))
						nelem=nelem+1
		else:
			xelem+=1				


	print(f'{nelem} mapped leafs found')
	logging.info(f'{nelem} mapped leafs found')
	print(f'{xelem} leafs not found in input')
	logging.info(f'{xelem} leafs not found in input')
#	logging.info(f'{xelemNC} should be instantiated (according only to leafs)')


def complete_actual_leafs(templateId,listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs,mapping_ids):
	'''add default values taken from the template or not to the compulsory fields not fillable with the input data'''
	if(config.fr==1):
		complete_actual_leafs_crc(templateId,listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs,mapping_ids)
		fix_leaf_with_missing_fields_crc(templateId,listofActualLeafs)

	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)		

def create_listofnoactualleafs(listofActualLeafs,listofleafs):
	'''add default values taken from the template or not to the compulsory fields not fillable with the input data'''
	if(config.fr==1):
		return create_listofnoactualleafs_crc(listofActualLeafs,listofleafs)
	elif(config.fr==2):
		print("Not yet implemented")
		exit(0)		



def check_missing_leafs(patid,listofleafs,listofActualLeafs,listofNodes):

	listofNoActualLeafs=create_listofnoactualleafs(listofActualLeafs,listofleafs)
	xelemC=0
	xelemFixable=0
	xelemcard=0
	lni=[]

	for ll in listofNoActualLeafs:

#now find what elements are compulsory GIVEN the actual leafs are filled
#each part of the path of an actual leaf becomes True to compulsory
				#find the actualleaf closer to the non-leaf
		if (ll.get_cardinality()[0]==0):
			xelemcard+=1
			continue
		path=ll.get_path()
		logging.debug(f"calling findclosestPath with path {path}")
		maxnumber,maxpath,maxpathorigin=findclosestPath(listofActualLeafs,path)
		logging.debug(f'maxnumber={maxnumber} maxpath={maxpath} maxpathorigin={maxpathorigin}')		
		#now we print the ones we should have had but we hadn't
		#calculate how many words between slashes we have since maxpath to get to path
		slashes=path.count('/')-maxpath.count("/")
		logging.debug(f"slashes={slashes}")
		totalslashes=path.count('/')
		if(slashes==0):
			xelemC+=1
			if(ll.get_id()=="subject"):
				xelemFixable+=1
			else:
				lni.append(ll)
				#logging.warning(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")

		else:
			st=maxnumber+1
			npath=[]
			for i in range(slashes):
				indexslash=path.find('/',st)
				logging.debug(f"{indexslash} indexslash")
				logging.debug(len(path))
				logging.debug(i)
				npath.append(path[:indexslash])
				logging.debug(f"npath {npath}")
				st=indexslash+1
			ncomp=True
			for n in npath:
				for node in listofNodes:
					if(node.get_path()==n):
						logging.debug(f"{node.get_path()} {n} {node.get_cardinality()[0]}")
						if(node.get_cardinality()[0]==0):
							ncomp=False
							break
			if(ncomp):
				xelemC+=1
#					if(ll.get_id()=="subject" or ll.get_id()=="ism_transition"):
				if(ll.get_id()=="subject"):
					xelemFixable+=1
				else:
					lni.append(ll)
					#logging.warning(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")
			else:
				xelemcard+=1
	print(f'{xelemcard} elements not compulsory (zero cardinality)')
	logging.info(f'{xelemcard} elements not compulsory (zero cardinality)')				
	print(f'{xelemFixable}/{xelemC} can be reasonably omitted')
	logging.info(f'{xelemFixable}/{xelemC} can be reasonably omitted')
	if(xelemFixable<xelemC):
		print(f'WARNING: Patient {patid} ')
		print(f'{xelemC} elements not present')
		print(f'{xelemFixable} elements fixable')
		print(f'{xelemC-xelemFixable} elements not omittable:')
		
		logging.warning(f'WARNING: Patient {patid} ')
		logging.warning(f'{xelemC} elements not present')
		logging.warning(f'{xelemFixable} elements fixable')		
		logging.warning(f'{xelemC-xelemFixable} elements not omittable:')

		for lnie in lni:
			print(f'id={lnie.get_id()} path={lnie.get_path()}')
			logging.warning(f'id={lnie.get_id()} path={lnie.get_path()}')



def create_actual_noleafs(listofnoleafs,all_items_patient_i,listofActualNoleafs):
	nnelem=0
	nxelem=0
	noflist=[]
	for (indexnoleaf,ll) in enumerate(listofnoleafs):
		logging.debug("********************************************")
		logging.debug(f'noleaf ids: id={ll.get_id()} path={ll.get_path()}')
		noflist=meventfinder(ll,all_items_patient_i)
		if len(noflist) > 0:
			for f in noflist:
				logging.debug(f'Added index in bh items {f}, element={all_items_patient_i[f]}')
				listofActualNoleafs.append(ActualNoLeaf(ll,f))
				nnelem=nnelem+1
		else:
				nxelem=nxelem+1	




	logging.info(f'{nnelem} mapped noleafs')
	logging.info(f'{nxelem} noleafs not found')

def read_blacklist(patients_blacklist_file):
	bl_file = Path(patients_blacklist_file)
	blacklist=[]
	if bl_file.exists():
		with open(bl_file, 'r') as f:
			for line in f:
				if line.startswith('#'):
					continue
				else:
					blacklist.extend(line.strip().split(','))
	return blacklist

def read_mapping_ids(mapping_ids_file):
	mapping_ids={}
	with open(mapping_ids_file,'r') as f:	
		for line in f:
			kv=line.strip().split(',')
			if kv[0].isnumeric():
				mapping_ids[kv[0]]=kv[1]
	return mapping_ids