install:
	pip install --upgrade pip
	pip install gpt4all
	sudo apt install -y nvidia-cuda-toolkit
	pip install fastapi
	pip install pydantic
	pip install uvicorn
start:
	kong restart
run-gpt4all:
	python3 startgpt4all.py
run-service:
	python3 -m uvicorn startgpt4all:app --host 0.0.0.0 --port 8080
test-raw:
	curl -X POST "http://localhost:8000/gpt4all" -H "Content-Type: application/json" -d '{"message": "Hello, GPT4All!"}'
test-raw2:
	curl -X POST "http://localhost:8000/gpt4all" -H "Content-Type: application/json" -d '{"message": "What is a bird?"}'
