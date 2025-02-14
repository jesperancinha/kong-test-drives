from fastapi import FastAPI
from pydantic import BaseModel
from gpt4all import GPT4All

app = FastAPI()

print(GPT4All.list_models())
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

class RequestData(BaseModel):
    message: str

@app.post("/gpt4all")
def chat(request: RequestData):
    response = model.generate(request.message)
    return {"response": response}
