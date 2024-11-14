#!/bin/sh
python ./refinement_test.py bm25 dl_20 original 3
echo 'Finished generation for 3shot for trec-dl-20 o bm25!'
python ./refinement_test.py mt5 dl_20 original 3
echo 'Finished generation for 3shot for trec-dl-20 o mt5!'