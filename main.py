#!/usr/bin/python3
'''convert given format to_openehr compositions'''
import json
import logging
from webtemplate.webtemplate_reader import read_wt
from webtemplate.webtemplate_parser import parse_wt
from crc_cohort.xml_parser import find_ns
from composition.occurrences import FindOccurencesFromNoLeafs
from composition.composition import Composition
from composition.utils import readinput,retrieve_all_items_patient,check_missing_leafs,create_actual_leafs,create_actual_noleafs
import argparse
import config


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

	if(args.convertfrom == "bbmrixml"):
		config.fr=1
	elif(args.convertfrom== "phenopacketV2"):
		config.fr=2
	else:
		print(f"Error: 'convertfrom' parameter must be chosen from the parameter values range")
		exit(1)		


	# READ AND PARSE WEBTEMPLATE
	#webtemplate="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/TMP/WebTemplatecrc_cohort_dazipMOD.json"
	#webtemplate="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CRC_COHORT/crc_cohort_v2.json"
	myjson,defaultLanguage=read_wt(webtemplate)
	logging.info(json.dumps(myjson, indent = 4, sort_keys=True))

	#create leafs, noleafs(4 molteplicity) and nodes
	listofleafs,listofnoleafs,listofNodes=parse_wt(myjson)

	logging.debug("Leafs")
	logging.debug(f"number of leafs={len(listofleafs)}")
	for ll in listofleafs:
		logging.debug(f"leaf {ll.get_all()}")

	logging.debug("********************************************")
	logging.debug("No leafs annotated")
	logging.debug(f"number of no leaf annotated={len(listofnoleafs)}")
	for nl in listofnoleafs:
		logging.debug(f"no leaf annotated {nl.get_id()} {nl.get_annotation()}{nl.get_path()}")
	logging.debug("********************************************")	

	logging.debug("NOODES")
	for n in listofNodes:
		logging.debug(f"path {n.get_path()} maxcardinality {n.get_cardinality()[1]}")	


	# READ AND PARSE INPUTFILE
	#inputfile="/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/TMP/import_exampleMOD.xml"
	listofpatients=readinput(inputfile)

	#NAMESPACE (for xml)
	ns=""
	if(config.fr==1):
		ns=find_ns(listofpatients[0])


	#LOOP OVER PATIENTS
	for i in range(len(listofpatients)):
#		bhp=listofpatients[i]
		p_i=listofpatients[i]
		outputfile=outputfilebasename+"_"+str(i+1)+".json"
		all_items_patient_i=retrieve_all_items_patient(p_i,ns)
#		all_items_bh=(all_items(bhp,ns))
		logging.debug(f'all items for patient {i+1}')
		logging.debug(all_items_patient_i)
		logging.debug("********************************************")

		# CREATE AN ACTUALLEAF FOR EACH LEAF WHOSE MAPPING IS INSTANCIATED IN THE INPUT FILE
		# PLUS FILL WITH DEFAULT VALUES
		listofActualLeafs=[]
		listofNoActualLeafs=[]
		create_actual_leafs(listofleafs,all_items_patient_i,listofActualLeafs,listofNoActualLeafs,listofNodes,defaultLanguage)

		#THIS SUBROUTINE IS ONLY TO LOOK FOR LEAFS THAT SHOULD HAVE BEEN INSTANTIATED!!!!
		check_missing_leafs(listofNoActualLeafs,listofActualLeafs,listofNodes)

		# CREATE AN ACTUALNOLEAF FOR EACH NOLEAF THAT IS ANNOTATED AND WHOSE MAPPING IS INSTANCIATED IN THE INPUT FILE
		# this is necessary to treat nodes molteplicity 
		listofActualNoleafs=[]	
		create_actual_noleafs(listofnoleafs,all_items_patient_i,listofActualNoleafs)	

		for ll in listofActualLeafs:
			logging.debug(f'listofActualleafs {ll.get_id()} {ll.get_path()}')

		#FIND OCCURRENCES OF EACH NODE WITH MOLTEPLICITY			
		listofoccurrences=FindOccurencesFromNoLeafs(listofActualNoleafs)

		#CREATE THE COMPOSITION
		c=Composition(listofActualLeafs,listofActualNoleafs,listofoccurrences)

		#WRITE THE COMPOSITION
		des="th"
		if(i+1==1):
			des="st"
		elif(i+1==2):
			des="nd"
		elif(i+1==3):
			des="rd"
		c.writeComposition(outputfile)
		print(f"{i+1}{des} outputfile {outputfile}")
		logging.info(f"{i+1}{des} outputfile {outputfile}")
		print("----------------------------------------------")
		logging.info("----------------------------------------------")


if __name__ == '__main__':
    main()
