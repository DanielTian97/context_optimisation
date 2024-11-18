#!/bin/sh
python ./refinement_test.py bm25 dl_20 original 7
echo 'Finished generation for 7shot for trec-dl-20 o bm25!'
python ./refinement_test.py bm25 dl_20 modified 7
echo 'Finished generation for 7shot for trec-dl-20 m bm25!'
python ./refinement_test.py bm25 dl_20 reranked_modified 7
echo 'Finished generation for 7shot for trec-dl-20 rm bm25!'
python ./refinement_test.py mt5 dl_20 original 7
echo 'Finished generation for 7shot for trec-dl-20 o mt5!'
python ./refinement_test.py mt5 dl_20 modified 7
echo 'Finished generation for 7shot for trec-dl-20 m mt5!'
python ./refinement_test.py mt5 dl_20 reranked_modified 7
echo 'Finished generation for 7shot for trec-dl-20 rm mt5!'