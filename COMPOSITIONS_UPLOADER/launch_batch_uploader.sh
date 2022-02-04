#!/bin/bash
mya1="--inputdir=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/"
mya2="--templatename=mycrc_cohort6mod"
mya3="--check"
mya4="--loglevel=INFO"
mya5="--basename=myoutputceciDB5_"
mya6="--basename=myoutputceciDB6_"
mya7="--basename=myoutputceciDB7_"
mya8="--basename=myoutputceciDB8_"
mya9="--basename=myoutputceciDB9_"
mya10="--basename=myoutputceciDB10_"
mya11="--basename=myoutputceciDB11_"
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya5  > uploadingresultsceciDB5
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya6  > uploadingresultsceciDB6
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya7  > uploadingresultsceciDB7
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya8  > uploadingresultsceciDB8
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya9  > uploadingresultsceciDB9
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya10_ > uploadingresultsceciDB10
python3 ./CompositionUploader.py $mya1 $mya2 $mya3 $mya4 $mya11_ > uploadingresultsceciDB11
