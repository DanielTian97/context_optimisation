import pandas as pd
from tqdm import tqdm
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import pickle
import json
import sys
import pyterrier as pt

def sentence_assembler(sentences: list, indices: list):
    output = ''
    for i in indices:
        output += (sentences[i] + ' ')
    return output[:-1]

def trimming_passage(res_df, target_qid, target_qtext, splitter, judger, doc_dict, convert_doc_num:int):

    trimmed_passage_dict = {}
    
    for selected_no in range(min(res_df[res_df.qid==target_qid].shape[0], convert_doc_num)):
        pid = res_df[res_df.qid==target_qid].docno.values[selected_no]
        original_passage = doc_dict[pid]
        
        sentences = splitter.split(text=original_passage)
        
        sentences_analysis_input_content = [[target_qid, target_qtext, f's', original_passage]]
        for i in range(len(sentences)):
            sentences_analysis_input_content.append([target_qid, target_qtext, f's_{i}', sentences[i]])
        
        # Having analysed the sentences, filtering out the sentences that are non-relevant
        sentence_for_comparison = sentence_assembler(sentences, list(range(len(sentences))))
        original_passage = sentence_for_comparison
        
        o_start = 0
        for k in range(len(sentences)-1):
            to_check = sentence_assembler(sentences, list(range(k+1, len(sentences))))
            to_check_df_content = []
            to_check_df_content.append([target_qid, target_qtext, f'c_s_0', sentence_for_comparison])
            to_check_df_content.append([target_qid, target_qtext, f'c_s_1', to_check])
            to_check_input = pd.DataFrame(to_check_df_content, columns=['qid', 'query', 'docno', 'text'])
            to_check_output = judger.transform(to_check_input)
            if(to_check_output[to_check_output.docno=='c_s_1']['rank'].values[0]==0):
                sentence_for_comparison = to_check
                o_start = k
        
        o_end = len(sentences)
        for k in range(len(sentences)-1, o_start, -1):
            to_check = sentence_assembler(sentences, list(range(o_start, k)))
            to_check_df_content = []
            to_check_df_content.append([target_qid, target_qtext, f'c_s_0', sentence_for_comparison])
            to_check_df_content.append([target_qid, target_qtext, f'c_s_1', to_check])
            to_check_input = pd.DataFrame(to_check_df_content, columns=['qid', 'query', 'docno', 'text'])
            to_check_output = judger.transform(to_check_input)
            if(to_check_output[to_check_output.docno=='c_s_1']['rank'].values[0]==0):
                sentence_for_comparison = to_check
                o_end = k
    
        interval_ids = [o_start-1, o_end]
        compare_indices = []
        for i in range(len(interval_ids)-1):
            compare_indices += list(range(interval_ids[i]+1, interval_ids[i+1]))
        sentence_for_comparison = sentence_assembler(sentences, compare_indices)   
        
        for k in range(o_start, o_end):
            to_check_interval_ids = interval_ids[:-1] + [k, o_end]
            to_check_indices = []
            for i in range(len(to_check_interval_ids)-1):
                to_check_indices += list(range(to_check_interval_ids[i]+1, to_check_interval_ids[i+1]))
                
            to_check = sentence_assembler(sentences, to_check_indices)
            to_check_df_content = []
            to_check_df_content.append([target_qid, target_qtext, f'c_s_0', sentence_for_comparison])
            to_check_df_content.append([target_qid, target_qtext, f'c_s_1', to_check])
            to_check_input = pd.DataFrame(to_check_df_content, columns=['qid', 'query', 'docno', 'text'])
            to_check_output = judger.transform(to_check_input)
            if(to_check_output[to_check_output.docno=='c_s_1']['rank'].values[0]==0):
                interval_ids = to_check_interval_ids
                sentence_for_comparison = to_check
        
        pseudo_optimal = sentence_for_comparison
        
        sentences_analysis_input_content.append([target_qid, target_qtext, f's_o', pseudo_optimal])
        
        sentences_analysis_input = pd.DataFrame(sentences_analysis_input_content, columns=['qid', 'query', 'docno', 'text'])
        sentences_analysis_output = judger.transform(sentences_analysis_input)
    
        trimmed_passage_dict.update({pid: {'text': pseudo_optimal, 'rel': sentences_analysis_output[sentences_analysis_output.docno=='s_o'].score.values[0]}})

    return trimmed_passage_dict

if __name__=="__main__":

    retriever = str(sys.argv[1])
    dataset_name = str(sys.argv[2]) # dl_19
    num_docs = int(sys.argv[3])
      
    if not pt.java.started():
        pt.java.init()
    
    from pyterrier_t5 import MonoT5ReRanker, DuoT5ReRanker
    monoT5 = MonoT5ReRanker(verbose=False) # loads castorini/monot5-base-msmarco by default
        
    with open('../../get_res/msmarco_passage_dict.pkl', 'rb') as f:
        doc_dict = pickle.load(f)
        
    splitter = SentenceSplitter(language='en')
        
    res = pd.read_csv(f'./res/{retriever}_{dataset_name}.csv')
    res.qid = res.qid.astype('str')
    res.docno = res.docno.astype('str')
        
    refined_dict = {}
    for target_qid in tqdm(res.qid.unique()):
        target_qtext = res[res.qid==target_qid]['query'].values[0]
        # print(target_qid, target_qtext)
        
        refined_dict.update({target_qid: trimming_passage(res, target_qid, target_qtext, splitter, monoT5, doc_dict, num_docs)})
        
    file_name = f'./refined_passages/refined_dict_{retriever}_{dataset_name}_top-{num_docs}.json'
    f = open(file_name, "w+", encoding='UTF-8')
    json.dump(refined_dict, f, indent=4)
    f.close()