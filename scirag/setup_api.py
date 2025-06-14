import os.path
from typing import Union
from setup_rag import *
from fastapi import FastAPI





def init_ragchain():
    global chain
    path = os.path.dirname(os.path.realpath(__file__))

    path_index = f"{path}/../data/index"
    path_dataset = f"{path}/../data/acl-publication-info.74k.parquet"
    if os.path.exists("/bigwork/nhwpajjy/pre-trained-models"):
        path_model = "/bigwork/nhwpajjy/pre-trained-models/TinyLlama-1.1B-Chat-v1.0"
    elif os.path.exists("/mnt/home/yajjour/pre-trained-models"):
        path_model ="/mnt/home/yajjour/pre-trained-models/TinyLlama-1.1B-Chat-v1.0"
    else:
        path_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    if not os.path.exists(path_index):
        create_index( path_dataset=path_dataset, path_index=path_index, debug=False)

    chain = create_rag_pipeline(path_index, path_model, True)

chain = None
init_ragchain()

app = FastAPI()

@app.get("/chat")
def read_item(q: Union[str, None] = None):
    if not chain:
        return {"answer": "call /"}
    answer = chain.run({"query": q})
    print(answer)
    #answer = answer.split("<assistant>:")[1]
    return {"answer": answer}
