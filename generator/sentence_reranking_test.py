from llama_tools import llama_tools
from prompt1_tools import *
import json
import sys
import pandas as pd

if __name__=="__main__":
    retriever_name = str(sys.argv[1])
    dataset_name = str(sys.argv[2])
    method_name = str(sys.argv[3]) # original/s-reranked/s-reranked_position
    batch_size = int(sys.argv[4])
    
    llm = llama_tools.load_llama()

    result_file_name = f'./answers/random_answers_{batch_size}shot_5calls_{retriever_name}_{dataset_name}_integrated_{method_name}.json'
    context_file_name = f'./context/integrated_context/integrated_contexts_{method_name}_{retriever_name}_{dataset_name}_{batch_size}.csv'
    query_file_name = f'./queries/queries_{dataset_name}.csv'
    
    f = open(file=context_file_name, mode="r", encoding='UTF-8')
    context_df = pd.read_csv(f)
    f.close()
    
    f = open(file=query_file_name, mode="r", encoding='UTF-8')
    query_df = pd.read_csv(f)
    f.close()
    
    result_record = {}
    for qid in query_df.qid.values:
        llm.set_seed(1000)
        query = query_df[query_df.qid==qid]['query'].values[0]
        print(query)
        
        preamble = used_preamble()
        context = compose_context_single(context_df, qid)
        prompt = f'{preamble} \n{context}Question: "{query}"\nNow start your answer. \nAnswer: '
        print(prompt)
        
        multi_call_results = {}
        result_record.update({str(qid): multi_call_results})
                  
        for j in range(5):
            print(f'\t\tno.{j}')
            result = llama_tools.single_call(llm=llm, prompt=prompt, temperature=0.3)
            multi_call_results.update({j: result})
    
    
    print(result_record)
     
    f = open(result_file_name, "w+", encoding='UTF-8')
    json.dump(result_record, f, indent=4)
    f.close()
    
    del llm