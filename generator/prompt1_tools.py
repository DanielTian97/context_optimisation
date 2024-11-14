def used_preamble():
    return "You are an expert at answering questions based on your own knowledge and related context. Please answer this question based on the given context. End your answer with STOP."

# prepare needed files
def prepare_data(dataset_name: str, retriever_name = 'bm25'):
    import pandas as pd
    # read the retrieved documents
    import pickle
    
    if(retriever_name == 'bm25'):
        with open('./middle_products/msmarco_passage_v1_retrieved_top_tail.pkl', 'rb') as f:
            doc_dict = pickle.load(f)
            f.close()
    elif('oracle' in retriever_name):
        with open('./middle_products/msmarco_passage_v1_qrels.pkl', 'rb') as f:
            doc_dict = pickle.load(f)
            f.close()
    elif(retriever_name == 'mt5'):
        with open('./middle_products/msmarco_passage_v1_retrieved_mt5.pkl', 'rb') as f:
            doc_dict = pickle.load(f)
            f.close()
    else:
        print('this retriever is not supported')
        return
    # prepare queries
    queries = pd.read_csv(f'./middle_products/queries_{dataset_name}.csv')
    # prepare res file
    res = pd.read_csv(f'./res/{retriever_name}_dl_{dataset_name}.csv') # retrieval result
      
    return doc_dict, queries, res

# compose the examples in the context part into a single passage
def compose_context_single(context_res, qid: str):
    print(qid)
    retrieved_for_q = context_res[context_res.qid==qid].sort_values(by=['rank']).head(1)
    
    composed_context = ''
    text = retrieved_for_q.text.values[0]
    composed_context += f'Context: "{text}";\n'
            
    return composed_context

# compose the examples in the context part
def compose_context_simplified(context_res, qid: str, batch_size):
    print(qid)
    retrieved_for_q = context_res[context_res.qid==qid].sort_values(by=['rank']).head(batch_size)
    
    composed_context = ''
    batch_texts = retrieved_for_q.text.values
            
    num = 0
    for text in batch_texts:
        num += 1
        composed_context += f'Context {num}: "{text}";\n'
            
    return composed_context

# compose the examples in the context part
def compose_context(res, qid: str, batch_size, batch_step, top_starts, tail_starts, doc_dict):
    print(qid)
    retrieved_for_q = res[res.qid==qid]
    retrieved_num = retrieved_for_q['rank'].max()+1
      
    starts = list(range(0, (retrieved_num-1)-(batch_size-1)+1, batch_step))
    start_rank_list = list(set(starts[:top_starts]).union(set(starts[(len(starts)-1)-(tail_starts-1):])))
    start_rank_list.sort()
    print(start_rank_list)
    context_book = []
    for start in start_rank_list:
        context = ''
        end = start + batch_size
        batch_docnos = retrieved_for_q[(retrieved_for_q['rank']>=start)&(retrieved_for_q['rank']<end)].docno.tolist()
        batch_texts = [doc_dict[str(docno)] for docno in batch_docnos]
            
        num = 0
        for text in batch_texts:
            num += 1
            context += f'Context {num}: "{text}";\n'
            
        context_book.append(context)
            
    return start_rank_list, context_book