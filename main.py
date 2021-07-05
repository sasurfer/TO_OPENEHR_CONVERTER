#!/usr/bin/python3
'''convert given format to_openehr compositions'''
import json
import logging
from webtemplate.webtemplate_reader import read_wt
from webtemplate.webtemplate_parser import parse_wt
from crc_cohort.xml_parser import parse_xml,find_ns
from crc_cohort.mapped_element_finder import mefinder,all_items,meventfinder,mtimefinder
from composition.leaf import ActualLeaf,ActualNoLeaf
from composition.occurrences import FindOccurencesFromNoLeafs
from composition.composition import Composition
from composition.utils import findclosestActual,findclosestPath
import argparse
import re


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='WARNING')
	parser.add_argument('--convertfrom',help='which format we convert from',default='bbmrixml',metavar=['bbmrixml','phenopacketV2'])
	parser.add_argument('--inputfile',help='input filename',default='input')
	parser.add_argument('--webtemplate',help='template target in simple template format',default='webtemplate')
#    parser.add_argument('--pathfile',help='file with the paths to the phenopackets',type=str)
#    parser.add_argument('--check',action='store_true', help='4 debugging: check the composition obtained against a target')

	parser.add_argument('--outputfilebasename',help='output file basename',default='output')
	args=parser.parse_args()

	loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
	if not isinstance(loglevel, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	logging.basicConfig(filename='./conversion.log',filemode='w',level=loglevel)

	
	inputfile=args.inputfile
	webtemplate=args.webtemplate
	outputfilebasename=args.outputfilebasename

	if(args.convertfrom != "bbmrixml" and args.convertfrom !="phenopacketV2"):
		print(f"Error: 'convertfrom' parameter must be chosen from the parameter values range")
		exit(1)


	# read and parse webtemplate
	#webtemplate="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/TMP/WebTemplatecrc_cohort_dazipMOD.json"
	#webtemplate="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CRC_COHORT/crc_cohort_v2.json"
	myjson,defaultLanguage=read_wt(webtemplate)
	logging.info(json.dumps(myjson, indent = 4, sort_keys=True))

	#create leafs, noleafs(4 molteplicity) and nodes
	listofleafs,listofnoleafsannotated,listofNodes=parse_wt(myjson)

	logging.debug("Leafs")
	logging.debug(f"number of leafs={len(listofleafs)}")
	for ll in listofleafs:
		logging.debug(f"leaf {ll.get_all()}")

	logging.debug("********************************************")
	logging.debug("No leafs annotated")
	logging.debug(f"number of no leaf annotated={len(listofnoleafsannotated)}")
	for nl in listofnoleafsannotated:
		logging.debug(f"no leaf annotated {nl.get_id()} {nl.get_annotation()}{nl.get_path()}")
	logging.debug("********************************************")	

	logging.debug("NOODES")
	for n in listofNodes:
		logging.debug(f"path {n.get_path()} maxcardinality {n.get_cardinality()[1]}")	

	# choose conversion 
	# 1- crc xml
	# 2- phenopacket
	#


	# read and parse XML
	#inputfile="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/TMP/import_exampleMOD.xml"
	listofbhpatients=parse_xml(inputfile)
	ns=find_ns(listofbhpatients[0])

	for i in range(1):
		bhp=listofbhpatients[i]
		outputfile=outputfilebasename+"_"+str(i)+".json"
#	for bhp in listofbhpatients:
		#create mapping for each leaf annotated
		#create list with all the items
		all_items_bh=(all_items(bhp,ns))
		logging.debug(f'all items for patient {i}')
		logging.debug(all_items_bh)
		logging.debug("********************************************")

# create an ActualLeaf for each Leaf whose mapping is instanciated in xml
# plus fill all the language and encoding if necessary
		nelem=0
		xelem=0
		xelemNC=0
		flist=[]
		listofActualLeafs=[]
		listofNoActualLeafs=[]
		for (indexleaf,ll) in enumerate(listofleafs):


			logging.debug(f'leaf ids: {ll.get_id()}')
			flist=mefinder(ll,all_items_bh)
			if len(flist) >0 :
				for f in flist:
					logging.debug("********************************************")
					logging.debug('index in bh items {f}, {element all_items_bh[f]}')
					logging.debug(f'GJH {ll.get_path()} {all_items_bh[f]} {all_items_bh[f][1]}')
					if (f+1<len(all_items_bh)):
						logging.debug(f'GJH {ll.get_path()} {all_items_bh[f+1]} {all_items_bh[f+1][1]}')

					#if all_items_bh[f][1] not empty then that's the value
					value=all_items_bh[f][1]
					valuestripped=re.sub(r"[\n\t\s]*", "", value)
					if(valuestripped==""):
						#look for values
						somevalue=True
						g=f+1
						value=""
						while(somevalue):
							if(g<len(all_items_bh)):
								if(all_items_bh[g][0].rstrip(" ")=="Value"):
									if(value==""):
										value=all_items_bh[g][1]
									else:
										value=value+","+all_items_bh[g][1]
								else:
									somevalue=False
							else:
								somevalue=False		
							g=g+1

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
					listofActualLeafs.append(ActualLeaf(ll,value,f))
					nelem=nelem+1
			else:
				#if language,territory,composer,category or encoding fill it with default values
				#subject and ism_transition are ignored unless mapped
				# if(1==0):
				# 	pass
				if(ll.get_id() == "language"):
					nelem=nelem+1
					language={}
					language['code']=defaultLanguage
					language['terminology']="ISO_639-1"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					logging.debug(f"language {ll.get_path()} ")
					listofActualLeafs.append(ActualLeaf(ll,language,closestposition))
				elif(ll.get_id() == "encoding"):
					nelem=nelem+1
					encoding={}
					encoding['code']="UTF-8"
					encoding['terminology']="IANA_character-sets"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,encoding,closestposition))
				elif(ll.get_id()=="composer" and ll.get_path().count('/')==2):
					nelem=nelem+1
					composer={}
					composer['name']='Unknown'
					listofActualLeafs.append(ActualLeaf(ll,composer,0))
				elif(ll.get_id()=="terrritory" and ll.get_path().count('/')==2):
					nelem=nelem+1
					territory={}
					territory['code']='DE'
					territory['terminology']="ISO_3166-1"
					listofActualLeafs.append(ActualLeaf(ll,territory,0))
				elif(ll.get_id()=="category" and ll.get_path().count('/')==2):
					nelem=nelem+1
					category={}
					category['code']="433"
					category['value']="event"
					category['terminology']="openehr"
					logging.debug(f"CATEGORY {ll.get_path()} {category}")
					listofActualLeafs.append(ActualLeaf(ll,category,0))
				elif(ll.get_id()=="territory" and ll.get_path().count('/')==2):
					nelem=nelem+1
					territory={}
					territory['code']="DE"
					territory['terminology']="ISO_3166-1"
					listofActualLeafs.append(ActualLeaf(ll,territory,0))
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
					time=mtimefinder(annotation,all_items_bh)
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,time,closestposition))	
				elif(ll.get_id()=="setting" and ll.get_path().count('/')==3):
					setting={}
					setting['code']="238"
					setting['terminology']="openehr"
					setting['value']="other care"
					listofActualLeafs.append(ActualLeaf(ll,setting,0))
#INSTANTIATE AD HOC LEAFS
				elif(ll.get_id()=="ism_transition"):
					ll.path=ll.path+"/current_state"
					cstate={}
					cstate["value"]="completed"
					cstate["terminology"]="openehr"
					cstate["code"]="532"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,cstate,closestposition))
				elif(ll.get_path()=="/crc_cohort/context/start_time"):
 					starttime="2021-05-25T15:48:35.35Z"
 					listofActualLeafs.append(ActualLeaf(ll,starttime,0))
				elif(ll.get_path()=="/crc_cohort/patient_data/primary_diagnosis/primary_diagnosis"):
 					primd="primary diagnosis"
 					listofActualLeafs.append(ActualLeaf(ll,primd,0))
				elif(ll.get_path()=="/crc_cohort/patient_data/metastasis_diagnosis/metastasis_diagnosis"):
 					metd="metastasis_diagnosis"
 					listofActualLeafs.append(ActualLeaf(ll,metd,0))
				elif(ll.get_id()=="test_name"):
					testname="test_name"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,testname,closestposition))
				elif(ll.get_id()=="procedure_name"):
					path=ll.get_path()
					logging.debug(f"path {path}")
					procedure2=path.rfind('/')
					logging.debug(f"proc2 {procedure2}")	
					procedure1=path.rfind('/',0,procedure2)
					logging.debug(f"proc1 {procedure1}")	
					procedurename=path[procedure1+1:procedure2]
#					procedurename="procedure_name"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,procedurename,closestposition))			
				elif(ll.get_id()=="therapy"):
					therapy="therapy"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,therapy,closestposition))					
				elif(ll.get_path()=="/crc_cohort/histopathology/result_group/cancer_diagnosis/problem_diagnosis_name"):
 					pdn="problem diagnosis name"
 					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
 					listofActualLeafs.append(ActualLeaf(ll,pdn,closestposition))			
				elif(ll.get_id()=="date_of_end_of_radiation_therapy"):
					dert="P15W"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,dert,closestposition))	
				elif(ll.get_id()=="variant_name"):
					vn="variant name"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,vn,closestposition))
				elif(ll.get_id()=="health_risk"):
					hr="HNPCC"
					closestposition=findclosestActual(listofActualLeafs,ll.get_path())
					listofActualLeafs.append(ActualLeaf(ll,hr,closestposition))
				else:
					listofNoActualLeafs.append(ll)
					#print(f'CARD {ll.get_cardinality()}')
					#print(f'CARD[0] {ll.get_cardinality()[0]} {type(ll.get_cardinality()[0])}')
					if(ll.is_compulsory()):
						xelemNC+=1
						print(f"NC:LEAF {ll.get_id()} not instantiated {ll.get_path()} but min,max {ll.get_cardinality()}")
						logging.debug(f"NC:LEAF {ll.get_id()} not instantiated {ll.get_path()} but min,max {ll.get_cardinality()}")
#					print (ll.get_path(), 'Not found')
					xelem=xelem+1

		xelemC=0
		xelemFixable=0
		for ll in listofNoActualLeafs:

#now find what elements are compulsory GIVEN the actual leafs are filled
#each part of the path of an actual leaf becomes True to compulsory
					#find the actualleaf closer to the non-leaf
			if (ll.get_cardinality()[0]==0):
				continue
			path=ll.get_path()
			maxnumber,maxpath,maxpathorigin=findclosestPath(listofActualLeafs,path)
			# maxnumber=1
			# maxpath="/"
			# maxpathorigin=""
			# for al in listofActualLeafs:
			# 	alpath=al.get_path()
			# 	for ip in range(1,len(alpath)):
			# 		if((alpath[0:ip] in path) and ip>maxnumber and alpath[ip-1:ip]=='/'):
			# 			maxnumber=ip 
			# 			maxpath=alpath[0:ip]
			# 			maxpathorigin=alpath
			logging.debug(f"path {path}")
			logging.debug(f'maxnumber={maxnumber} maxpath={maxpath} maxpathorigin={maxpathorigin}')
			#now we print the ones we should have had but we hadn't
			#calculate how many words between slashes we have since maxpath to get to path
			slashes=path.count('/')-maxpath.count("/")
			# slashes=0
			# found=0
			# st=maxnumber+1
			# while (found != -1):
			# 	found=path.find('/',st)
			# 	if (found != -1):
			# 		st=found+1
			# 		slashes+-1
			logging.debug(f"slashes={slashes}")
			totalslashes=path.count('/')
			if(slashes==0):
				xelemC+=1
#						logging.debug(f"CHECK:LEAF {ll.get_id()} not instantiated {ll.get_path()} min,max {ll.get_cardinality()}")
				if(ll.get_id()=="subject" or ll.get_id()=="ism_transition"):
					xelemFixable+=1
				else:
					logging.debug(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")

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
#						logging.debug(f"CHECK(ncomp):LEAF {ll.get_id()} not instantiated {ll.get_path()}  min,max {ll.get_cardinality()}")
					if(ll.get_id()=="subject" or ll.get_id()=="ism_transition"):
						xelemFixable+=1
					else:
						logging.debug(f"LEAF NOT INSTANTIATED {ll.get_id()} {ll.get_path()}")


#		print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
# create an ActualNoLeaf for each NoLeaf whose mapping is instanciated in xml		
		nnelem=0
		nxelem=0
		noflist=[]
		listofActualNoleafs=[]
#		print(listofActualNoleafs)
		for (indexnoleaf,ll) in enumerate(listofnoleafsannotated):
#			print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
			logging.debug("********************************************")
			logging.debug(f'noleaf ids: {ll.get_id()}')
#			print(f'indexnoleaf {indexnoleaf}/{len(listofnoleafsannotated)}')
			noflist=meventfinder(ll,all_items_bh)
#			print (noflist)
			if len(noflist) > 0:
				for f in noflist:
					logging.debug("********************************************")
					logging.debug('index in bh items {f}, {element all_items_bh[f]}')
#					print (ll.get_path(),all_items_bh[f])
					listofActualNoleafs.append(ActualNoLeaf(ll,f))
#					print("found")
					nnelem=nnelem+1
			else:
#					print (ll.get_path(), 'Not found')
					nxelem=nxelem+1	


		print(f'{nelem} mapped leafs')
		logging.info(f'{nelem} mapped leafs')
		print(f'{xelem} leafs not found')
		logging.info(f'{xelem} leafs not found')
		logging.info(f'{xelemNC} should be instantiated (according only to leafs)')
		print(f'{xelemFixable}/{xelemC} can be reasonably omitted')
		logging.info(f'{xelemFixable}/{xelemC} can be reasonably omitted')

		logging.info(f'{nnelem} mapped noleafs')
		logging.info(f'{nxelem} noleafs not found')
		for ll in listofActualLeafs:
			logging.debug(f'listofActualleafs {ll.get_id()} {ll.get_path()}')
		listofoccurrences=FindOccurencesFromNoLeafs(listofActualNoleafs)

		#create the composition
		c=Composition(listofActualLeafs,listofActualNoleafs,listofoccurrences)

		#write the composition
		c.writeComposition(outputfile)




if __name__ == '__main__':
    main()
