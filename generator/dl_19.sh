#!/bin/sh
python ./refinement_test.py bm25 dl_19 original 3
echo 'Finished generation for 3shot for trec-dl-19 o bm25!'
python ./refinement_test.py bm25 dl_19 modified 3
echo 'Finished generation for 3shot for trec-dl-19 m bm25!'
python ./refinement_test.py bm25 dl_19 reranked_modified 3
echo 'Finished generation for 3shot for trec-dl-19 rm bm25!'
python ./refinement_test.py mt5 dl_19 original 3
echo 'Finished generation for 3shot for trec-dl-19 o mt5!'
python ./refinement_test.py mt5 dl_19 modified 3
echo 'Finished generation for 3shot for trec-dl-19 m mt5!'
python ./refinement_test.py mt5 dl_19 reranked_modified 3
echo 'Finished generation for 3shot for trec-dl-19 rm mt5!'

python ./refinement_test.py bm25 dl_19 original 5
echo 'Finished generation for 5shot for trec-dl-19 o bm25!'
python ./refinement_test.py bm25 dl_19 modified 5
echo 'Finished generation for 5shot for trec-dl-19 m bm25!'
python ./refinement_test.py bm25 dl_19 reranked_modified 5
echo 'Finished generation for 5shot for trec-dl-19 rm bm25!'
python ./refinement_test.py mt5 dl_19 original 5
echo 'Finished generation for 5shot for trec-dl-19 o mt5!'
python ./refinement_test.py mt5 dl_19 modified 5
echo 'Finished generation for 5shot for trec-dl-19 m mt5!'
python ./refinement_test.py mt5 dl_19 reranked_modified 5
echo 'Finished generation for 5shot for trec-dl-19 rm mt5!'

python ./refinement_test.py bm25 dl_19 original 7
echo 'Finished generation for 7shot for trec-dl-19 o bm25!'
python ./refinement_test.py bm25 dl_19 modified 7
echo 'Finished generation for 7shot for trec-dl-19 m bm25!'
python ./refinement_test.py bm25 dl_19 reranked_modified 7
echo 'Finished generation for 7shot for trec-dl-19 rm bm25!'
python ./refinement_test.py mt5 dl_19 original 7
echo 'Finished generation for 7shot for trec-dl-19 o mt5!'
python ./refinement_test.py mt5 dl_19 modified 7
echo 'Finished generation for 7shot for trec-dl-19 m mt5!'
python ./refinement_test.py mt5 dl_19 reranked_modified 7
echo 'Finished generation for 7shot for trec-dl-19 rm mt5!'

python ./refinement_test.py bm25 dl_19 original 10
echo 'Finished generation for 10shot for trec-dl-19 o bm25!'
python ./refinement_test.py bm25 dl_19 modified 10
echo 'Finished generation for 10shot for trec-dl-19 m bm25!'
python ./refinement_test.py bm25 dl_19 reranked_modified 10
echo 'Finished generation for 10shot for trec-dl-19 rm bm25!'
python ./refinement_test.py mt5 dl_19 original 10
echo 'Finished generation for 10shot for trec-dl-19 o mt5!'
python ./refinement_test.py mt5 dl_19 modified 10
echo 'Finished generation for 10shot for trec-dl-19 m mt5!'
python ./refinement_test.py mt5 dl_19 reranked_modified 10
echo 'Finished generation for 10shot for trec-dl-19 rm mt5!'