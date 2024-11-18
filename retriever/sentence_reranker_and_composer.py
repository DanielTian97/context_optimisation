import pickle
import json
import sys

import pyterrier as pt
from pyterrier_t5 import MonoT5ReRanker, DuoT5ReRanker
import pandas as pd
from sentence_splitter import SentenceSplitter, split_text_into_sentences
from tqdm import tqdm

def warningfree_concat(df1, df2):
    return (df1.copy() if df2.empty else df2.copy() if df1.empty else pd.concat([df1, df2]))

def direct_composer(retriever, dataset_name, _k, doc_dict):
    splitter = SentenceSplitter(language='en')
    
    kv_dict = {}
    raw_context_df_content = []
    
    for qid in queries[dataset_name].qid.values:
        qText = res[res.qid==qid]['query'].values[0]
        
        sentence_df_content = []
        kv = 0
        temp_context = ''
        for docno in res[(res.qid==qid)&(res['rank']<_k)].docno.values:
            dText = doc_dict[docno]
            sentences = splitter.split(dText)
            temp_sentence_list = [[qid, qText, f'{docno}_{i}', sentences[i]] for i in range(len(sentences))]
            sentence_df_content += temp_sentence_list
    
            temp_context += dText + ' '
            kv += len(sentences)
    
        # print(kv, len(splitter.split(temp_context)))
        raw_context_df_content.append([qid, f'i_c_{qid}', temp_context[:-1], 0])
        kv_dict.update({qid: kv})
    
    integrated_context_df = pd.DataFrame(raw_context_df_content, columns=['qid', 'docno', 'text', 'rank'])
    integrated_context_df.to_csv(f'./contexts/integrated_context/integrated_contexts_original_{retriever}_{dataset_name}_{_k}.csv', index=False)

    return kv_dict

def build_sentence_corpus_and_retrieve(retriever, dataset_name, _n, doc_dict):
    splitter = SentenceSplitter(language='en')
    monoT5 = MonoT5ReRanker(verbose=False) # loads castorini/monot5-base-msmarco by default
    
    single_gram_sentence_output = pd.DataFrame([], columns=['qid', 'query', 'docno', 'text', 'score', 'rank'])
    
    for qid in tqdm(queries[dataset_name].qid.values):
        qText = res[res.qid==qid]['query'].values[0]
        
        sentence_df_content = []

        for docno in res[(res.qid==qid)&(res['rank']<_n)].docno.values:
            dText = doc_dict[docno]
            sentences = splitter.split(dText)
            temp_sentence_list = [[qid, qText, f'{docno}_{i}', sentences[i]] for i in range(len(sentences))]
            sentence_df_content += temp_sentence_list

        analyse_input = pd.DataFrame(sentence_df_content, columns=['qid', 'query', 'docno', 'text'])
        analyse_output = monoT5.transform(analyse_input)
        analyse_output = analyse_output.sort_values(by=['rank'])
    
        single_gram_sentence_output = pd.concat([single_gram_sentence_output, analyse_output])
    
    single_gram_sentence_output.to_csv(f'./middle_products/sentence_res_{retriever}_{dataset_name}_{_n}.csv', index=False)

def simple_kv_composer(retriever, dataset, _k, _n, kv_dict):
    single_gram_sentence_res = pd.read_csv(f'./middle_products/sentence_res_{retriever}_{dataset_name}_{_n}.csv')
    single_gram_sentence_res.qid = single_gram_sentence_res.qid.astype('str')
    
    raw_context_df_content = []
    
    for qid in queries[dataset_name].qid.values:
        context_source = single_gram_sentence_res[single_gram_sentence_res.qid==qid].head(1*kv_dict[qid])
    
        reconstructed_df = pd.DataFrame([], columns=['qid', 'query', 'docno', 'text', 'score', 'rank'])
        not_full = True
        temp_context = ''
        for i in range(context_source.shape[0]):
            
            reconstructed_df = warningfree_concat(reconstructed_df, context_source.iloc[i])
            temp_context += (context_source.text.values[i] + ' ')
            pivot_sid = context_source.docno.values[i]
            same_p_dict = {i: pivot_sid.split('_')[1]}
            for j in range(i+1, context_source.shape[0]):
                sid = context_source.docno.values[j]
                if(pivot_sid.split('_')[0] == sid.split('_')[0]):
                    same_p_dict.update({j: sid.split('_')[1]})
            same_p_dict = {k: v for k, v in sorted(same_p_dict.items(), key=lambda item: item[1])}
    
        raw_context_df_content.append([qid, f'i_r_c_{qid}', temp_context, 0])
        
    integrated_context_df = pd.DataFrame(raw_context_df_content, columns=['qid', 'docno', 'text', 'rank'])
    integrated_context_df.to_csv(f'./contexts/integrated_context/integrated_contexts_s-reranked_{retriever}_{dataset_name}_{_k}.csv', index=False)

def position_based_kv_composer(retriever, dataset, _k, _n, kv_dict, alpha):
    single_gram_sentence_res = pd.read_csv(f'./middle_products/sentence_res_{retriever}_{dataset_name}_{_n}.csv')
    single_gram_sentence_res.qid = single_gram_sentence_res.qid.astype('str')
    
    raw_context_df_content = []
    
    for qid in queries[dataset_name].qid.values:
        print(qid, kv_dict[qid])
        context_source = single_gram_sentence_res[single_gram_sentence_res.qid==qid].head(alpha*kv_dict[qid])
    
        collected = []
        reconstructed_df = pd.DataFrame([], columns=['qid', 'query', 'docno', 'text', 'score', 'rank'])
        temp_context_list = []
        not_full = True
        temp_context = ''
        for i in range(context_source.shape[0]):
            print(i)
            if(i in collected):
                continue
                
            pivot_sid = context_source.docno.values[i]
            same_p_dict = {i: pivot_sid.split('_')[1]}
            for j in range(i+1, context_source.shape[0]):
                sid = context_source.docno.values[j]
                if(pivot_sid.split('_')[0] == sid.split('_')[0]):
                    same_p_dict.update({j: sid.split('_')[1]})
            same_p_dict = {k: v for k, v in sorted(same_p_dict.items(), key=lambda item: item[1])}
            temp_context_p = ''
            
            for j in same_p_dict.keys():
                reconstructed_df = warningfree_concat(reconstructed_df, context_source.iloc[j])
                temp_context_p += (context_source.text.values[j] + ' ')
                temp_context += (context_source.text.values[j] + ' ')
                # if(i != j):
                #     print('!!!!!!')
                collected.append(j)
            if(not_full):
                print(collected)
                temp_context_list.append(temp_context_p)
                if(len(collected) >= kv_dict[qid]):
                    not_full = False
        
        raw_context_df_content.append([qid, f'i_r_c_p_{qid}', temp_context, 0])
        
    integrated_context_df = pd.DataFrame(raw_context_df_content, columns=['qid', 'docno', 'text', 'rank'])
    if(alpha==1):
        integrated_context_df.to_csv(f'./contexts/integrated_context/integrated_contexts_s-reranked_position_{retriever}_{dataset_name}_{_k}.csv', index=False)
    else:
        integrated_context_df.to_csv(f'./contexts/integrated_context/integrated_contexts_s-reranked_position-{alpha}_{retriever}_{dataset_name}_{_k}.csv', index=False)
    
if __name__=="__main__":

    retriever = str(sys.argv[1])
    dataset_name = str(sys.argv[2]) # dl_19
    _k = int(sys.argv[3])
    _n = 50
    _alpha = 3
    
    if not pt.java.started():
        pt.java.init()

    dataset_2019 = pt.get_dataset('irds:msmarco-passage/trec-dl-2019/judged')
    queries_2019 = dataset_2019.get_topics()
    
    dataset_2020 = pt.get_dataset('irds:msmarco-passage/trec-dl-2020/judged')
    queries_2020 = dataset_2020.get_topics()
    
    queries = {'dl_19': queries_2019, 'dl_20': queries_2020}

    with open('../../get_res/msmarco_passage_dict.pkl', 'rb') as f:
        doc_dict = pickle.load(f)
        f.close()

    res = pd.read_csv(f'./res/{retriever}_{dataset_name}.csv')
    res.qid = res.qid.astype('str')
    res.docno = res.docno.astype('str')

    kv_dict = direct_composer(retriever, dataset_name, _k, doc_dict)
    build_sentence_corpus_and_retrieve(retriever, dataset_name, _n, doc_dict)

    simple_kv_composer(retriever, dataset_name, _k, _n, kv_dict)
    position_based_kv_composer(retriever, dataset_name, _k, _n, kv_dict, _alpha)
    