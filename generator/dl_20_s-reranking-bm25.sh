#!/bin/sh
python ./sentence_reranking_test.py bm25 dl_20 original 3
echo 'Finished generation for 3shot for trec-dl-20 integrated-o bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked 3
echo 'Finished generation for 3shot for trec-dl-20 integrated-r bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position 3
echo 'Finished generation for 3shot for trec-dl-20 integrated-rp-full bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-1 3
echo 'Finished generation for 3shot for trec-dl-20 integrated-rp-1 bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 3
echo 'Finished generation for 3shot for trec-dl-20 integrated-rp-3 bm25!'

python ./sentence_reranking_test.py bm25 dl_20 original 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-o bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-r bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-rp-full bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-1 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-rp-1 bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 5
echo 'Finished generation for 5shot for trec-dl-20 integrated-rp-3 bm25!'

python ./sentence_reranking_test.py bm25 dl_20 original 7
echo 'Finished generation for 7shot for trec-dl-20 integrated-o bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked 7
echo 'Finished generation for 7shot for trec-dl-20 integrated-r bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position 7
echo 'Finished generation for 7shot for trec-dl-20 integrated-rp-full bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-1 7
echo 'Finished generation for 7shot for trec-dl-20 integrated-rp-1 bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 7
echo 'Finished generation for 7shot for trec-dl-20 integrated-rp-3 bm25!'

python ./sentence_reranking_test.py bm25 dl_20 original 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-o bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-r bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-rp-full bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-1 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-rp-1 bm25!'
python ./sentence_reranking_test.py bm25 dl_20 s-reranked_position-3 10
echo 'Finished generation for 10shot for trec-dl-20 integrated-rp-3 bm25!'