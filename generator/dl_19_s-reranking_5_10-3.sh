#!/bin/sh
python ./sentence_reranking_test.py bm25 dl_19 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-rp-3 bm25!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-19 integrated-rp mt5!'
python ./sentence_reranking_test.py bm25 dl_19 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-rp-3 bm25!'
python ./sentence_reranking_test.py mt5 dl_19 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-19 integrated-rp-3 mt5!'