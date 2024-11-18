#!/bin/sh
python ./sentence_reranking_test.py bm25 dl_19 original 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-o bm25!'
python ./sentence_reranking_test.py bm25 dl_19 s-reranked 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-r bm25!'
python ./sentence_reranking_test.py bm25 dl_19 s-reranked_position 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-rp bm25!'
python ./sentence_reranking_test.py mt5 dl_19 original 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-o mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-r mt5!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position 7
echo 'Finished generation for 7shot for trec-dl-19 integrated-rp mt5!'