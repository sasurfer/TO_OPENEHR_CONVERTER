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

def fill_in_ism(path,shortpath,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'ism transition pathassoc={ll.get_path()} path={path}')
	cstate={}
	cstate["value"]="completed"
	cstate["terminology"]="openehr"
	cstate["code"]="532"
	closestposition=ll.get_positioninXML()
	lnew=findExactPath(listofleafs,shortpath)
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
	return ActualLeaf(lnew,encoding,closestposition)

def fill_in_from_event(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'from event pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	fe=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,fe,closestposition)

def fill_in_language(path,ll,listofleafs,defaultLanguage):
	from composition.utils import findExactPath
	language={}
	language['code']=defaultLanguage
	language['terminology']="ISO_639-1"
	closestposition=ll.get_positioninXML()
	logging.debug(f"language pathassoc={ll.get_path()} path={path} ")
	lnew=findExactPath(listofleafs,path)
	return ActualLeaf(lnew,language,closestposition)

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
	return ActualLeaf(lnew,time,closestposition)	

def fill_in_procedure_name(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'procedure name pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)		
	procedurename=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,procedurename,closestposition)

def fill_in_primary_diagnosis(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'primary diagnosis pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	primd=lnew.get_acceptable_values()[0]["defaultValue"]
	return ActualLeaf(lnew,primd,0)

def fill_in_metastatis_diagnosis(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'metastatis diagnosis pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	metd=lnew.get_acceptable_values()[0]["defaultValue"]
	return ActualLeaf(lnew,metd,0)

def fill_in_test_name(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'test name pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	testname=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,testname,closestposition)

def fill_in_problem_diagnosis_name(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'problem diagnosis name pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	pdn=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,pdn,closestposition)

def fill_in_therapy(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'therapy pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	therapy=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,therapy,closestposition)		

def fill_in_variant_name(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'variant_name pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	vn=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,vn,closestposition)


def fill_in_health_risk(path,ll,listofleafs):
	from composition.utils import findExactPath
	logging.debug(f'health_risk pathassoc={ll.get_path()} path={path}')
	lnew=findExactPath(listofleafs,path)
	hr=lnew.get_acceptable_values()[0]["defaultValue"]
	closestposition=ll.get_positioninXML()
	return ActualLeaf(lnew,hr,closestposition)




def complete_actual_leafs_crc(listofActualLeafs,listofnoleafs,listofNodes,all_items_patient_i,defaultLanguage,listofleafs):
	'''add default values taken from the template or not to the compulsory fields not fillable with the input data'''
	from composition.utils import findExactPath
	nelemn=0

	#add dependent leafs
	for (indexleaf,ll) in enumerate(listofActualLeafs):
		logging.debug(f'leaf ids second sweep DEFAULT ITEMS: {ll.get_id()}')
		lid=ll.get_id()

		if(lid=="surgery_type"):#surgery
			#ism
			path='/crc_cohort/surgery/surgery:0/ism_transition/current_state'
			shortpath='/crc_cohort/surgery/surgery:0/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/crc_cohort/surgery/surgery:0/surgery_timing/surgery:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/surgery/surgery:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)


			#language
			path='/crc_cohort/surgery/surgery:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/surgery/surgery:0/time'
			shortpath='/crc_cohort/surgery/surgery:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="biological_sex"):#gender
			#encoding
			path='/crc_cohort/patient_data/gender/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/patient_data/gender/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			nelemn+=2

		elif(lid=="colonoscopy"):#colonoscopy
			#ism
			path='/crc_cohort/diagnostic_examinations/colonoscopy/ism_transition/current_state'
			shortpath='/crc_cohort/diagnostic_examinations/colonoscopy/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/diagnostic_examinations/colonoscopy/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)


			#language
			path='/crc_cohort/diagnostic_examinations/colonoscopy/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/diagnostic_examinations/colonoscopy/time'
			shortpath='/crc_cohort/diagnostic_examinations/colonoscopy'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			#provedure_name
			path='/crc_cohort/diagnostic_examinations/colonoscopy/procedure_name'
			al=fill_in_procedure_name(path,ll,listofleafs)

			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="age_at_diagnosis"):#primary diagnosis
			#encoding
			path='/crc_cohort/patient_data/primary_diagnosis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/patient_data/primary_diagnosis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#primary_diagnosis
			path='/crc_cohort/patient_data/primary_diagnosis/primary_diagnosis'
			al=fill_in_primary_diagnosis(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=3

		elif(lid=="time_of_recurrence"):#metastasis diagnosis
			#from event
			path='/crc_cohort/patient_data/metastasis_diagnosis/metastasis_diagnosis2/metastasis_diagnosis:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/patient_data/metastasis_diagnosis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/patient_data/metastasis_diagnosis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#metastasis diagnosis
			path='/crc_cohort/patient_data/metastasis_diagnosis/metastasis_diagnosis'
			al=fill_in_metastatis_diagnosis(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="material_type"):#specimen
			#encoding
			path='/crc_cohort/histopathology/result_group/laboratory_test_result/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/histopathology/result_group/laboratory_test_result/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/crc_cohort/histopathology/result_group/laboratory_test_result/any_event:0/test_name'
			al=fill_in_test_name(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/histopathology/result_group/laboratory_test_result/any_event:0/time'
			shortpath='/crc_cohort/histopathology/result_group/laboratory_test_result/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="localization_of_primary_tumor"):#cancer diagnosis
			#encoding
			path='/crc_cohort/histopathology/result_group/cancer_diagnosis/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/histopathology/result_group/cancer_diagnosis/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#problem_diagnosis_name
			path='/crc_cohort/histopathology/result_group/cancer_diagnosis/problem_diagnosis_name'
			al=fill_in_problem_diagnosis_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=3

		elif(lid=="date_of_start_of_radiation_therapy"):#radiation therapy
			#encoding
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from_event
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_start/start_of_radiation_therapy/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#ism
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/ism_transition/current_state'
			shortpath='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#therapy
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/therapy'
			al=fill_in_therapy(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/time'
			shortpath='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=6			

		elif(lid=="date_of_start_of_targeted_therapy"):#targeted_therapy
			#ism
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/ism_transition/current_state'
			shortpath='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/encoding'			
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/targeted_therapy_start/start_of_targeted_therapy/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#therapy
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/therapy'
			al=fill_in_therapy(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/time'
			shortpath='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=6

		elif(lid=="date_of_start_of_pharmacotherapy"):#pharmacotherapy
			#ism
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/ism_transition/current_state'
			shortpath='/crc_cohort/therapies/pharmacotherapy/medication_management:0/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from event
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_start/start_of_pharmacotherapy/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/time'
			shortpath='/crc_cohort/therapies/pharmacotherapy/medication_management:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="specific_response"):#response to therapy
			#encoding
			path='/crc_cohort/therapies/response_to_therapy/clinical_synopsis:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/therapies/response_to_therapy/clinical_synopsis:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			nelemn+=2

		elif(lid=="ct"):#ct
			#ism
			path='/crc_cohort/diagnostic_examinations/ct/ism_transition/current_state'
			shortpath='/crc_cohort/diagnostic_examinations/ct/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)

			#encoding
			path='/crc_cohort/diagnostic_examinations/ct/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/diagnostic_examinations/ct/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/crc_cohort/diagnostic_examinations/ct/procedure_name'
			al=fill_in_procedure_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/diagnostic_examinations/ct/time'
			shortpath='/crc_cohort/diagnostic_examinations/ct'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="liver_imaging"):#ctliver_imaging
			#ism
			path='/crc_cohort/diagnostic_examinations/liver_imaging/ism_transition/current_state'
			shortpath='/crc_cohort/diagnostic_examinations/liver_imaging/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/crc_cohort/diagnostic_examinations/liver_imaging/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/diagnostic_examinations/liver_imaging/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/crc_cohort/diagnostic_examinations/liver_imaging/procedure_name'
			al=fill_in_procedure_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/diagnostic_examinations/liver_imaging/time'
			shortpath='/crc_cohort/diagnostic_examinations/liver_imaging'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="lung_imaging"):#lung_imaging
			#ism
			path='/crc_cohort/diagnostic_examinations/lung_imaging/ism_transition/current_state'
			shortpath='/crc_cohort/diagnostic_examinations/lung_imaging/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/crc_cohort/diagnostic_examinations/lung_imaging/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/diagnostic_examinations/lung_imaging/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/crc_cohort/diagnostic_examinations/lung_imaging/procedure_name'
			al=fill_in_procedure_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/diagnostic_examinations/lung_imaging/time'
			shortpath='/crc_cohort/diagnostic_examinations/lung_imaging'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="mri"):#mri
			#ism
			path='/crc_cohort/diagnostic_examinations/mri/ism_transition/current_state'
			shortpath='/crc_cohort/diagnostic_examinations/mri/ism_transition'
			al=fill_in_ism(path,shortpath,ll,listofleafs)
			listofActualLeafs.append(al)			

			#encoding
			path='/crc_cohort/diagnostic_examinations/mri/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			#language
			path='/crc_cohort/diagnostic_examinations/mri/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#procedure_name
			path='/crc_cohort/diagnostic_examinations/mri/procedure_name'
			al=fill_in_procedure_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/diagnostic_examinations/mri/time'
			shortpath='/crc_cohort/diagnostic_examinations/mri'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="braf_pic3ca_her2_mutation_status"):#oncology_mutations_test
			#encoding
			path='/crc_cohort/molecular_markers/result_group/oncogenic_mutations_test/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)				

			#language
			path='/crc_cohort/molecular_markers/result_group/oncogenic_mutations_test/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/crc_cohort/molecular_markers/result_group/oncogenic_mutations_test/any_event:0/test_name'
			al=fill_in_test_name(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/molecular_markers/result_group/oncogenic_mutations_test/any_event:0/time'
			shortpath='/crc_cohort/molecular_markers/result_group/oncogenic_mutations_test/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="microsatellite_instability"):#microsatellite_instability
			#encoding
			path='/crc_cohort/molecular_markers/result_group/microsatellites_instability_analysis:0/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)				


			#language
			path='/crc_cohort/molecular_markers/result_group/microsatellites_instability_analysis:0/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)


			#test_name
			path='/crc_cohort/molecular_markers/result_group/microsatellites_instability_analysis:0/any_event:0/test_name'
			al=fill_in_test_name(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/molecular_markers/result_group/microsatellites_instability_analysis:0/any_event:0/time'
			shortpath='/crc_cohort/molecular_markers/result_group/microsatellites_instability_analysis:0/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=4

		elif(lid=="nras_exon_4_codons_117_or_146"):#kras mutation
			#encoding
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#test_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/test_name'
			al=fill_in_test_name(path,ll,listofleafs)			
			listofActualLeafs.append(al)

			#time
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/time'
			shortpath='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0'
			al=fill_in_time(path,shortpath,ll,listofNodes,all_items_patient_i,listofleafs)
			listofActualLeafs.append(al)

			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_4_codons_117_or_146/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=5

		elif(lid=="nras_exon_3_codons_59_or_61"):#nras_exon_3_codons_59_or_61
			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_3_codons_59_or_61/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1

		elif(lid=="nras_exon_2_codons_12_or_13"):#nras_exon_2_codons_12_or_13|
			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/nras_exon_2_codons_12_or_13/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_4_codons_117_or_146"):#kras_exon_4_codons_117_or_146
			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_4_codons_117_or_146/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_3_codons_59_or_61"):#kras_exon_3_codons_59_or_61
			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_3_codons_59_or_61/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="kras_exon_2_codons_12_or_13"):#kras_exon_2_codons_12_or_13
			#variant_name
			path='/crc_cohort/molecular_markers/result_group/kras_mutation_status/any_event:0/kras_exon_2_codons_12_or_13/variant_name'
			al=fill_in_variant_name(path,ll,listofleafs)
			listofActualLeafs.append(al)			

			nelemn+=1

		elif(lid=="risk_situation_only_hnpcc"):#health_risk_assessment
			#encoding
			path='/crc_cohort/molecular_markers/result_group/health_risk_assessment/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/molecular_markers/result_group/health_risk_assessment/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			#health_risk
			path='/crc_cohort/molecular_markers/result_group/health_risk_assessment/health_risk'
			al=fill_in_health_risk(path,ll,listofleafs)
			listofActualLeafs.append(al)	

			nelemn+=3		

		elif(lid=="vital_status"):#vital_status_and_survival_information
			#encoding
			path='/crc_cohort/vital_status_and_survival_information/vital_status_and_survival_information/encoding'
			al=fill_in_encoding(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#from_event
			path='/crc_cohort/vital_status_and_survival_information/vital_status_and_survival_information/vital_status_timing/overall_survival_status:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			#language
			path='/crc_cohort/vital_status_and_survival_information/vital_status_and_survival_information/language'
			al=fill_in_language(path,ll,listofleafs,defaultLanguage)
			listofActualLeafs.append(al)

			nelemn+=3

		elif(lid=="date_of_end_of_radiation_therapy"):#end_of_radiation_therapy
			#from_event
			path='/crc_cohort/therapies/radiation_therapy/radiation_therapy:0/radiation_therapy_end/end_of_radiation_therapy:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1

		elif(lid=="date_of_end_of_targeted_therapy"):#end_of_targeted_therapy
			#from_event
			path='/crc_cohort/therapies/targeted_therapy/targeted_therapy:0/targeted_therapy_end/end_of_targeted_therapy:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1			

		elif(lid=="date_of_end_of_pharmacotherapy"):#end_of_pharmacotherapy
			#from_event
			path='/crc_cohort/therapies/pharmacotherapy/medication_management:0/pharmacotherapy_end/end_of_pharmacotherapy/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1						

		elif(lid=="time_of_therapy_response"):#response timing
			#from_event
			path='/crc_cohort/therapies/response_to_therapy/clinical_synopsis:0/response_timing/therapy_response_timestamp:0/from_event'
			al=fill_in_from_event(path,ll,listofleafs)
			listofActualLeafs.append(al)

			nelemn+=1						


	#INDEPENDENT LEAFS
	#COHORT LANGUAGE
	path='/crc_cohort/language'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'language nopathassoc path={path}')
	language={}
	language['code']=defaultLanguage
	language['terminology']="ISO_639-1"
	closestposition=0
	listofActualLeafs.append(ActualLeaf(lnew,language,closestposition))
	nelemn+=1

	#START_TIME
	path='/crc_cohort/context/start_time'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'start_time path nopathassoc path={path}')
	starttime="9999-05-25T15:48:35.35Z"
	closestposition=0
	listofActualLeafs.append(ActualLeaf(lnew,starttime,closestposition))
	nelemn+=1

	#SETTING
	path='/crc_cohort/context/setting'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'setting nopathassoc path={path}')
	setting={}
	setting['code']="238"
	setting['terminology']="openehr"
	setting['value']="other care"
	closestposition=0
	listofActualLeafs.append(ActualLeaf(lnew,setting,closestposition))
	nelemn+=1

	#CATEGORY
	path='/crc_cohort/category'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'category nopathassoc path={path}')
	category={}
	category['code']="433"
	category['value']="event"
	category['terminology']="openehr"
	closestposition=0
	listofActualLeafs.append(ActualLeaf(lnew,category,closestposition))
	nelemn+=1

	#TERRITORY
	path='/crc_cohort/territory'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'territory nopathassoc path={path}')
	territory={}
#	territory['code']='EU'#EU NOT ACCEPTED!!
	territory['code']='ZW'
	territory['terminology']="ISO_3166-1"
	listofActualLeafs.append(ActualLeaf(lnew,territory,closestposition))
	nelemn+=1

	#COMPOSER
	path='/crc_cohort/composer'
	lnew=findExactPath(listofleafs,path)
	logging.debug(f'composer nopathassoc path={path}')
	composer={}
	composer['name']='EOSC-Life_WP1-DEM'
	listofActualLeafs.append(ActualLeaf(lnew,composer,closestposition))
	nelemn+=1

	print(f'{nelemn} mapped leafs added')
	logging.info(f'{nelemn} mapped leafs added')



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
			if(aid=='ism_transition'):
				apath=apath[:-14]#cut "/current_state"
			if(lid==aid):
				if(lpath==apath):
					found=True
					logging.debug(f'CREATENOACTUAL FOUND lid={lid} aid={aid} lpath={lpath} apath={apath}')
					break
				else:
					logging.debug(f'CREATENOACTUAL lid={lid} aid={aid} lpath={lpath} apath={apath}')
		if(found==False):
			listofNoActualLeafs.append(ll)
			missingleafs+=1

	print(f'Total missing leafs={missingleafs}')
	logging.info(f'Total missing leafs={missingleafs}')

	return listofNoActualLeafs



def fill_default_items_crc(ll,listofActualLeafs,listofNodes,defaultLanguage,all_items_patient_i):
	from composition.utils import findclosestActual
	logging.debug(f'DEFTOT id={ll.get_id()} path={ll.get_path()}')
	if(ll.get_id() == "language"):
		logging.debug(f'DEFADD language path={ll.get_path()}')
		language={}
		language['code']=defaultLanguage
		language['terminology']="ISO_639-1"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		logging.debug(f"language {ll.get_path()} ")
		listofActualLeafs.append(ActualLeaf(ll,language,closestposition))
		return True
	elif(ll.get_id() == "encoding"):
		logging.debug(f'DEFADD encoding path={ll.get_path()}')
		encoding={}
		encoding['code']="UTF-8"
		encoding['terminology']="IANA_character-sets"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,encoding,closestposition))
		return True
	elif(ll.get_id()=="composer" and ll.get_path().count('/')==2):
		logging.debug(f'DEFADD composer path={ll.get_path()}')
		composer={}
		composer['name']='EOSC-Life_WP1-DEM'
		listofActualLeafs.append(ActualLeaf(ll,composer,0))
		return True
	elif(ll.get_id()=="territory" and ll.get_path().count('/')==2):
		logging.debug(f'DEFADD territory path={ll.get_path()}')
		#EU NOT ACCEPTED!!
		territory={}
#		territory['code']='EU'
		territory['code']='ZW'
		territory['terminology']="ISO_3166-1"
		listofActualLeafs.append(ActualLeaf(ll,territory,0))
		return True
	elif(ll.get_id()=="category" and ll.get_path().count('/')==2):
		logging.debug(f'DEFADD category path={ll.get_path()}')
		category={}
		category['code']="433"
		category['value']="event"
		category['terminology']="openehr"
		logging.debug(f"CATEGORY {ll.get_path()} {category}")
		listofActualLeafs.append(ActualLeaf(ll,category,0))
		return True
	elif(ll.get_id()=="time"):
		logging.debug(f'DEFADD time path={ll.get_path()}')
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
		logging.debug(f'DEFADD setting path={ll.get_path()}')
		setting={}
		setting['code']="238"
		setting['terminology']="openehr"
		setting['value']="other care"
		listofActualLeafs.append(ActualLeaf(ll,setting,0))
		return True
	elif(ll.get_id()=="from_event"):
		logging.debug(f'DEFADD from event path={ll.get_path()}')
		fe=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,fe,closestposition))
		return True
	elif(ll.get_id()=="primary_diagnosis"):
		logging.debug(f'DEFADD primary diagnosis path={ll.get_path()}')
		primd=ll.get_acceptable_values()[0]["defaultValue"]
		listofActualLeafs.append(ActualLeaf(ll,primd,0))
		return True
	elif(ll.get_id()=="metastasis_diagnosis"):
		logging.debug(f'DEFADD metastasis diagnosis path={ll.get_path()}')
		metd=ll.get_acceptable_values()[0]["defaultValue"]
		listofActualLeafs.append(ActualLeaf(ll,metd,0))
		return True
	elif(ll.get_id()=="test_name"):
		logging.debug(f'DEFADD test name path={ll.get_path()}')
		testname=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,testname,closestposition))
		return True
	elif(ll.get_id()=="procedure_name"):
		logging.debug(f'DEFADD procedure name path={ll.get_path()}')
		procedurename=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,procedurename,closestposition))
		return True			
	elif(ll.get_id()=="therapy"):
		logging.debug(f'DEFADD thearapy path={ll.get_path()}')
		therapy=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,therapy,closestposition))
		return True					
	elif(ll.get_id()=="problem_diagnosis_name"):
		logging.debug(f'DEFADD problem diagnosis name path={ll.get_path()}')
		pdn=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,pdn,closestposition))
		return True			
	elif(ll.get_id()=="variant_name"):
		logging.debug(f'DEFADD variant name path={ll.get_path()}')
		vn=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,vn,closestposition))
		return True
	elif(ll.get_id()=="health_risk"):
		logging.debug(f'DEFADD health risk path={ll.get_path()}')
		hr=ll.get_acceptable_values()[0]["defaultValue"]
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,hr,closestposition))
		return True
#INSTANTIATE AD HOC LEAFS
	elif(ll.get_id()=="ism_transition"):
		logging.debug(f'DEFADD ism transition path={ll.get_path()}')
		if ("current_state" not in ll.path):
			ll.path=ll.path+"/current_state"
		cstate={}
		cstate["value"]="completed"
		cstate["terminology"]="openehr"
		cstate["code"]="532"
		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
		listofActualLeafs.append(ActualLeaf(ll,cstate,closestposition))
		return True
	elif(ll.get_path()=="/crc_cohort/context/start_time"):
		logging.debug(f'DEFADD start_time path={ll.get_path()}')
		starttime="2021-05-25T15:48:35.35Z"
		listofActualLeafs.append(ActualLeaf(ll,starttime,0))
		return True
#	elif(ll.get_id()=="date_of_end_of_radiation_therapy"):
#		dert="P15W"
#		closestposition=findclosestActual(listofActualLeafs,ll.get_path())
#		listofActualLeafs.append(ActualLeaf(ll,dert,closestposition))	
#		return True
	else:
		return False
