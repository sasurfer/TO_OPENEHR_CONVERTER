#!/usr/bin/python3
'''find an element in the BHPatient tree and return its index or not found'''
import xml.etree.ElementTree as ET
import logging
import copy
from composition.leaf import ActualLeaf,ActualNoLeaf


def mefinder(myleaf,listofitems):
	annotation=myleaf.get_annotation()
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
	logging.debug(f'MEVENTFINDER myleafid={myleaf.get_id()} myleafpath={myleaf.get_path()}')
	logging.debug(f'annotation: {myleaf.get_annotation()}')
	annotation=myleaf.get_annotation()
	indexes=[]
	if ('XSD label' in annotation):
		logging.debug(f"looking for {annotation['XSD label']}")
		for index,(a,b,c), in enumerate(listofitems):
			logging.debug(index)
			for k in c:
				logging.debug(f'c[k] {c[k]}')
				if c[k]==annotation['XSD label']:
					indexes.append(index)
					logging.debug(f'FOUNDDDDDDDDD {index}')
		return indexes
	return indexes


def mtimefinder(annotation,listofitems):
	#null flavour if unknown
	time="10/12/9999"
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

def fill_in_ism(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'ism transition pathassoc={ll.get_path()} path={path}')
	cstate={}
	cstate["value"]="completed"
	cstate["terminology"]="openehr"
	cstate["code"]="532"
	closestposition=ll.get_positioninXML()
	lnew=findExactPath(listofleafs,path)
	lnewnew=copy.deepcopy(lnew)
	lnewnew.path=path
	return ActualLeaf(lnewnew,cstate,closestposition)

def fill_in_encoding(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'encoding pathassoc={ll.get_path()} path={path}')
	encoding={}
	encoding['code']="UTF-8"
	encoding['terminology']="IANA_character-sets"
	closestposition=ll.get_positioninXML()
	lnew=findExactPath(listofleafs,path)
	lnewnew=copy.deepcopy(lnew)	
	return ActualLeaf(lnewnew,encoding,closestposition)


def fill_in_default(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'{ll.get_id()} pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)		
	defvalue=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	lnewnew=copy.deepcopy(lnew)	
	return ActualLeaf(lnewnew,defvalue,closestposition)

# def fill_in_from_event(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'from event pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	fe=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,fe,closestposition)

def fill_in_language(path,ll,listofleafs,defaultLanguage):
	from composition.utils import findExactPath
	language={}
	language['code']=defaultLanguage
	language['terminology']="ISO_639-1"
	closestposition=ll.get_positioninXML()
	logging.debug(f"language pathassoc={ll.get_path()} path={path} ")
	lnew=findExactPath(listofleafs,path)
	lnewnew=copy.deepcopy(lnew)	
	return ActualLeaf(lnewnew,language,closestposition)

def fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'time pathassoc={ll.get_path()} path={path}')
	annotation={}
	for n in listofNodes:
		if(n.get_path()==shortpath):
			annotation=n.get_annotation()
			break
	time=mtimefinder(annotation,all_items_patient_i)
	closestposition=ll.get_positioninXML()
	lnew=findExactPath(listofleafs,path)
	lnewnew=copy.deepcopy(lnew)	
	return ActualLeaf(lnewnew,time,closestposition)	


# def fill_in_procedure_name(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'procedure name pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)		
# 	procedurename=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,procedurename,closestposition)

def fill_in_diagnosis(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'{ll.get_id()} pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	pdg={}
	pdg['value']=lnew.get_acceptable_values()[0]['list'][0]['label']
	pdg['code']=lnew.get_acceptable_values()[0]['list'][0]['value']
	pdg['terminology']=lnew.get_acceptable_values()[0]['terminology']	
	lnewnew=copy.deepcopy(lnew)	
	return ActualLeaf(lnewnew,pdg,0)

# def fill_in_primary_diagnosis(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'{ll.get_id()} pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	pdg={}
# 	pdg['value']=lnew.get_acceptable_values()[0]['list'][0]['label']
# 	pdg['code']=lnew.get_acceptable_values()[0]['list'][0]['value']
# 	pdg['terminology']=lnew.get_acceptable_values()[0]['terminology']	
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,pdg,0)

# def fill_in_metastasis_diagnosis(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'metastatis diagnosis pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	mdg={}
# 	mdg['value']=lnew.get_acceptable_values()[0]['list'][0]['label']
# 	mdg['code']=lnew.get_acceptable_values()[0]['list'][0]['value']
# 	mdg['terminology']=lnew.get_acceptable_values()[0]['terminology']	
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,mdg,0)


# def fill_in_test_name(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'test name pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	testname=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,testname,closestposition)

# def fill_in_problem_diagnosis_name(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'problem diagnosis name pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	pdnn={}
# 	pdnn['value']=lnew.get_acceptable_values()[0]['list'][0]['label']
# 	pdnn['code']=lnew.get_acceptable_values()[0]['list'][0]['value']
# 	pdnn['terminology']=lnew.get_acceptable_values()[0]['terminology']	
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,pdnn,closestposition)

# def fill_in_therapy(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'therapy pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	therapy=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,therapy,closestposition)		

# def fill_in_variant_name(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'variant_name pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	vn=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,vn,closestposition)


# def fill_in_health_risk(path,ll,listofleafs):
# 	from composition.utils import findExactPath
# 	logging.debug(f'health_risk pathassoc={ll.get_path()} path={path}')
# 	lnew=findExactPath(listofleafs,path)
# 	hr=lnew.get_acceptable_values()[0]["defaultValue"]
# 	closestposition=ll.get_positioninXML()
# 	lnewnew=copy.deepcopy(lnew)	
# 	return ActualLeaf(lnewnew,hr,closestposition)




def complete_actual_leafs_crc(templateId,listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs):
	'''add default values taken from the template or not to the compulsory fields not fillable with the input data'''
	from composition.utils import findExactPath
	nelemn=0

	#add dependent leafs
	for (indexleaf,ll) in enumerate(listofActualLeafs):
		logging.debug(f'leaf ids second sweep DEFAULT ITEMS: {ll.get_id()}')
		lid=ll.get_id()

		if(lid=='mismatch_repair_gene_expression'):
			#test_name
			path='/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/any_event:0/test_name'
			al=fill_in_default(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/any_event:0/time'
			shortpath='/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4


		elif(lid=="biological_sex"):#gender
			#encoding
			path='/'+templateId+'/patient_data/gender/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/patient_data/gender/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			nelemn+=2

		elif(lid=="colonoscopy"):#colonoscopy
			#ism
			path='/'+templateId+'/diagnostic_examinations/colonoscopy/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/diagnostic_examinations/colonoscopy/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)


			#language
			path='/'+templateId+'/diagnostic_examinations/colonoscopy/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/diagnostic_examinations/colonoscopy/time'
			shortpath='/'+templateId+'/diagnostic_examinations/colonoscopy'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			#provedure_name
			path='/'+templateId+'/diagnostic_examinations/colonoscopy/procedure_name'
			al=fill_in_default(path,ll,listofleafs)

			listofActualLeafs.append(al)

			nelemn+=5

#BECOME COMPULSORY
		# elif(lid=="age_at_diagnosis"):#primary diagnosis
		# 	#encoding
		# 	path='/'+templateId+'/patient_data/primary_diagnosis/encoding'
		# 	al=fill_in_encoding(path,ll,listofleafs)
		# 	listofActualLeafs.append(al)

		# 	#language
		# 	path='/'+templateId+'/patient_data/primary_diagnosis/language'
		# 	al=fill_in_language(path,ll,listofleafs,defaultLanguage)
		# 	listofActualLeafs.append(al)

		# 	#primary_diagnosis
		# 	path='/'+templateId+'/patient_data/primary_diagnosis/primary_diagnosis'
		# 	al=fill_in_diagnosis(path,ll,listofleafs)
		# 	listofActualLeafs.append(al)

		# 	nelemn+=3

		elif(lid=="time_of_recurrence"):#metastasis diagnosis
			#from event
			path='/'+templateId+'/patient_data/metastasis_diagnosis/metastasis_diagnosis2/metastasis_diagnosis/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/patient_data/metastasis_diagnosis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/patient_data/metastasis_diagnosis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#metastasis diagnosis
			path='/'+templateId+'/patient_data/metastasis_diagnosis/metastasis_diagnosis'
			al=fill_in_diagnosis(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="material_type"):#specimen
			#encoding
			path='/'+templateId+'/histopathology/result_group/laboratory_test_result/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/histopathology/result_group/laboratory_test_result/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/test_name'
			al=fill_in_default(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/time'
			shortpath='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="localization_of_primary_tumor"):#cancer diagnosis
			#encoding
			path='/'+templateId+'/histopathology/result_group/cancer_diagnosis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/histopathology/result_group/cancer_diagnosis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#problem_diagnosis_name
			path='/'+templateId+'/histopathology/result_group/cancer_diagnosis/problem_diagnosis_name'
			al=fill_in_diagnosis(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=3



		elif(lid=="date_of_start_of_targeted_therapy"):#targeted_therapy
			#ism
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/encoding'			
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/targeted_therapy_start/start_of_targeted_therapy/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#therapy
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/therapy'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/time'
			shortpath='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=6

		elif(lid=="date_of_start_of_pharmacotherapy" ):#pharmacotherapy
			#ism
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_start/start_of_pharmacotherapy/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/time'
			shortpath='/'+templateId+'/therapies/pharmacotherapy/medication_management:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="specific_response"):#response to therapy
			#encoding
			path='/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			nelemn+=2

		elif(lid=="ct"):#ct
			#ism
			path='/'+templateId+'/diagnostic_examinations/ct/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/diagnostic_examinations/ct/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/diagnostic_examinations/ct/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/'+templateId+'/diagnostic_examinations/ct/procedure_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/diagnostic_examinations/ct/time'
			shortpath='/'+templateId+'/diagnostic_examinations/ct'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="liver_imaging"):#ctliver_imaging
			#ism
			path='/'+templateId+'/diagnostic_examinations/liver_imaging/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/'+templateId+'/diagnostic_examinations/liver_imaging/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/diagnostic_examinations/liver_imaging/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/'+templateId+'/diagnostic_examinations/liver_imaging/procedure_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/diagnostic_examinations/liver_imaging/time'
			shortpath='/'+templateId+'/diagnostic_examinations/liver_imaging'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="lung_imaging"):#lung_imaging
			#ism
			path='/'+templateId+'/diagnostic_examinations/lung_imaging/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/'+templateId+'/diagnostic_examinations/lung_imaging/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/diagnostic_examinations/lung_imaging/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/'+templateId+'/diagnostic_examinations/lung_imaging/procedure_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/diagnostic_examinations/lung_imaging/time'
			shortpath='/'+templateId+'/diagnostic_examinations/lung_imaging'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="mri"):#mri
			#ism
			path='/'+templateId+'/diagnostic_examinations/mri/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/'+templateId+'/diagnostic_examinations/mri/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			#language
			path='/'+templateId+'/diagnostic_examinations/mri/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/'+templateId+'/diagnostic_examinations/mri/procedure_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/diagnostic_examinations/mri/time'
			shortpath='/'+templateId+'/diagnostic_examinations/mri'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="braf_pic3ca_her2_mutation_status"):#oncology_mutations_test
			#encoding
			path='/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)				

			#language
			path='/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/any_event:0/test_name'
			al=fill_in_default(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/any_event:0/time'
			shortpath='/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="microsatellite_instability"):#microsatellite_instability
			#encoding
			path='/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)				


			#language
			path='/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)


			#test_name
			path='/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis/any_event:0/test_name'
			al=fill_in_default(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis/any_event:0/time'
			shortpath='/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis:0/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="nras_exon_4_codons_117_or_146"):#nras/kras mutation
			#encoding
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/test_name'
			al=fill_in_default(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/time'
			shortpath='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_4_codons_117_or_146/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="nras_exon_3_codons_59_or_61"):#nras_exon_3_codons_59_or_61
			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_3_codons_59_or_61/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1

		elif(lid=="nras_exon_2_codons_12_or_13"):#nras_exon_2_codons_12_or_13|
			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_2_codons_12_or_13/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_4_codons_117_or_146"):#kras_exon_4_codons_117_or_146
			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_4_codons_117_or_146/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_3_codons_59_or_61"):#kras_exon_3_codons_59_or_61
			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_3_codons_59_or_61/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_2_codons_12_or_13"):#kras_exon_2_codons_12_or_13
			#variant_name
			path='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_2_codons_12_or_13/variant_name'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="risk_situation_only_hnpcc"):#health_risk_assessment
			#encoding
			path='/'+templateId+'/molecular_markers/result_group/health_risk_assessment/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/molecular_markers/result_group/health_risk_assessment/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#health_risk
			path='/'+templateId+'/molecular_markers/result_group/health_risk_assessment/health_risk'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)	

			nelemn+=3		

		elif(lid=="date_of_start_of_radiation_therapy"):#radiation therapy
			#encoding
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from_event
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_start/start_of_radiation_therapy/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#ism
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#therapy
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/therapy'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/time'
			shortpath='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=6			

		elif(lid=="date_of_end_of_radiation_therapy"):#end_of_radiation_therapy
			#from_event
			path='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_end/end_of_radiation_therapy/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1

		elif(lid=="date_of_end_of_targeted_therapy"):#end_of_targeted_therapy
			#from_event
			path='/'+templateId+'/therapies/targeted_therapy/targeted_therapy:0/targeted_therapy_end/end_of_targeted_therapy:0/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1			

		elif(lid=="date_of_end_of_pharmacotherapy"):#end_of_pharmacotherapy
			#from_event
			path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_end/end_of_pharmacotherapy/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1						

		elif(lid=="time_of_therapy_response"):#response timing
			#from_event
			path='/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/response_timing/therapy_response_timestamp/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1						



	#VARIOUS FIXES FOR MORE THAN ONE MISSING COMPULSORY VALUES
	#CREATE LISTS FOR THE FIXES
	listofscheme=[]
	listofschemeother=[]
	listofdateofstart=[]
	listofother=[]
	posls=[]
	poslso=[]
	posdt=[]
	poso=[]
	nos=0
#
	listloc=[]
	listmor=[]
	posloc=[]
	posmor=[]
	pt=[]
	pospt=[]
#
	listmat=[]
	listsam=[]
	listyear=[]
	listgrad=[]
	listuicc=[]
	listwho=[]
	listlm=[]
	posmat=[]
	possam=[]
	posyear=[]
	posgrad=[]
	posuicc=[]
	poswho=[]
	poslm=[]
#
	loctum=[]
	posloctum=[]
	surgty=[]
	possurgty=[]
	ssr=[]
	posssr=[]
	surgrad=[]
	possurgrad=[]
#
	pmod=[]
	pospmod=[]
#
	ttr=[]
	posttr=[]
	sresp=[]
	possresp=[]
#
	vitstat=[]
	posvitstat=[]
	tlevs=[]
	postlevs=[]
	osurvs=[]
	pososurvs=[]
#
	rln=[]
	posrln=[]
	stage=[]
	posstage=[]
#
	osurgtype=[]
	pososurgtype=[]
#
	bsex=[]
	posbsex=[]
#
	dmeta=[]
	posdmeta=[]
#
	nras2=[]
	nras3=[]
	nras4=[]
	kras2=[]
	kras3=[]
	kras4=[]
	posnras2=[]
	posnras3=[]
	posnras4=[]
	poskras2=[]
	poskras3=[]
	poskras4=[]
#
	dert=[]
	dsrt=[]
	posdert=[]
	posdsrt=[]
#
	for ll in listofActualLeafs:
		lid=ll.get_id()
		lpath=ll.get_path()
#		
		if(lid=='scheme_of_pharmacotherapy'):
			listofscheme.append(ll)
			posls.append(ll.get_positioninXML())
			if(ll.get_data()).upper()=='OTHER':
				listofschemeother.append(ll)
				poslso.append(ll.get_positioninXML())
		elif(lid=='date_of_start_of_pharmacotherapy'):
			listofdateofstart.append(ll)
			posdt.append(ll.get_positioninXML())
		elif(lid=='other_pharmacotherapy_scheme'):
			if(ll.getnull()==False):
				listofother.append(ll)
				poso.append(ll.get_positioninXML())
		elif(lid=='localization_of_primary_tumor'):
			listloc.append(ll)
			posloc.append(ll.get_positioninXML())
		elif(lid=='morphology'):
			listmor.append(ll)
			posmor.append(ll.get_positioninXML())
		elif(lid=='material_type'):
			listmat.append(ll)
			posmat.append(ll.get_positioninXML())
		elif(lid=='sample_id'):
			listsam.append(ll)
			possam.append(ll.get_positioninXML())
		elif(lid=='year_of_sample_collection'):
			listyear.append(ll)
			posyear.append(ll.get_positioninXML())
		elif(lid=='grade'):
			listgrad.append(ll)
			posgrad.append(ll.get_positioninXML())
		elif(lid=='uicc_version'):
			listuicc.append(ll)
			posuicc.append(ll.get_positioninXML())
		elif(lid=='who_version'):
			listwho.append(ll)
			poswho.append(ll.get_positioninXML())
		elif(lid=='localization_of_metastasis'):
			listlm.append(ll)
			poslm.append(ll.get_positioninXML())
		elif(lid=='location_of_the_tumor'):
			loctum.append(ll)
			posloctum.append(ll.get_positioninXML())
		elif(lid=='surgery_type'):
			surgty.append(ll)
			possurgty.append(ll.get_positioninXML())
		elif(lid=='preservation_mode'):
			pmod.append(ll)
			pospmod.append(ll.get_positioninXML())
		elif(lid=='surgery_start_relative'):
			ssr.append(ll)
			posssr.append(ll.get_positioninXML())
		elif(lid=='primary_tumour'):
			pt.append(ll)
			pospt.append(ll.get_positioninXML())
		elif(lid=='surgery_radicality'):
			surgrad.append(ll)
			possurgrad.append(ll.get_positioninXML())			
		elif(lid=='time_of_therapy_response'):
			ttr.append(ll)
			posttr.append(ll.get_positioninXML())
		elif(lid=='specific_response'):
			sresp.append(ll)
			possresp.append(ll.get_positioninXML())
		elif(lid=='vital_status'):
			vitstat.append(ll)
			posvitstat.append(ll.get_positioninXML())
		elif(lid=='timestamp_of_last_update_of_vital_status'):
			tlevs.append(ll)
			postlevs.append(ll.get_positioninXML())
		elif(lid=='overall_survival_status'):
			osurvs.append(ll)
			pososurvs.append(ll.get_positioninXML())
		elif(lid=='regional_lymph_nodes'):
			rln.append(ll)
			posrln.append(ll.get_positioninXML())
		elif(lid=='stage'):
			stage.append(ll)
			posstage.append(ll.get_positioninXML())
		elif(lid=='other_surgery_type'):
			osurgtype.append(ll)
			pososurgtype.append(ll.get_positioninXML())
		elif(lid=='biological_sex'):
			bsex.append(ll)
			posbsex.append(ll.get_positioninXML())
		elif(lid=='distant_metastasis'):
			dmeta.append(ll)
			posdmeta.append(ll.get_positioninXML())
		elif(lid=='nras_exon_2_codons_12_or_13'):
			nras2.append(ll)
			posnras2.append(ll.get_positioninXML())
		elif(lid=='nras_exon_3_codons_59_or_61'):
			nras3.append(ll)
			posnras3.append(ll.get_positioninXML())
		elif(lid=='nras_exon_4_codons_117_or_146'):
			nras4.append(ll)
			posnras4.append(ll.get_positioninXML())
		elif(lid=='kras_exon_2_codons_12_or_13'):
			kras2.append(ll)
			poskras2.append(ll.get_positioninXML())
		elif(lid=='kras_exon_3_codons_59_or_61'):
			kras3.append(ll)
			poskras3.append(ll.get_positioninXML())
		elif(lid=='kras_exon_4_codons_117_or_146'):
			kras4.append(ll)
			poskras4.append(ll.get_positioninXML())
		elif(lid=='date_of_end_of_radiation_therapy'):
			dert.append(ll)
			posdert.append(ll.get_positioninXML())
		elif(lid=='date_of_start_of_radiation_therapy'):
			dsrt.append(ll)
			posdsrt.append(ll.get_positioninXML())

	logging.debug(f'LIST LEN')
	logging.debug(f'scheme_of_pharmacotherapy len={len(posls)}')
	logging.debug(f'scheme_of_pharmacotherapy other len={len(poslso)}')
	logging.debug(f'date_of_start_of_pharmacotherapy len={len(posdt)}')
	logging.debug(f'other_pharmacotherapy_scheme len={len(poso )}')
	logging.debug(f'localization_of_primary_tumor len={len(posloc)}')
	logging.debug(f'morphology len={len(posmor)}')
	logging.debug(f'material_type len={len(posmat)}')
	logging.debug(f'sample_id len={len(possam)}')
	logging.debug(f'year_of_sample_collection len={len(posyear)}') 
	logging.debug(f'grade len={len(posgrad)}')
	logging.debug(f'stage len={len(posstage)}')
	logging.debug(f'uicc_version len={len(posuicc)}')
	logging.debug(f'who_version len={len(poswho)}') 
	logging.debug(f'localization_of_metastasis len={len(poslm)}') 
	logging.debug(f'location_of_the_tumor len={len(posloctum)}')
	logging.debug(f'surgery_type len={len(possurgty)}')
	logging.debug(f'preservation_mode len={len(pospmod)}')
	logging.debug(f'surgery_start_relative len={len(posssr)}')
	logging.debug(f'primary_tumour len={len(pospt)}')
	logging.debug(f'surgery_radicality len={len(possurgrad)}')	
	logging.debug(f'time_of_therapy_response len={len(posttr)}')	
	logging.debug(f'specific_response len={len(possresp)}')	
	logging.debug(f'vital_status len={len(posvitstat)}')	
	logging.debug(f'timestamp_of_last_update_of_vital_status len={len(postlevs)}')	
	logging.debug(f'overall_survival_status len={len(pososurvs)}')	
	logging.debug(f'regional_lymph_nodes len={len(posrln)}')
	logging.debug(f'other_surgery_type len={len(pososurgtype)}')
	logging.debug(f'biological_sex len={len(posbsex)}')
	logging.debug(f'distant_metastasis len={len(posdmeta)}')
	logging.debug(f'nras_exon_2_codons_12_or_13  len={len(posnras2)}')
	logging.debug(f'nras_exon_3_codons_59_or_61  len={len(posnras3)}')
	logging.debug(f'nnras_exon_4_codons_117_or_146  len={len(posnras4)}')
	logging.debug(f'kras_exon_2_codons_12_or_13  len={len(posnras2)}')
	logging.debug(f'kras_exon_3_codons_59_or_61  len={len(posnras3)}')
	logging.debug(f'kras_exon_4_codons_117_or_146  len={len(posnras4)}')
	logging.debug(f'date_of_start_of_radiation_therapy  len={len(posdsrt)}')
	logging.debug(f'date_of_end_of_radiation_therapy  len={len(posdert)}')

	#FIX when we have date_of_end_of_radiation_therapy but we don't have date_of_start_of_radiation_thearapy
	if(len(dsrt) < len(dert)):#missing date_of_start_of_radiation_therapy
		idis='date_of_end_of_radiation_therapy'
		idmissing='date_of_start_of_radiation_therapy'
		pathmissing='/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_start/start_of_radiation_therapy/date_of_start_of_radiation_therapy'
		other_paths=[['encoding','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/encoding'],\
		['from_event','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_start/start_of_radiation_therapy/from_event'],
		['ism','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/ism_transition/current_state'],
		['language','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/language'],
		['therapy','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/therapy'],
		['time','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0/time','/'+templateId+'/therapies/radiation_therapy/radiation_therapy:0']]
		nadd=fix_too_many_missing(idis,idmissing,dert,dsrt,posdert,posdsrt,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd
	
	#FIX when we have time_of_therapy_response but we don't have specific_response
	if(len(sresp) < len(ttr)):#missing specific_response
		print('fiuuuuuuuuuuuuuuuu')
		idis='time_of_therapy_response'
		idmissing='specific_response'
		pathmissing='/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/specific_response'
		other_paths=[['encoding','/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/encoding'],\
		['language','/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/language']]
		nadd=fix_too_many_missing(idis,idmissing,ttr,sresp,posttr,possresp,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd

	#FIX when we have specific_response but we don't have time_of_therapy_response
	if(len(ttr) < len(sresp)):#missing ttr
		idis='specific_response'
		idmissing='time_of_therapy_response'
		pathmissing='/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/response_timing/therapy_response_timestamp/time_of_therapy_response'
		nadd=fix_too_many_missing(idis,idmissing,sresp,ttr,possresp,posttr,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd	


	#FIX when we have nras but not kras
	if(len(kras2) < len(nras2)):#missing kras2
		idis='nras_exon_2_codons_12_or_13'
		idmissing='kras_exon_2_codons_12_or_13'
		pathmissing='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_2_codons_12_or_13/kras_exon_2_codons_12_or_13'
		other_paths=[['variant_name','/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_2_codons_12_or_13/variant_name']]
		nadd=fix_too_many_missing(idis,idmissing,nras2,kras2,posnras2,poskras2,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd
	if(len(kras3) < len(nras3)):#missing kras3
		idis='nras_exon_3_codons_59_or_61'
		idmissing='kras_exon_3_codons_59_or_61'
		pathmissing='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_3_codons_59_or_61/kras_exon_3_codons_59_or_61'
		other_paths=[['variant_name','/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_3_codons_59_or_61/variant_name']]
		nadd=fix_too_many_missing(idis,idmissing,nras3,kras3,posnras3,poskras3,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd
	if(len(kras4) < len(nras4)):#missing kras4
		idis='nras_exon_4_codons_117_or_146'
		idmissing='kras_exon_4_codons_117_or_146'
		pathmissing='/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_4_codons_117_or_146/kras_exon_4_codons_117_or_146'
		other_paths=[['variant_name','/'+templateId+'/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_4_codons_117_or_146/variant_name']]
		nadd=fix_too_many_missing(idis,idmissing,nras4,kras4,posnras4,poskras4,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd

	#FIX when we have timestamp_of_last_update_of_vital_status but we don't have vital_status
	if(len(vitstat) < len(tlevs)):#missing vital_status
		idis='timestamp_of_last_update_of_vital_status'
		idmissing='vital_status'
		pathmissing='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/vital_status'
		nadd=fix_too_many_missing(idis,idmissing,tlevs,vitstat,postlevs,posvitstat,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE timestamp_of_last_update_of_vital_status but we don't have overall_survival_status
	if(len(osurvs) < len(tlevs)):#missing overall_survival_status
		idis='timestamp_of_last_update_of_vital_status'
		idmissing='overall_survival_status'
		pathmissing='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/vital_status_timing/overall_survival_status/overall_survival_status'
		nadd=fix_too_many_missing(idis,idmissing,tlevs,osurvs,postlevs,pososurvs,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd	

	#FIX WHEN WE HAVE overall_survival_status but we don't have vital_status
	if(len(vitstat) < len(osurvs)):#missing overall_survival_status
		idis='overall_survival_status'
		idmissing='vital_status'
		pathmissing='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/vital_status'
		nadd=fix_too_many_missing(idis,idmissing,osurvs,vitstat,pososurvs,posvitstat,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd	

	#FILL WHEN we (finally) have vital_status
	if(len(vitstat)>0):
		ll=vitstat[0]
		#encoding
		path='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/encoding'
		al=fill_in_encoding(path,ll,listofleafs)
		listofActualLeafs.append(al)

		#language
		path='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/language'
		al=fill_in_language(path,ll,listofleafs,defaultLanguage)
		listofActualLeafs.append(al)

	#FILL WHEN we (finally) have overall_survival_status
	if(len(osurvs)>0):
		ll=osurvs[0]
		#from_event
		path='/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/vital_status_timing/overall_survival_status/from_event'
		al=fill_in_default(path,ll,listofleafs)
		listofActualLeafs.append(al)



	#FIX when we have info about samples (material_type) but we don't have anything about cancer diagnosis. we create morphology
	if(len(listmor)+len(listloc)+len(pt)+len(listgrad)+len(listwho)+len(listuicc)+len(stage)==0 and len(listmat)>0):
		idis='material_type'
		idmissing='morphology'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/morphology'
		nadd=fix_too_many_missing(idis,idmissing,listmat,listmor,posmat,posmor,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd	

	#FIX WHEN WE HAVE distant_metastasis but we don't have Morphology 
	if(len(listmor) < len(dmeta)):
		idis='distant_metastasis'
		idmissing='morphology'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/morphology'
		nadd=fix_too_many_missing(idis,idmissing,dmeta,listmor,posdmeta,posmor,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a localization_of_primary_tumor
	if(len(listloc) < len(listmor)):#missing localization
		idis='morphology'
		idmissing='localization_of_primary_tumor'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/localization_of_primary_tumor'
		other_paths=[['encoding','/'+templateId+'/histopathology/result_group/cancer_diagnosis/encoding'],\
		['language','/'+templateId+'/histopathology/result_group/cancer_diagnosis/language'],\
		['problem_diagnosis_name','/'+templateId+'/histopathology/result_group/cancer_diagnosis/problem_diagnosis_name']]
		nadd=fix_too_many_missing(idis,idmissing,listmor,listloc,posmor,posloc,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd

	#FIX when we have primary_tumour bu we don't have a localization_of_primary_tumor
	if(len(listloc) < len(pt)):#missing localization
		idis='primary_tumour'
		idmissing='localization_of_primary_tumor'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/localization_of_primary_tumor'
		other_paths=[['encoding','/'+templateId+'/histopathology/result_group/cancer_diagnosis/encoding'],\
		['language','/'+templateId+'/histopathology/result_group/cancer_diagnosis/language'],\
		['problem_diagnosis_name','/'+templateId+'/histopathology/result_group/cancer_diagnosis/problem_diagnosis_name']]
		nadd=fix_too_many_missing(idis,idmissing,pt,listloc,pospt,posloc,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd

	#FIX when we have primary_tumour bu we don't have a morphology
	if(len(listmor) < len(pt)):#missing localization
		idis='primary_tumour'
		idmissing='morphology'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/morphology'
		nadd=fix_too_many_missing(idis,idmissing,pt,listmor,pospt,posmor,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd


	#FIX WHEN WE HAVE Morphology bu we don't have localization_of_metastasis
	if(len(listlm) < len(listmor)):
		idis='morphology'
		idmissing='localization_of_metastasis'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/distant_metastasis/anatomical_location:0/localization_of_metastasis'
		nadd=fix_too_many_missing(idis,idmissing,listmor,listlm,posmor,poslm,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have distant_metastasis
	if(len(dmeta) < len(listmor)):
		idis='morphology'
		idmissing='distant_metastasis'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/distant_metastasis'
		nadd=fix_too_many_missing(idis,idmissing,listmor,dmeta,posmor,posdmeta,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd


	#FIX WHEN WE HAVE Morphology but we don't have a grade
	if(len(listgrad) < len(listmor)):#missing grade
		idis='morphology'
		idmissing='grade'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/grade'
		nadd=fix_too_many_missing(idis,idmissing,listmor,listgrad,posmor,posgrad,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a who_version
	if(len(listwho) < len(listmor)):#missing grade
		idis='morphology'
		idmissing='who_version'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/histological_grading/who_version'
		nadd=fix_too_many_missing(idis,idmissing,listmor,listwho,posmor,poswho,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a uicc_version
	if(len(listuicc) < len(listmor)):#missing uicc_version
		idis='morphology'
		idmissing='uicc_version'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/uicc_version'
		nadd=fix_too_many_missing(idis,idmissing,listmor,listuicc,posmor,posuicc,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a stage
	if(len(stage) < len(listmor)):#missing uicc_version
		idis='morphology'
		idmissing='stage'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/stage'
		nadd=fix_too_many_missing(idis,idmissing,listmor,stage,posmor,posstage,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a primary_tumour
	if(len(pt) < len(listmor)):#missing primary_tumour
		idis='morphology'
		idmissing='primary_tumour'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/primary_tumour'
		nadd=fix_too_many_missing(idis,idmissing,listmor,pt,posmor,pospt,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN WE HAVE Morphology bu we don't have a regional_lymph_nodes
	if(len(rln) < len(listmor)):#missing uicc_version
		idis='morphology'
		idmissing='regional_lymph_nodes'
		pathmissing='/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/regional_lymph_nodes'
		nadd=fix_too_many_missing(idis,idmissing,listmor,rln,posmor,posrln,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN we have a year_of_sample_collection but we don't have a sample_id 
	if(len(listsam) < len(listyear)):#missing sample_id
		idis='year_of_sample_collection'
		idmissing='sample_id'
		pathmissing='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/sample_id'
		nadd=fix_too_many_missing(idis,idmissing,listyear,listsam,posyear,possam,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN we have a sample_id but we don't have a material_type or viceversa
	if(len(listmat)<len(listsam)):#missing material_type
		idis='sample_id'
		idmissing='material_type'
		pathmissing='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/material_type'
		other_paths=[['encoding','/'+templateId+'/histopathology/result_group/laboratory_test_result/encoding'],\
		['language','/'+templateId+'/histopathology/result_group/laboratory_test_result/language'],\
		['test_name','/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/test_name'],\
		['time','/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/time','/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0']]
		nadd=fix_too_many_missing(idis,idmissing,listsam,listmat,possam,posmat,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd
	elif(len(listsam)<len(listmat)):#missing sample_id
		idis='material_type'
		idmissing='sample_id'
		pathmissing='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/sample_id'
		nadd=fix_too_many_missing(idis,idmissing,listmat,listsam,posmat,possam,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN we have a sample_id but we don't have a year_of_sample_collection
	if(len(listyear) < len(listsam)):#missing year_of_sample
		idis='sample_id'
		idmissing='year_of_sample_collection'
		pathmissing='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/year_of_sample_collection'
		nadd=fix_too_many_missing(idis,idmissing,listsam,listyear,possam,posyear,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX WHEN we have a sample_id but we don't have a preservation_mode
	if(len(pmod) < len(listsam)):#missing preservation_mode
		idis='sample_id'
		idmissing='preservation_mode'
		pathmissing='/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/specimen_preparation/preservation_mode'
		nadd=fix_too_many_missing(idis,idmissing,listsam,pmod,possam,pospmod,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX when we have a surgery_radicality but we don't have a surgery_type		
	if(len(surgty) < len(surgrad)):#missing surgery_type
		idis='surgery_radicality'
		idmissing='surgery_type'
		pathmissing='/'+templateId+'/surgery/surgery:0/surgery_type'
		nadd=fix_too_many_missing(idis,idmissing,surgrad,surgty,possurgrad,possurgty,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX when we have a other_surgery_type but we don't have a surgery_type		
	if(len(surgty) < len(osurgtype)):#missing surgery_type
		idis='other_surgery_type'
		idmissing='surgery_type'
		pathmissing='/'+templateId+'/surgery/surgery:0/surgery_type'
		nadd=fix_too_many_missing(idis,idmissing,osurgtype,surgty,pososurgtype,possurgty,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd

	#FIX when we have a surgery_type but we don't have a surgery_radicality  	
	if(len(surgrad) < len(surgty)):#missing surgery_radicality
		idis='surgery_type'
		idmissing='surgery_radicality'
		pathmissing='/'+templateId+'/surgery/surgery:0/surgery_radicality'
		nadd=fix_too_many_missing(idis,idmissing,surgty,surgrad,possurgty,possurgrad,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd


	#FILL when we have (finally) a surgery_type
	if(len(surgty)>0):
		for ll in surgty:
			#ism
			path='/'+templateId+'/surgery/surgery:0/ism_transition/current_state'
			al=fill_in_ism(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/'+templateId+'/surgery/surgery:0/surgery_timing/surgery/from_event'
			al=fill_in_default(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/'+templateId+'/surgery/surgery:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)


			#language
			path='/'+templateId+'/surgery/surgery:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/'+templateId+'/surgery/surgery:0/time'
			shortpath='/'+templateId+'/surgery/surgery:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

	#FIX WHEN we have a surgery_type but we don't have a location_of_the_tumor
	if(len(loctum) < len(surgty)):#missing location_of_the_tumor
		idis='surgery_type'
		idmissing='location_of_the_tumor'
		pathmissing='/'+templateId+'/surgery/surgery:0/location_of_the_tumor'
		nadd=fix_too_many_missing(idis,idmissing,surgty,loctum,possurgty,posloctum,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd		

	#FIX WHEN we have a surgery_type but we don't have a surgery_start_relative
	if(len(ssr) < len(surgty)):#missing location_of_the_tumor
		idis='surgery_type'
		idmissing='surgery_start_relative'
		pathmissing='/'+templateId+'/surgery/surgery:0/surgery_timing/surgery/surgery_start_relative'
		nadd=fix_too_many_missing(idis,idmissing,surgty,ssr,possurgty,posssr,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd	

	# #FIX scheme_of_pharmacotherapy when other present
	#count all the scheme of pharmacotherapy that contain Other as value
	#and compare to the number of Other pharmacotherapy scheme
	if(len(listofschemeother) < len(listofother)):#missing schemes
		difference=len(listofother)-len(listofschemeother)
		if(len(listofschemeother)==0):
			for ll in listofother:
				#create a new scheme_of_pharmacotherapy with value 'Other'			
				path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/scheme_of_pharmacotherapy'
				lnew=findExactPath(listofleafs,path)
				logging.debug(f'scheme_of_pharmacotherapy from other_pharmacotherapy_scheme nopathassoc path={path}')
				value='Other'
				closestposition=ll.get_positioninXML()
				lnewnew=copy.deepcopy(lnew)
				lladded=ActualLeaf(lnewnew,value,closestposition)
				listofActualLeafs.append(lladded)
				nelemn+=1
				listofscheme.append(lladded)
				posls.append(ll.get_positioninXML())
		else:
			positions=find_position_of_missing_element(difference,poso,poslso)

			#print(f'pos={positions}')

			for i in range(0,difference):
				ll=listofother[positions[i]]
				#create a new scheme_of_pharmacotherapy with value 'Other'			
				path='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/scheme_of_pharmacotherapy'
				lnew=findExactPath(listofleafs,path)
				logging.debug(f'scheme_of_pharmacotherapy from other_pharmacotherapy_scheme nopathassoc path={path}')
				value='Other'
				closestposition=ll.get_positioninXML()
				lnewnew=copy.deepcopy(lnew)	
				lladded=ActualLeaf(lnewnew,value,closestposition)
				listofActualLeafs.append(lladded)
				nelemn+=1
				listofscheme.append(lladded)
				posls.append(ll.get_positioninXML())

	#FIX date_of_start_of_pharmacotherapy when scheme present
	if(len(listofscheme)>len(listofdateofstart)):#we miss date_of_start
		idis='scheme_of_pharmacotherapy'
		idmissing='date_of_start_of_pharmacotherapy'
		pathmissing='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_start/start_of_pharmacotherapy/date_of_start_of_pharmacotherapy'
		other_paths=[['encoding','/'+templateId+'/therapies/pharmacotherapy/medication_management:0/encoding'],\
		['ism','/'+templateId+'/therapies/pharmacotherapy/medication_management:0/ism_transition/current_state'],\
		['from_event','/'+templateId+'/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_start/start_of_pharmacotherapy/from_event'],\
		['language','/'+templateId+'/therapies/pharmacotherapy/medication_management:0/language'],\
		['time','/'+templateId+'/therapies/pharmacotherapy/medication_management:0/time','/'+templateId+'/therapies/pharmacotherapy/medication_management:0']]
		nadd=fix_too_many_missing(idis,idmissing,listofscheme,listofdateofstart,posls,posdt,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths)
		nelemn+=nadd

	#FIX scheme_of_pharmacotherapy when date_of_start_of_pharmacotherapy present
	if(len(listofdateofstart)>len(listofscheme)):#we miss date_of_start
		idis='date_of_start_of_pharmacotherapy'
		idmissing='scheme_of_pharmacotherapy'  
		pathmissing='/'+templateId+'/therapies/pharmacotherapy/medication_management:0/scheme_of_pharmacotherapy'
		nadd=fix_too_many_missing(idis,idmissing,listofdateofstart,listofscheme,posdt,posls,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i)
		nelemn+=nadd


	#FIX biological_sex missing
	if(len(bsex)==0):
		path='/'+templateId+'/patient_data/gender/biological_sex'
		lnew=findExactPath(listofleafs,path)
		logging.debug(f'biological_sex nopathassoc path={path}')
		value='NULLFLAVOURsex'
		closestposition=0
		lnewnew=copy.deepcopy(lnew)	
		ladded=ActualLeaf(lnewnew,value,closestposition,True)
		listofActualLeafs.append(ladded)
		nelemn+=1	

		#encoding
		path='/'+templateId+'/patient_data/gender/encoding'
		al=fill_in_encoding(path,ladded,listofleafs)
		listofActualLeafs.append(al)

		#language
		path='/'+templateId+'/patient_data/gender/language'
		al=fill_in_language(path,ladded,listofleafs,defaultLanguage)
		listofActualLeafs.append(al)

		nelemn+=2



	#INDEPENDENT LEAFS
	#COHORT LANGUAGE
	path='/'+templateId+'/language'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'language nopathassoc path={path}')
	language={}
	language['code']=defaultLanguage
	language['terminology']="ISO_639-1"
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,language,closestposition))
	nelemn+=1

	#START_TIME
	path='/'+templateId+'/context/start_time'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'start_time path nopathassoc path={path}')
	starttime="9999-05-25T15:48:35.35Z"
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,starttime,closestposition,True))
	nelemn+=1

	#SETTING
	path='/'+templateId+'/context/setting'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'setting nopathassoc path={path}')
	setting={}
	setting['code']="238"
	setting['terminology']="openehr"
	setting['value']="other care"
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,setting,closestposition))
	nelemn+=1

	#CATEGORY
	path='/'+templateId+'/category'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'category nopathassoc path={path}')
	category={}
	category['code']="433"
	category['value']="event"
	category['terminology']="openehr"
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,category,closestposition))
	nelemn+=1

	#TERRITORY
	path='/'+templateId+'/territory'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'territory nopathassoc path={path}')
	territory={}
#	territory['code']='EU'#EU NOT ACCEPTED!!
	territory['code']='ZW'
	territory['terminology']="ISO_3166-1"
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,territory,closestposition))
	nelemn+=1

	#COMPOSER
	path='/'+templateId+'/composer'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'composer nopathassoc path={path}')
	composer={}
	composer['name']='EOSC-Life_WP1-DEM'
	closestposition=0
	lnewnew=copy.deepcopy(lnew)	
	listofActualLeafs.append(ActualLeaf(lnewnew,composer,closestposition))
	nelemn+=1

	#PRIMARY_DIAGNOSIS
	##primary_diagnosis
	path='/'+templateId+'/patient_data/primary_diagnosis/primary_diagnosis'
	al=fill_in_diagnosis(path,ll,listofleafs)
	listofActualLeafs.append(al)
	##encoding
	path='/'+templateId+'/patient_data/primary_diagnosis/encoding'
	al=fill_in_encoding(path,ll,listofleafs)
	listofActualLeafs.append(al)
	##language
	path='/'+templateId+'/patient_data/primary_diagnosis/language'
	al=fill_in_language(path,ll,listofleafs,defaultLanguage)
	listofActualLeafs.append(al)

	nelemn+=3




	print(f'{nelemn} mapped leafs added')
	logging.info(f'{nelemn} mapped leafs added')



def fix_too_many_missing(idis,idmissing,listis,listmissing,posis,posmissing,listofActualLeafs,listofleafs,pathmissing,defaultLanguage,listofNodes,all_items_patient_i,other_paths=[]):
	from composition.utils import findExactPath
	nelemn=0
	difference=len(listis)-len(listmissing)
	logging.debug(f'idis={idis} idmissing={idmissing} lenis={len(listis)} lenmissing={len(listmissing)}' )
	if(len(listmissing)==0):
		for ll in listis:		
			path=pathmissing
			logging.debug(f'lenis={len(listis)}')
			lnew=findExactPath(listofleafs,path)
			logging.debug(f'{idmissing} from {idis} path={path}')
			value='NULLFLAVOUR'+idmissing
			closestposition=ll.get_positioninXML()
			lnewnew=copy.deepcopy(lnew)	
			lladded=ActualLeaf(lnewnew,value,closestposition,True)
			listofActualLeafs.append(lladded)
			nelemn+=1
			listmissing.append(lladded)
			posmissing.append(closestposition)

			if(other_paths):
				for li in other_paths:
					name=li[0]
					path=li[1]
					if(name=='encoding'):
						al=fill_in_encoding(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='language'):
						al=fill_in_language(path,ll,listofleafs,defaultLanguage)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='test_name'):
						al=fill_in_default(path,ll,listofleafs)			
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='time'):
						shortpath=li[2]
						al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='problem_diagnosis_name'):		
						al=fill_in_diagnosis(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='ism'):
						al=fill_in_ism(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='from_event'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1	
					elif(name=='test_name'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1	
					elif(name=='variant_name'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1	
					elif(name=='therapy'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1							

	else:
		positions=find_position_of_missing_element(difference,posis,posmissing)

		for i in range(0,difference):
			ll=listis[positions[i]]		
			path=pathmissing
			lnew=findExactPath(listofleafs,path)
			logging.debug(f'{idmissing} from {idis} path={path}')
			value='NULLFLAVOUR'+idmissing
			closestposition=ll.get_positioninXML()
			lnewnew=copy.deepcopy(lnew)	
			lladded=ActualLeaf(lnewnew,value,closestposition,True)
			listofActualLeafs.append(lladded)
			nelemn+=1				
			listmissing.append(lladded)
			posmissing.append(closestposition)

			if(other_paths):
				for li in other_paths:
					name=li[0]
					path=li[1]
					if(name=='encoding'):
						al=fill_in_encoding(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='language'):
						al=fill_in_language(path,ll,listofleafs,defaultLanguage)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='test_name'):
						al=fill_in_default(path,ll,listofleafs)			
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='time'):
						shortpath=li[2]
						al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='problem_diagnosis_name'):		
						al=fill_in_diagnosis(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='ism'):
						al=fill_in_ism(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1
					elif(name=='from_event'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)
						nelemn+=1						
					elif(name=='test_name'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1	
					elif(name=='variant_name'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1												
					elif(name=='therapy'):
						al=fill_in_default(path,ll,listofleafs)
						listofActualLeafs.append(al)	
						nelemn+=1							

	return nelemn

def find_position_of_missing_element(difference,pos1,pos2):
	#2 is the missing element 
	#1 is the element coupled with it
	#difference is the number of missing elements so the 
	#number of positions we need
	gaps=[]
	positions=[]
	lenpos2=len(pos2)
#	print(f'pos1={pos1} pos2={pos2}')
	for i,ps in enumerate(pos1):
		for pd in pos2:
			gap=abs(ps-pd)
			gaps.append(gap)
			positions.append(i)
#	print(f'difference={difference}')
#	print(f'pos={positions}')
#	print(f'gaps={gaps}')
	for i in range(0,(int(len(positions)/lenpos2)-difference)):
		min_value=min(gaps)
		min_index=gaps.index(min_value)
		row=int((min_index)/len(pos2))
		positions=positions[0:row*lenpos2]+positions[(row+1)*lenpos2:]
		gaps=gaps[0:row*lenpos2]+gaps[(row+1)*lenpos2:]
#		print(f'pos={positions} gaps={gaps}')
#	print(f'pos={positions}')

	return positions


def pick_from_list(ll,value):
	newvalue={}
	ilist=ll.get_acceptable_values()[0]['list']
	maxlen=0
	for ili in ilist:
		if(ili['label'].upper() in value):
			vlen=len(ili['label'])
			if(vlen>maxlen):
				maxlen=vlen
				newvalue['value']=ili['label']
				newvalue['code']=ili['value']
				newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']

	if (maxlen==0):
		print(f'warning id={ll.get_id()} value {value} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
	return newvalue

def pick_from_list_label(ll,value):
	newvalue=''
	ilist=ll.get_acceptable_values()[0]['list']
	maxlen=0
	for ili in ilist:
		if(ili['label'].upper() in value):
			vlen=len(ili['label'])	
			if(vlen>maxlen):
				maxlen=vlen
				newvalue=ili['label']

	if (maxlen==0):
		print(f'warning id={ll.get_id()} value {value} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
	return newvalue

def pick_from_list_nras(ll,value):
	newvalue={}
	ilist=ll.get_acceptable_values()[0]['list']
	maxlen=0
	for ili in ilist:
		if('label' in ili):
			if(ili['label'].upper() in value):
				vlen=len(ili['label'])	
				if(vlen>maxlen):
					maxlen=vlen
					newvalue['value']=ili['label']
					#for ehrbase
					#newvalue['code']=ili['termBindings']['LOINC']['value']
					#newvalue['terminology']=ili['termBindings']['LOINC']['terminologyId']

					#for marand
					newvalue['code']=ili['value']
					newvalue['terminology']='local'
		else:
			if(ili['localizedLabels']['en'].upper() in value):
				vlen=len(ili['localizedLabels']['en'])	
				if(vlen>maxlen):
					maxlen=vlen				
					newvalue['value']=ili['localizedLabels']['en']

					#for ehrbase
					#newvalue['code']=ili['termBindings']['LOINC']['value']
					#newvalue['terminology']=ili['termBindings']['LOINC']['terminologyId']

					#for marand
					newvalue['code']=ili['value']
					newvalue['terminology']='local'

	if (maxlen==0):
		print(f'warning id={ll.get_id()} value {value} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
	return newvalue

def pick_from_list_morphology(ll,value):
	newvalue={}
	ilist=ll.get_acceptable_values()[0]['list']
	maxlen=0
	for ili in ilist:
		if(ili['label'].upper() in value or  ili['label'].upper() in value.replace('-'," ")):
			vlen=len(ili['label'])	
			if(vlen>maxlen):
				maxlen=vlen	
				newvalue['value']=ili['label']
				newvalue['code']=ili['value']
				newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']

	if (maxlen==0):
		print(f'warning id={ll.get_id()} value {value} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
	return newvalue

def pick_from_list_cut(ll,value_cut,number_of_letters):
	newvalue={}
	ilist=ll.get_acceptable_values()[0]['list']
	for ili in ilist:
		if(ili['label'].upper().lstrip()[0:number_of_letters]==value_cut):
			newvalue['value']=ili['label']
			newvalue['code']=ili['value']
			newvalue['terminology']='local'
	if ('code' not in newvalue):
		print(f'warning id={ll.get_id()} value {value_cut} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value_cut} not found as possiblelabel')
	return newvalue

def pick_from_list_cut_value(ll,value_cut,number_of_letters):
	newvalue='NOT FOUND IN LIST'
	ilist=ll.get_acceptable_values()[0]['list']
	for ili in ilist:
		if(ili['label'].upper().lstrip()[0:number_of_letters]==value_cut):
			newvalue=ili['label']
	if(newvalue=='NOT FOUND IN LIST'):
		print(f'warning id={ll.get_id()} value {value_cut} not found as possible label')
		logging.warning(f'id={ll.get_id()} value {value_cut} not found as possiblelabel')
	return newvalue

def comparestrings(str1,str2):
	if (len(str1) != len(str2)):
		return False
	differences = 0;
	for i,j in zip(str1,str2):
		if(i.isnumeric()):
			continue
		else:
			if(i!=j):
				return False
	return True

def fix_leaf_with_missing_fields_crc(templateId,listofActualLeafs):
	for (indexleaf,ll) in enumerate(listofActualLeafs):
		logging.debug(f'leaf ids third sweep fill missing fields: {ll.get_id()}')
		lid=ll.get_id()
		llpath=ll.get_path()

		if(comparestrings(llpath,'/'+templateId+'/patient_data/gender/biological_sex')):
			#biological_sex from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/therapies/response_to_therapy/clinical_synopsis:0/specific_response')):
			#specific_response from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')				
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/distant_metastasis/anatomical_location:0/localization_of_metastasis')):
			#localization_of_metastasis from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue					
			value=origvalue.upper()
			if(value=='LOCALIZATION OF METASTASIS - PULMONARY'):
				value='LUNG'
			newvalue=pick_from_list(ll,value)
			if(newvalue=={}):
				value='OTHERS'
				newvalue=pick_from_list(ll,value)
				print(f'warning: id={ll.get_id()} value set from {ll.get_data()} to {newvalue} ')
				logging.warning(f'warning: id={ll.get_id()} value set from {ll.get_data()} to {newvalue} ')								
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')			
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/grade')):
			#grade from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue			
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')			
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/distant_metastasis')):
			#distant_metastasis from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/regional_lymph_nodes')):
			#regional_lymph_nodes from DV_TEXT to DV_CODED_TEXT
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/primary_tumour')):
			#primary_tumour
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/localization_of_primary_tumor')):
			#localization_of_primary_tumor
			#part starting with C and add a space
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue
			value=origvalue.rstrip()		
			a=[idx for idx, chr in enumerate(value) if chr=='C']
			if(len(a) != 0):
				#space after C?
				print()
				if( value[a[-1]+1]!=' ' ):
					value_cut=str(value[a[-1]])+' '+value[a[-1]+1:]
				else:
					value_cut=str(value[a[-1]:])
			else:
				print(f'warning id={ll.get_id()} value {value} does not contains code starting with C')
				logging.warning(f'id={ll.get_id()} value {value} does not contains code starting with C')
			newvalue={}
			ilist=ll.get_acceptable_values()[0]['list']
			for ili in ilist:
				if '.' in value_cut:
					if(ili['label'][:6]==value_cut):
						newvalue['value']=ili['label']
						newvalue['code']=ili['value']
						newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']
				else:
					if(ili['label'][:4]==value_cut):
						newvalue['value']=ili['label']
						newvalue['code']=ili['value']
						newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']
			if ('code' not in newvalue):
				print(f'warning id={ll.get_id()} value {value} not found as possible label')
				logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')				
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/material_type')):
			#material_type
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue
			value=origvalue.upper()
			if(value=='OTHER'):
				value='Other specimen type'.upper()
			elif(value=='TUMOR'):
				value='Tumor tissue sample'.upper()
			elif(value=='HEALTHY COLON TISSUE'):
				value='Tissue specimen from colon'.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/stage')):
			#stage
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue}to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/tnm_pathological_classification/uicc_version')):
			#uicc_version
			#take first three characters not null and compare to first three
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue
			value=origvalue.upper()
			number_of_letters=3
			value_cut=value.lstrip()[0:number_of_letters]
			newvalue=pick_from_list_cut_value(ll,value_cut,number_of_letters)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/surgery/surgery:0/surgery_type')):
			#surgery_type			
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue						
			value=origvalue.upper()
			if(value=='LOW ANTEROIR COLON RESECTION'):
				value='Low anterior colon resection'.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/surgery/surgery:0/location_of_the_tumor')):
			#location_of_the_tumor
			#part starting iwth C and add a space
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue			
			if('C20.9' in origvalue):
				value='C20'
			elif('C19.9' in origvalue):
				value='C19'
			else:
				value=origvalue.rstrip()
			a=[idx for idx, chr in enumerate(value) if chr=='C']
			if(len(a) != 0):
				#space after C?
				if( value[a[-1]+1]!=' '  ):
					value_cut=str(value[a[-1]])+' '+value[a[-1]+1:]
				else:
					value_cut=str(value[a[-1]:])
			else:
				print(f'warning id={ll.get_id()} value {value} does not contains code starting with C')
				logging.warning(f'id={ll.get_id()} value {value} does not contains code starting with C')
			newvalue={}
			ilist=ll.get_acceptable_values()[0]['list']
			for ili in ilist:
				if '.' in value_cut:
					if(ili['label'][:6]==value_cut):
						newvalue['value']=ili['label']
						newvalue['code']=ili['value']
						newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']
				else:
					if(ili['label'][:4]==value_cut):
						newvalue['value']=ili['label']
						newvalue['code']=ili['value']
						newvalue['terminology']=ll.get_acceptable_values()[0]['terminology']
			if ('code' not in newvalue):
				print(f'warning id={ll.get_id()} value {value} not found as possible label')
				logging.warning(f'id={ll.get_id()} value {value} not found as possiblelabel')
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')	
		elif(comparestrings(llpath,'/'+templateId+'/surgery/surgery:0/surgery_radicality')):
			#surgery_radicality		
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue						
			value=origvalue.upper()
			newvalue=pick_from_list(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif( ( "nras" in ll.get_id() ) or ("kras" in ll.get_id() ) ):
			#all nras and kras	
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue								
			value=origvalue.upper()
			if(value=='NOT DONE'):
				value='Indeterminate'.upper()
			elif(value=='NOT MUTATED'):
				value="Absent".upper()
			elif(value=='MUTATED'):
				value='Present'.upper()
			newvalue=pick_from_list_nras(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/laboratory_test_result/any_event:0/specimen:0/sample_id')):
			#sample_id
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['id']=origvalue
				ll.set_data(value)
				continue			
			value=origvalue
			newvalue={}
			newvalue['id']=value
			newvalue['issuer']='unknown'
			newvalue['assigner']='unknown'
			newvalue['type']='unknown'
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/morphology')):
			#morphology
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				value={}
				value['value']=origvalue
				ll.set_data(value)
				continue						
			value=origvalue.upper()
			if(value=='MUCINOUS CARCINOMA'):
				value='Mucinous adenocarcinoma'.upper()
			elif(value=='ADEONSQUAMOUS CARCINOMA'):
				value='Adenosquamous carcinoma'.upper()					
			newvalue=pick_from_list_morphology(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')	
		elif(llpath=='/'+templateId+'/context/case_identification/participation_in_clinical_study'):
			#participation_in_clinical_study
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			newvalue=pick_from_list_label(ll,value)
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/histopathology/result_group/cancer_diagnosis/synoptic_details_-_colorectal_cancer/microscopic_findings/histological_grading/who_version')):	
			#who_version
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue
			value=origvalue.upper()[0:3]
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''
			for ili in ilist:
				if(ili['label'].upper()[0:3]==value):
					newvalue=ili['label']
			if(newvalue==''):
				newvalue=ilist[-1]['label']#other
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')			
		elif(comparestrings(llpath,'/'+templateId+'/therapies/pharmacotherapy/medication_management:0/scheme_of_pharmacotherapy')):
			#scheme_of_pharmacotherapy
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue
			value=''
			if('scheme of pharmacotherapy'.upper() in origvalue.upper()):
				value=origvalue.upper()[26:].replace('-','',1).lstrip()
			else:
				value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''		
			for ili in ilist:
				if(ili['label'].upper()==value):
					newvalue=ili['label']
			if(newvalue==''):
				newvalue='NULLFLAVOURscheme'
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')		
		elif(comparestrings(llpath,'/'+templateId+'/diagnostic_examinations/colonoscopy/colonoscopy')):
			#colonoscopy
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''		
			for ili in ilist:
				if(ili['label'].upper() in value):
					newvalue=ili['label']
			if(newvalue==''):
				newvalue=ilist[-1]['label']#Unknown
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/diagnostic_examinations/ct/ct')):
			#ct
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''	
			maxlen=0	
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen	
						newvalue=ili['label']
			if(maxlen==0):
				newvalue=ilist[-1]['label']#Unknown
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/molecular_markers/result_group/oncogenic_mutations_test/any_event:0/braf_pic3ca_her2_mutation_status')):
			#braf_pic3ca_her2_mutation_status
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''		
			maxlen=0
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen	
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/molecular_markers/result_group/microsatellites_instability_analysis/any_event:0/microsatellite_instability')):	
			#microsatellite_instability
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper().replace("_"," ")
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''		
			maxlen=0
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen						
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')							
		elif(comparestrings(llpath,'/'+templateId+'/molecular_markers/result_group/mismatch_repair_gene_analysis/any_event:0/mismatch_repair_gene_expression')):	
			#mismatch_repair_gene_expression
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper().replace("_"," ")
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''		
			maxlen=0
			for ili in ilist:
	#			print(f"ili={ili['label']} value={value}")
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
	#				print(f'vlen={vlen} maxlen={maxlen}')
					if(vlen>maxlen):
						maxlen=vlen								
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')	
		elif(comparestrings(llpath,'/'+templateId+'/vital_status_and_survival_information/vital_status_and_survival_information/vital_status')):	
			#vital_status
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			if('ALIVE' in value):
				newvalue=ilist[3]['label']
			elif('OTHER' in value):
				newvalue=ilist[1]['label']
			elif('COLON' in value):
				newvalue=ilist[0]['label']
			elif('DEATH' in value):
				newvalue=ilist[2]['label']
			elif('UNKNOWN' in value):
				newvalue=ilist[4]['label']
			else:
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue				
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')
		elif(comparestrings(llpath,'/'+templateId+'/molecular_markers/result_group/health_risk_assessment/risk_situation_only_hnpcc')):	
			#risk_situation_only_hnpcc
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			newvalue=''	
			maxlen=0	
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen										
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')							
		elif(comparestrings(llpath,'/'+templateId+'/diagnostic_examinations/liver_imaging/liver_imaging')):
			#liver_imaging
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			maxlen=0	
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen										
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')				
		elif(comparestrings(llpath,'/'+templateId+'/diagnostic_examinations/lung_imaging/lung_imaging')):
			#lung_imaging
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			maxlen=0	
			ilist=ll.get_acceptable_values()[0]['list']
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen										
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')				
		elif(comparestrings(llpath,'/'+templateId+'/diagnostic_examinations/mri/mri')):
			#mri
			origvalue=ll.get_data()
			if('NULLFLAVOUR' in origvalue):
				continue						
			value=origvalue.upper()
			ilist=ll.get_acceptable_values()[0]['list']
			maxlen=0	
			for ili in ilist:
				if(ili['label'].upper() in value):
					vlen=len(ili['label'])	
					if(vlen>maxlen):
						maxlen=vlen										
						newvalue=ili['label']
			if(maxlen==0):
				print(f'warning {ll.get_id()} cannot map {origvalue}')
				logging.warning(f'{ll.get_id()} cannot map {origvalue}')
				newvalue=origvalue
			ll.set_data(newvalue)
			logging.debug(f'fixed {ll.get_id()} from {origvalue} to {newvalue}')				

	#null_flavour round
	#every missing value is started with NULLFLAVOUR
	for ll in listofActualLeafs:
		value=ll.get_data()
		rm=ll.get_rmtype()
		if(rm=='DV_CODED_TEXT'):
			# print(f'DV_CODED rm {rm} {value} {ll.get_path()}')
			if('value' in value):
				if(value['value'].startswith('NULLFLAVOUR')):
					change_to_null_flavour(ll)
			else:
				print(f'warning DV_CODED_TEXT with no "value" label inside value: value={value} path={ll.get_path()}')
				logging.warning(f'warning DV_CODED_TEXT with no value {value} {ll.get_path()}')
		elif(rm=='DV_TEXT'):
			# if(isinstance(value,dict)):
			# 	print(f'dict {value} {ll.get_path()}')
			if(value.startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)
		elif(rm=='CODE_PHRASE'):
			if(value['code'].startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)			
		elif(rm=='DV_IDENTIFIER'):
			if(value['id'].startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)						
		elif(rm=='DV_BOOLEAN'):
			if(value.startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)
		elif(rm=='DV_DATE_TIME'):
			if('NULLFLAVOUR' in value):
				#for ehrbase
				#newvalue=value[11:]
				#ll.set_data(newvalue)
				#al=create_null_flavour(ll)
				#listofActualLeafs.append(al)
				#for marand
				change_to_null_flavour(ll)	
		elif(rm=='DV_DATE'):
			if('NULLFLAVOUR' in value):
				#for ehrbase
				#newvalue=value[11:]
				#ll.set_data(newvalue)
				#al=create_null_flavour(ll)
				#listofActualLeafs.append(al)
				#for marand
				change_to_null_flavour(ll)						
		elif(rm=='DV_DURATION'):
			if('NULLFLAVOUR' in value):
				#for ehrbase
				#newvalue=value[11:]
				#ll.set_data(newvalue)
				#al=create_null_flavour(ll)	
				#listofActualLeafs.append(al)
				#for marand
				change_to_null_flavour(ll)	
		elif(rm=='PARTY_PROXY'):
			if(value['name'].startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)						
		else:
			print(f'rm {rm} {ll.get_path()}')
			if(value.startswith('NULLFLAVOUR')):
				change_to_null_flavour(ll)						

def change_to_null_flavour(ll):
	newpath=ll.get_path()+'/_null_flavour'
	ll.set_path(newpath)
	newvalue={}
#	newvalue['value']='unknown'
	newvalue['code']='253'
#	newvalue['terminology']='openehr'
	ll.setnull(True)
	ll.set_data(newvalue)


def create_null_flavour(ll):
	lnew=copy.deepcopy(ll)
	newpath=lnew.get_path()+'/_null_flavour'
	lnew.set_path(newpath)
	newvalue={}
	newvalue['value']='unknown'
	newvalue['code']='253'
	newvalue['terminology']='openehr'
	pos=ll,get_positioninXML()
	return ActualLeaf(lnew,newvalue,pos,True)

def create_listofnoactualleafs_crc(listofActualLeafs,listofleafs):
	listofNoActualLeafs=[]
	missingleafs=0
	for ll in listofleafs:
		lpath=ll.get_path()

		lid=ll.get_id()

		found=False
		for la in listofActualLeafs:
			aid=la.get_id()
			apath=la.get_path()
			#if(aid=='ism_transition'):
			#	apath=apath[:-14]#cut '/current_state'
			if('_null_flavour' in apath):
				apath=apath[:-14]
			if(lid==aid):
				if(lpath==apath):
					found=True
					logging.debug(f'CREATENOACTUAL FOUND lid={lid} aid={aid} lpath={lpath} apath={apath}')
					break
				else:
					logging.debug(f'CREATENOACTUAL NOTFOUNDlid={lid} aid={aid} lpath={lpath} apath={apath}')
		if(found==False):
			listofNoActualLeafs.append(ll)
			missingleafs+=1

	print(f'Total missing leafs={missingleafs}')
	logging.info(f'Total missing leafs={missingleafs}')

	return listofNoActualLeafs

