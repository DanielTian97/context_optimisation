import sys
import pickle
import pandas as pd
import json

import pyterrier as pt
import pickle

from sentence_splitter import SentenceSplitter, split_text_into_sentences

def sentence_assembler(sentences: list, indices: list):
    output = ''
    for i in indices:
        output += (sentences[i] + ' ')
    return output[:-1]

def sentence_assembler_all_pass(sentences: list):
    output = ''
    for s in sentences:
        output += (s + ' ')
    return output[:-1]

def res_loader(retriever, dataset_name):
    res = pd.read_csv(f'./res/{retriever}_{dataset_name}.csv')
    res.qid = res.qid.astype('str')
    res.docno = res.docno.astype('str')
    return res

def unrefined_top_k_composer(retriever, dataset_name, _k):
    splitter = SentenceSplitter(language='en')

    res = res_loader(retriever, dataset_name)

    original_length_list = {}
    original_text_list = {}
    content = []

    for qid in queries[dataset_name].qid.values:
        top_k_docno_for_q = res[(res.qid == qid) & (res['rank'] < _k)].sort_values(by=['rank']).docno.values
        top_k_texts_for_q = [doc_dict[x] for x in top_k_docno_for_q]
        num_s = sum([len(splitter.split(text=t)) for t in top_k_texts_for_q])
        reconstructed_top_k = [sentence_assembler_all_pass(splitter.split(text=t)) for t in top_k_texts_for_q]
        original_length_list.update({qid: num_s})
        original_text_list.update({qid: reconstructed_top_k})
    
        # save results:
        for i in range(len(top_k_docno_for_q)):
            content.append([qid, f'o_{top_k_docno_for_q[i]}', reconstructed_top_k[i], i])
    
    original_context_df = pd.DataFrame(content, columns=['qid', 'docno', 'text', 'rank'])
    original_context_df.to_csv(f'./contexts/refined_context/original_contexts_{retriever}_{dataset_name}_{_k}.csv', index=False)

def refined_top_k_composer(retriever, dataset_name, _k, refined_doc_dict):
    splitter = SentenceSplitter(language='en')

    res = res_loader(retriever, dataset_name)

    refined_length_list = {}
    refined_text_list = {}
    content = []
    
    for qid in queries[dataset_name].qid.values:
        top_k_docno_for_q = res[(res.qid == qid) & (res['rank'] < _k)].sort_values(by=['rank']).docno.values
        top_k_texts_for_q = [refined_doc_dict[qid][x]['text'] for x in top_k_docno_for_q]
        num_s = sum([len(splitter.split(text=t)) for t in top_k_texts_for_q])
        refined_length_list.update({qid: num_s})
        refined_text_list.update({qid: top_k_texts_for_q})
        
        # save results:
        for i in range(len(top_k_docno_for_q)):
            content.append([qid, f'm_{top_k_docno_for_q[i]}', top_k_texts_for_q[i], i])
    
    modified_context_df = pd.DataFrame(content, columns=['qid', 'docno', 'text', 'rank'])
    modified_context_df.to_csv(f'./contexts/refined_context/modified_contexts_{retriever}_{dataset_name}_{_k}.csv', index=False)

def reranked_refined_top_k_composer(retriever, dataset_name, _k, refined_doc_dict):
    splitter = SentenceSplitter(language='en')
    
    reordered_refined_length_list = {}
    reordered_refined_text_list = {}
    content = []
    
    for qid in queries[dataset_name].qid.values:
        top_k_texts_for_q = refined_doc_dict[qid]
        temp_df_content = []
        for item in top_k_texts_for_q.items():
            temp_df_content.append([item[0], item[1]['text'], item[1]['rel']])
    
        temp_df = pd.DataFrame(temp_df_content, columns=['pid', 'text', 'score']).sort_values(by=['score'], ascending=False)

        top_k_docno_for_q = temp_df.head(_k).pid.values.tolist()
        top_k_texts_for_q = temp_df.head(_k).text.values.tolist()
        num_s = sum([len(splitter.split(text=t)) for t in top_k_texts_for_q])
        reordered_refined_length_list.update({qid: num_s})
        reordered_refined_text_list.update({qid: top_k_texts_for_q})
    
        for i in range(min(len(top_k_docno_for_q), _k)):
            content.append([qid, f'rm_{top_k_docno_for_q[i]}', top_k_texts_for_q[i], i])
    
    reranked_modified_context_df = pd.DataFrame(content, columns=['qid', 'docno', 'text', 'rank'])
    reranked_modified_context_df.to_csv(f'./contexts/refined_context/reranked_modified_contexts_{retriever}_{dataset_name}_{_k}.csv', index=False)
    
if __name__=="__main__":
    retriever = str(sys.argv[1])
    dataset_name = str(sys.argv[2]) # dl_19
    _k = int(sys.argv[3])
    _n = 20

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

    with open(f'./refined_passages/refined_dict_{retriever}_{dataset_name}_top-{_n}.json', 'r') as f:
        refined_doc_dict = json.load(f)
        f.close()

    unrefined_top_k_composer(retriever, dataset_name, _k)
    refined_top_k_composer(retriever, dataset_name, _k, refined_doc_dict)
    reranked_refined_top_k_composer(retriever, dataset_name, _k, refined_doc_dict)
