# GPT4All Experiments in Kong

## Start Service

```shell
curl -Ls https://get.konghq.com/quickstart | bash
```

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
  --data name=gpt4all-service \
  --data url=http://localhost:8080
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
  --data "name=ai-proxy" \
  --data "config.route_type=llm/v1/chat" \
  --data "config.model.provider=gemini" \
  --data "config.auth.allow_override=false" \
  --data "config.model.name=gpt4all"
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

## Arguments for

✅ Flexibility → Centralized control over AI requests.

✅ Cost Efficiency → Reduces redundant API calls via caching.

✅ Security → Protects API keys and ensures data privacy.

✅ Scalability → Handles high AI traffic with rate limits and load balancing.
