from gpt4all import GPT4All
from gpt4all import GPT4All

print(GPT4All.list_models())
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
model.serve(port=8000)
