#!/bin/sh
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-rp-3 bm25!'
python ./sentence_reranking_test.py mt5 dl_20 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-rp mt5!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-rp-3 bm25!'
python ./sentence_reranking_test.py mt5 dl_20 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-rp-3 mt5!'