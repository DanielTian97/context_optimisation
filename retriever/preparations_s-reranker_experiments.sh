#!/bin/sh
python sentence_reranker_and_composer.py bm25 dl_19 3
python sentence_reranker_and_composer.py bm25 dl_20 3
python sentence_reranker_and_composer.py mt5 dl_19 3
python sentence_reranker_and_composer.py mt5 dl_20 3

python sentence_reranker_and_composer.py bm25 dl_19 5
python sentence_reranker_and_composer.py bm25 dl_20 5
python sentence_reranker_and_composer.py mt5 dl_19 5
python sentence_reranker_and_composer.py mt5 dl_20 5

python sentence_reranker_and_composer.py bm25 dl_19 7
python sentence_reranker_and_composer.py bm25 dl_20 7
python sentence_reranker_and_composer.py mt5 dl_19 7
python sentence_reranker_and_composer.py mt5 dl_20 7

python sentence_reranker_and_composer.py bm25 dl_19 10
python sentence_reranker_and_composer.py bm25 dl_20 10
python sentence_reranker_and_composer.py mt5 dl_19 10
python sentence_reranker_and_composer.py mt5 dl_20 10