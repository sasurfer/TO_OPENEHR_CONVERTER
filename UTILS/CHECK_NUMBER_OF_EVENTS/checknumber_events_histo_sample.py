#!/usr/bin/python3
'''given an xml output the patient names that have more than one histopathology and more than one sample
'''
import argparse,logging,os
import numpy as np

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--loglevel',help='the logging level:DEBUG,INFO,WARNING,ERROR or CRITICAL',default='INFO')
	parser.add_argument('--inputfile',help='input filename',default='input')
	parser.add_argument('--inputfilebasename',help='input filebasename')
	parser.add_argument('--inputdir',help='input directory',default='.')
#	parser.add_argument('--outputfile',help='output file',default='output')
	args=parser.parse_args()


	loglevel=getattr(logging, args.loglevel.upper(),logging.WARNING)
	if not isinstance(loglevel, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	logging.basicConfig(filename='./checknumber_histo_sample.log',filemode='w',level=loglevel)

	
	inputfile=args.inputfile
	inputfilebasename=args.inputfilebasename
	inputdir=args.inputdir

	print(inputfilebasename)

	inputfiles=[]
	if(inputfilebasename):
		for file in os.listdir(inputdir):
			if file.startswith(inputfilebasename):
				inputfiles.append(inputdir+file)
	else:
		inputfiles.append(inputfile)

	print(inputfiles)

#directory=os.path.dirname(os.path.realpath(__file__))
#	outputfile=args.outputfile

	
#	directory=directory+'/RESULTS/'
#	outputfilebasename=directory+outputfile
	#<Dataelement_31_3=CT , Dataelement_30_3=MRI , Dataelement_88_1=colonoscopy, Dataelement_61_5=liver imaging
	#<Dataelement_63_4=lung imaging
#	possible_diagnostic_exam=["<Dataelement_31_3",'<Dataelement_30_3', '<Dataelement_88_1','Dataelement_61_5','<Dataelement_63_4']
#	possible_events=['<BasicData>','eventtype="Histopathology','eventtype="Sample','eventtype="Surgery"','eventtype="Pharmacotherapy','eventtype="Response to therapy','eventtype="Radiation therapy','eventtype="Targeted Therapy']
	p_e=['eventtype="Histopathology','eventtype="Sample']


	nevents=0
	for inpf in inputfiles:
		logging.info(f'inputfile={inpf}')
		print(f'inputfile={inpf}')
		with open(inpf) as f:
			for line in f:
				if('<BHP' in line):
					#reset counters
					mype=[0]*len(p_e)
					histo=[]
					sample=[]

				if('Identifier' in line):
					i1=line.index('>')
					i2=line.index('<',i1)
					identifier=line[i1+1:i2]


				for i,pe in enumerate(p_e):
					if pe in line:
						mype[i]+=1
						if(p_e[0] in line):#histo
							histo.append(line)
						else:#sample
	 						sample.append(line)

				if('</BHP' in line):
					if(min(mype)>1):
						logging.info(f'-------------------------------')
						logging.info(f'BHPatient identifier={identifier}')
						logging.info(f'p_e_{p_e}')
						logging.info(f'events {mype}')
						logging.info(f'histo: {histo}\n')
						logging.info(f'sample: {sample}')
						nevents+=1


	logging.info(f'Number of patients with histo>1 and sample>1 {nevents}')
	print(f'Number of patients with histo>1 and sample>1 {nevents}')



if __name__ == '__main__':
	main()
