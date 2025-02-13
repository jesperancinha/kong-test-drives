#

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
  --data name=gpt4all-service \
  --data url=http://localhost:8000/v1/chat/completions
```

## Create a route

```shell
curl -i -X POST http://localhost:8001/services/gpt4all-service/routes \
  --data name=gpt4all-route \
  --data paths=/gpt4all
```

## Enable the AI Plugin:

```shell
curl -i -X POST http://localhost:8001/services/gpt4all-service/plugins \
  --data name=ai \
  --data config.model=gpt4all \
  --data config.provider=openai \
  --data config.api_key=none \
  --data config.url=http://localhost:8000/v1/chat/completions
```

## Test

```shell
curl -X POST http://localhost:8000/gpt4all \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt4all",
    "messages": [{"role": "user", "content": "Hello, GPT4All!"}]
  }'
```