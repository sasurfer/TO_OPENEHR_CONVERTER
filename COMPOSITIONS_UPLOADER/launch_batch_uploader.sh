#!/bin/bash
mya1="--inputdir=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/"
mya2="--templatename=mycrc_cohort6mod"
mya3="--check"
mya4="--loglevel=INFO"
myb1="--basename=myoutputceciDB1_"
myb2="--basename=myoutputceciDB2_"
myb3="--basename=myoutputceciDB3_"
myb4="--basename=myoutputceciDB4_"
myb5="--basename=myoutputceciDB5_"
myb6="--basename=myoutputceciDB6_"
myb7="--basename=myoutputceciDB7_"
myb8="--basename=myoutputceciDB8_"
myb9="--basename=myoutputceciDB9_"
myb10="--basename=myoutputceciDB10_"
myb11="--basename=myoutputceciDB11_"
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb1  > uploadingresultsceciDB1
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb2  > uploadingresultsceciDB2
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb3  > uploadingresultsceciDB3
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb4  > uploadingresultsceciDB4
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb5  > uploadingresultsceciDB5
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb6  > uploadingresultsceciDB6
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb7  > uploadingresultsceciDB7
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb8  > uploadingresultsceciDB8
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb9  > uploadingresultsceciDB9
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb10 > uploadingresultsceciDB10
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $myb11 > uploadingresultsceciDB11
