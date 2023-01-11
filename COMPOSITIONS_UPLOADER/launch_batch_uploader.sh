#!/bin/bash
mya1="--inputdir=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/"
mya2="--templatename=crc_cohort7"
mya3="--check"
mya4="--loglevel=INFO"
myb1="--basename=myoutput7DB1_"
myb2="--basename=myoutput7DB2_"
myb3="--basename=myoutput7DB3_"
myb4="--basename=myoutput7DB4_"
myb5="--basename=myoutput7DB5_"
myb6="--basename=myoutput7DB6_"
myb7="--basename=myoutput7DB7_"
myb8="--basename=myoutput7DB8_"
myb9="--basename=myoutput7DB9_"
myb10="--basename=myoutput7DB10_"
myb11="--basename=myoutput7DB11_"
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb1  > uploadingresults7DB1
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb2  > uploadingresults7DB2
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb3  > uploadingresults7DB3
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb4  > uploadingresults7DB4
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb5  > uploadingresults7DB5
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb6  > uploadingresults7DB6
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb7  > uploadingresults7DB7
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb8  > uploadingresults7DB8
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb9  > uploadingresults7DB9
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb10 > uploadingresults7DB10
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb11 > uploadingresults7DB11
