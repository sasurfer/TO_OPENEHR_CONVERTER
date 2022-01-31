#!/usr/bin/python3
'''given an xml output the number of patients that have some events more than one divided by pattern
of occurences of events
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
	logging.basicConfig(filename='./checknumber.log',filemode='w',level=loglevel)

	
	inputfile=args.inputfile
	inputfilebasename=args.inputfilebasename
	inputdir=args.inputdir

	print(inputfilebasename)

	inputfiles=[]
	if(inputfilebasename):
		for file in os.listdir(inputdir):
			if file.startswith(inputfilebasename):
				inputfiles.append(inputdir+'/'+file)
	else:
		inputfiles.append(inputfile)

	print(inputfiles)

#directory=os.path.dirname(os.path.realpath(__file__))
#	outputfile=args.outputfile

	
#	directory=directory+'/RESULTS/'
#	outputfilebasename=directory+outputfile
	#<Dataelement_31_3=CT , Dataelement_30_3=MRI , Dataelement_88_1=colonoscopy, Dataelement_61_5=liver imaging
	#<Dataelement_63_4=lung imaging
	possible_diagnostic_exam=["<Dataelement_31_3",'<Dataelement_30_3', '<Dataelement_88_1','Dataelement_61_5','<Dataelement_63_4']
	possible_events=['<BasicData>','eventtype="Histopathology','eventtype="Sample','eventtype="Surgery"','eventtype="Pharmacotherapy','eventtype="Response to therapy','eventtype="Radiation therapy','eventtype="Targeted Therapy']
	interesting_dataelements=["<Dataelement_81_3",'<Dataelement_59_5']

#	listofDE=[]
#	listofPE=[]
#	listofPEn=[]
#	listofDEn=[]
	for inpf in inputfiles:
		logging.info(f'inputfile={inpf}')
		print(f'inputfile={inpf}')
		with open(inpf) as f:
			for line in f:
				if('eventtype="Pharmacotherapy' in line):
					#reset counters
					mype=[0]*len(possible_events)
					myde=[0]*len(possible_diagnostic_exam)
					found=0

				if('Identifier' in line):
					i1=line.index('>')
					i2=line.index('<',i1)
					identifier=line[i1+1:i2]


				for i,pp in enumerate(interesting_dataelements):
					if pp in line:
						found+=1
						if(found==2):
							print(f'patient {identifier} has both')


				# for i,pe in enumerate(possible_events):
				# 	if pe in line:
				# 		mype[i]+=1
	 
				# for i,de in enumerate(possible_diagnostic_exam):
				# 	if de in line:
				# 		myde[i]+=1
	 

				# if('</BHP' in line):
				# 	if(max(mype)>1):
				# 		if mype in listofPE:
				# 			listofPEn[listofPE.index(mype)]+=1
				# 		else:
				# 			listofPE.append(mype)
				# 			listofPEn.append(1)
				# 		logging.info(f'BHPatient identifier={identifier}')
				# 		logging.info(possible_events)
				# 		logging.info(mype)

				# 	if(max(myde)>1):
				# 		if myde in listofDE:
				# 			listofDEn[listofDE.index(myde)]+=1
				# 		else:
				# 			listofDE.append(myde)
				# 			listofDEn.append(1)
				# 		logging.info(f'BHPatient identifier={identifier}')
				# 		logging.info(possible_diagnostic_exam)
				# 		logging.info(myde)					


# 	logging.info('-------------------------------')
# 	for a,b in zip(listofPE,listofPEn):
# 		print(f'{possible_events} {a} {b}')
# 		logging.info(f'{possible_events} {a} {b}')	

	
# 	a=[0]*len(possible_events)
# 	abin=np.array(a)    
# #	abin="".join(str(x) for x in b)
# 	for i in listofPE:
# 		b=[1 if el>1 else 0 for el in i]
# 		if(i[1]>1):
# 			print(f'histopathology {i}')
# 		bbin=np.array(b)
# #		bbin="".join(str(x) for x in b)
# 		res=abin | bbin
# 		abin=res

# 	print(f'res={abin}')


# 	print('-----------------------------------')
# 	logging.info('-------------------------------')
# 	for a,b in zip(listofDE,listofDEn):
# 		print(f'{possible_diagnostic_exam} {a} {b}')
# 		logging.info(f'{possible_diagnostic_exam} {a} {b}')		



if __name__ == '__main__':
	main()
