#!/usr/bin/python3
'''utils'''
from rm.rmclasses import CODE_PHRASE 
import logging
import config
import sys
from crc_cohort.xml_parser import parse_xml
from crc_cohort.mapped_element_finder import mefinder,all_items,fill_default_items_crc,meventfinder,mtimefinder  
from crc_cohort.mapped_element_finder import complete_actual_leafs_crc,create_listofnoactualleafs_crc

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
		if(ll.get_path()==path):
			return ll
	sys.exit(f'error can\'t find {path}' )

def readinput(inputfile):
	if(config.fr==1):
		return parse_xml(inputfile)
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
		value=all_items_patient_i[f][1]
		try:
			valuestripped=re.sub(r"[\n\t\s]*", "", value)
		except TypeError as t:
			logging.info(f'typeerror {t} in position {f}')
			logging.info(f'null value inserted')
			logging.info(f'element: {all_items_patient_i[f]}')
			values.append("Null Value")
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

		if(len(flist)>0):
			logging.debug(f"SISTERACT {ll.get_path()}  {len(flist)}")

		if len(flist) >0 :
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
					#fix kras and nras mapping
					if( ( "nras" in ll.get_id() ) or ("kras" in ll.get_id() ) ):
						if(value.lower()=="not done"):
							myvalue={}
	#							myvalue['code']="at0007"
							myvalue['value']="Indeterminate"
	#							myvalue['terminology']="local"
							myvalue["code"]="[LOINC(2.65)::LA11884-6]"
							myvalue["terminology"]="LOINC"
							value=myvalue
						elif (value.lower()=="not mutated"):
							myvalue={}
	#							myvalue['code']="at0005"
							myvalue['value']="Absent"
	#							myvalue['terminology']="local"
							myvalue["code"]="[LOINC(2.65)::LA9634-2]"
							myvalue["terminology"]="LOINC"
							value=myvalue
						elif(value.lower()=="mutated"):
							myvalue={}
	#							myvalue['code']="at0004"
							myvalue['value']="Present"
	#							myvalue['terminology']="local"
							myvalue["code"]="[LOINC(2.65)::LA9633-4]"
							myvalue["terminology"]="LOINC"
							value=myvalue

					elif(ll.get_id()=='sample_id'):
						myvalue={}
						myvalue['id']=value
						value=myvalue
					elif(ll.get_id()=='morphology'):
						#high-grade neuroendocrine carcinoma,Other,Mucinous carcinoma NOT MAPPED

						#maps "Serrated adenocarcinoma" to "Adenocarcinoma, serrated type"
						if (value=='Serrated adenocarcinoma'):
							value="Adenocarcinoma, serrated type"
						#maps "Adeonsquamous carcinoma" to "Adenosquamous carcinoma"
						elif(value=='Adeonsquamous carcinoma'):
							value='Adenosquamous carcinoma'
						#maps "Large cell neuroendocrine carcinoma" to "Neuroendocrine carcinoma, large cell"	
						elif(value=='Large cell neuroendocrine carcinoma'):
							value='Neuroendocrine carcinoma, large cell'

						myvalue={}
						mylist=ll.get_acceptable_values()[0]['list']
						mylistlabels=[i["label"].lower() for i in mylist]
						if(value.lower().replace('-'," ") not in mylistlabels):
							print(f'error in morphology mapping! unmapped label={value}')
							logging.info(f'error in morphology mapping! unmapped label={value}')
							#take the first one for sake of continuity
							myvalue['value']=mylist[0]['label']
							myvalue['code']=mylist[0]['value']
							myvalue['terminology']='local'	
							value=myvalue						
						else:
							for m in mylist:
								if(m['label'].lower() == value.lower().replace('-',' ')):
									myvalue['value']=m['label']
									myvalue['code']=m['value']
									myvalue['terminology']='local'
									value=myvalue
									break


					logging.debug(f"BAR i={i} llid={ll.get_id()} value={value}")
					if(i>0):
						lltemp=ll
						tpath=ll.get_path()
						lastocc=tpath.rfind(":0")
						logging.debug(f"KK: tpath,lastocc,tpath[lastocc] {tpath} {lastocc} {tpath[lastocc]}")
						#works till i=9
						if(lastocc != -1):
							npath=tpath[0:lastocc+1]+str(i)+tpath[lastocc+2:]
							logging.debug(f"KK: tpath, {npath} ")
						lltemp.set_path(npath)
						listofActualLeafs.append(ActualLeaf(lltemp,value,f))
					else:
						listofActualLeafs.append(ActualLeaf(ll,value,f))
						nelem=nelem+1
		else:
			xelem+=1				


	print(f'{nelem} mapped leafs found')
	logging.info(f'{nelem} mapped leafs found')
	print(f'{xelem} leafs not found in input')
	logging.info(f'{xelem} leafs not found in input')
#	logging.info(f'{xelemNC} should be instantiated (according only to leafs)')


def complete_actual_leafs(listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs):
	'''add default values taken from the template or not to the compulsory fields not fillable with the input data'''
	if(config.fr==1):
		return complete_actual_leafs_crc(listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs)
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

	for ll in listofNoActualLeafs:

#now find what elements are compulsory GIVEN the actual leafs are filled
#each part of the path of an actual leaf becomes True to compulsory
				#find the actualleaf closer to the non-leaf
		if (ll.get_cardinality()[0]==0):
			xelemcard+=1
			continue
		path=ll.get_path()
		maxnumber,maxpath,maxpathorigin=findclosestPath(listofActualLeafs,path)
		logging.debug(f"path {path}")
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
				logging.warning(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")

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
					logging.warning(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")
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
		print(f'{xelemC-xelemFixable} elements not omittable')
		logging.warning(f'WARNING: Patient {patid} ')
		print(f'{xelemC} elements not present')
		print(f'{xelemFixable} elements fixable')		
		logging.warning(f'{xelemC-xelemFixable} elements not omittable')



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