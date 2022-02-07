# TO_OPENEHR_CONVERTER
Convert from BBMRI XML to OpenEHR template by @fra and @ceci
current template version mycrc_cohort6mod

For ehrbase (0.18.3-0.19) use flag --ehrbase
For earlier version there's a problem with null_flavour not supported.
For Marand simply omit the flag --ehrbase


Use example for ehrbase:
python3 main.py --loglevel=INFO --inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_8.xml --webtemplate=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/TEST/NEWTEMPLATE/mycrc_cohort6mod.json --outputfilebasename=myoutputceciDB8 --check --ehrbase 
