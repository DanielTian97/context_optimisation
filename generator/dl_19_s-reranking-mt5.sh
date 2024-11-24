#!/bin/sh
python ./sentence_reranking_test.py mt5 dl_19 original 3
echo 'Finished generation for 3shot for trec-dl-19 integrated-o mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked 3
echo 'Finished generation for 3shot for trec-dl-19 integrated-r mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position 3
echo 'Finished generation for 3shot for trec-dl-19 integrated-rp mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-1 3
echo 'Finished generation for 3shot for trec-dl-19 integrated-rp-1 mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 3
echo 'Finished generation for 3shot for trec-dl-19 integrated-rp-3 mt5!'

python ./sentence_reranking_test.py mt5 dl_19 original 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-o mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-r mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-rp mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-1 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-rp-1 mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-rp-3 mt5!'

python ./sentence_reranking_test.py mt5 dl_19 original 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-o mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-r mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-rp mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-1 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-rp-1 mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-rp-3 mt5!'

python ./sentence_reranking_test.py mt5 dl_19 original 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-o mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-r mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-rp mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-1 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-rp-1 mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-rp-3 mt5!'