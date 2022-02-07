#!/bin/bash
mya1="--webtemplate=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/TEST/NEWTEMPLATE/mycrc_cohort6mod.json"
mya2="--ehrbase"
mya3="--check"
mya4="--loglevel=INFO"
myb1="--outputfilebasename=myoutputceciDB1"
myb2="--outputfilebasename=myoutputceciDB2"
myb3="--outputfilebasename=myoutputceciDB3"
myb4="--outputfilebasename=myoutputceciDB4"
myb5="--outputfilebasename=myoutputceciDB5"
myb6="--outputfilebasename=myoutputceciDB6"
myb7="--outputfilebasename=myoutputceciDB7"
myb8="--outputfilebasename=myoutputceciDB8"
myb9="--outputfilebasename=myoutputceciDB9"
myb10="--outputfilebasename=myoutputceciDB10"
myb11="--outputfilebasename=myoutputceciDB11"
myc1="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_1.xml"
myc2="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_2.xml"
myc3="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_3.xml"
myc4="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_4.xml"
myc5="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_5.xml"
myc6="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_6.xml"
myc7="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_7.xml"
myc8="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_8.xml"
myc9="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_9.xml"
myc10="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_10.xml"
myc11="--inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_11.xml"
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb1 $myc1 > conversion.screen.ceciDB1
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb2 $myc2 > conversion.screen.ceciDB2
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb3 $myc3 > conversion.screen.ceciDB3
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb4 $myc4 > conversion.screen.ceciDB4
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb5 $myc5 > conversion.screen.ceciDB5
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb6 $myc6 > conversion.screen.ceciDB6
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb7 $myc7 > conversion.screen.ceciDB7
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb8 $myc8 > conversion.screen.ceciDB8
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb9 $myc9 > conversion.screen.ceciDB9
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb10 $myc10> conversion.screen.ceciDB10
python3 ./main.py $mya1 $mya2 $mya3 $mya4 $myb11 $myc11> conversion.screen.ceciDB11
