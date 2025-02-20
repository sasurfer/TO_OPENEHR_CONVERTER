# TO_OPENEHR_CONVERTER
Convert from BBMRI XML to OpenEHR template by @fra and @ceci
(current template version mycrc_cohort7)

For ehrbase (0.18.3-0.19) use flag --ehrbase
For earlier version there's a problem with null_flavour not supported.
For Marand simply omit the flag --ehrbase

Flags in brief:
loglevel=set level for the log file conversion.log
inputfile=xml input file
webtemplate=template for the flat format composition
outputfilebasename=basename for the flat composition(s) created
check=check the leafs created and warn if some compulsory ones are missing
ehrbase=flag to be used with ehrbase. In some input files one or more therapies exist but response_to_therapy is missing. EHRBase do not work on these so with the flag we add a complete null flavour response.

Use example for ehrbase:
python3 main.py --loglevel=INFO --inputfile=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/FROM_DB_CSV_TO_XML_CONVERTER/patientsFromDb_8.xml --webtemplate=/usr/local/data/WORK/OPENEHR/ECOSYSTEM/TO_AND_FROM_CONVERTER/CODE/RESULTS/TEST/NEWTEMPLATE/mycrc_cohort6mod.json --outputfilebasename=myoutputceciDB8 --check --ehrbase 

# Acknowledgments
This work has been partially funded by the following sources:
<ul>
<li> the EOSC-Life European project (H2020, grant agreement N. 824087), within the EOSC-Life WP1 Demonstrator “Cloudification of BBMRI-ERIC CRC-Cohort and its Digital Pathology Imaging” (APPID 1228)<\li>
<li> the “Processing, Analysis, Exploration, and Sharing of Big and/or Complex Data” (XDATA) project (grant by the Sardinian Regional Authority)</li>
</ul>
