#!/bin/sh
python ./refinement_test.py bm25 dl_19 original 3
echo 'Finished generation for 3shot for trec-dl-19 o bm25!'
python ./refinement_test.py mt5 dl_19 original 3
echo 'Finished generation for 3shot for trec-dl-19 o mt5!'
