#!/bin/sh
python refined_passages_composer.py bm25 dl_110 10
python refined_passages_composer.py bm25 dl_20 10
python refined_passages_composer.py mt5 dl_110 10
python refined_passages_composer.py mt5 dl_20 10

python sentence_reranker_and_composer.py bm25 dl_110 10
python sentence_reranker_and_composer.py bm25 dl_20 10
python sentence_reranker_and_composer.py mt5 dl_110 10
python sentence_reranker_and_composer.py mt5 dl_20 10