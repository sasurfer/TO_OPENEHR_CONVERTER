#Starting from two groups of compositions 
#find the pair (one for each group) that refer to the same patient
#compare them
#ignore if given, the errors to ignore
#Example of a run:
#python3 CreateListofCompositionsPairsandCompare.py --dir1=TMP1 --dir2=TMP2 --basecomp1=myoutput7AQCDB --basecomp2=BBPatientDB --errors_to_ignore='{"replace":"/bmri-eric_colorectal_cancer_cohort_report/context/start_time","add":"/bbmri-eric_colorectal_cancer_cohort_report/context/biobank/case_identification/biobank_patient_identifier"}'
# show the remaining errors
from typing import Any,Callable
import re
import json
from json_tools import diff
import argparse
import logging
import collections
import pathlib



def getfiledictlist(dir,basecomp):
    '''
    input: directory, basefile for compositions
    output: json with key=patient_id value=filename
    '''
    filedictlist={}
    p=pathlib.Path(dir)
    for f in p.glob(basecomp+"*.json"):
        patientid=str(f).split(".json")[0].split("_")[-1]
        filedictlist[patientid]=f
    logging.info(f'Found {len(filedictlist)} compositions in dir {dir}')
    return filedictlist


def compare(firstjson:json,secondjson:json,errors_to_ignore:json)->json:
    '''
    compare the given jsons
    '''
    one=flatten(firstjson)
    two=flatten(secondjson)
    results=diff(one,two)
    newresults=[]
    for elem in results:
        logging.debug(elem)
        found=False
        ignore=False
        for keye in elem:
            logging.debug(keye)
            if keye in errors_to_ignore:
                found=True
                logging.debug('found')
                logging.debug(errors_to_ignore[keye])
                logging.debug(elem[keye])
                if errors_to_ignore[keye]==elem[keye]:
                    ignore=True
                    logging.debug('ignore')
                
        if found and ignore:
            continue

        newresults.append(elem)

    return newresults
#    return json.dumps((diff(one,two)),indent=4)

def readjson(filename:str)->json:
    '''read in the json file'''
    with open(filename,'r') as f:
        newjson = json.load(f)	
    return newjson

def change_naming(myjson:json)->json:
    '''change naming convention on the json'''
    return change_dict_naming_convention(myjson,convertcase)


def flatten(d:dict, parent_key:str='', sep:str='_')->dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def change_dict_naming_convention(d:Any, convert_function:Callable[[str],str])->dict:
    """
    Convert a nested dictionary from one convention to another.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    """
    if not isinstance(d,dict):
        return d
    new = {}
    for k, v in d.items():
        new_v = v
        if isinstance(v, dict):
            new_v = change_dict_naming_convention(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(change_dict_naming_convention(x, convert_function))
        new[convert_function(k)] = new_v
    return new

def convertcase(name:str)->str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def main():
    parser = argparse.ArgumentParser(description="Compare two sets of compositions")
    parser.add_argument("--dir1",help="first directory with compositions",required=True)
    parser.add_argument("--dir2",help="second directory with compositions",required=True)
    parser.add_argument("--basecomp1",help="basename used for compositions in dir1",required=True)
    parser.add_argument("--basecomp2",help="basename() used for compositions in dir2",required=True)
    parser.add_argument("--errors_to_ignore",help="dictionary with errors to ignore")
    parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='INFO')
    parser.add_argument("--outputfile",help="output file",default="CompareJsonFilesInDirs.log")

    args=parser.parse_args()
    
    dir1=args.dir1
    dir2=args.dir2
    basecomp1=args.basecomp1
    basecomp2=args.basecomp2
    errors_to_ignore=args.errors_to_ignore
    if errors_to_ignore is not None:
        print(f'errors_to_ignore={errors_to_ignore}')
        errors_to_ignore=json.loads(errors_to_ignore)
    else:
        errors_to_ignore={}
    
    outputfile=args.outputfile

    loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
    if not isinstance(loglevel, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename=outputfile,filemode='w',level=loglevel)


    #retrieve all files in dir starting with basename. Results {patient_id_1:pathtofilename1,patient_id_2:pathtofilename2,..]
    files_dir1=getfiledictlist(dir1,basecomp1)
    files_dir2=getfiledictlist(dir2,basecomp2)

    #iter through all the patient_ids
    for patientid in files_dir1:
        logging.info(f'---------patientid={patientid}-----------')               
        filename1=files_dir1[patientid]
        logging.info(f'filename1: {filename1}') 
        if patientid not in files_dir2:
            logging.info(f'patientid={patientid} not in {dir2}')
            continue
        filename2=files_dir2[patientid]
        logging.info(f'filename2: {filename2}')

        firstjson=readjson(filename1)
        secondjson=readjson(filename2)

        firstchanged=change_naming(firstjson)
        secondchanged=change_naming(secondjson)

        results=compare(firstchanged,secondchanged,errors_to_ignore)

        if results != []:
            print(f'----patientid={patientid} differences exist----')
            print(f'filename1= {filename1} filename2= {filename2}')

        logging.info('Differences:')
        logging.info(results)
    print(f'FINISHED')
    

if __name__ == '__main__':
    main()
