# Kong's AI Semantic Prompt Guard Configuration (Under Development...)

## Config variables

```properties
CONTROL_PLANE_ID=AAAAA
SERVICE_ID=AAAAA
ROUTE_ID=AAAAA
```

## Start Service

```shell
curl -Ls https://get.konghq.com/quickstart | bash
```

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
  --data "name=mistral-service" \
  --data "url=https://your-upstream-ai-model-endpoint"
```

## Create a route

```shell
curl -i -X POST http://localhost:8001/routes \
  --data "name=ai-route" \
  --data "paths[]=/mistral" \
  --data "service.name=mistral-service"
```

## Enable the AI Plugin:

```shell
curl -X POST \
"https://eu.api.konghq.com/v2/control-planes/$CONTROL_PLANE_ID/core-entities/services/$SERVICE_ID/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer KONG_API_KEY" \
    --data '{
      "name": "ai-proxy",
      "config": {
        "model": {
          "name": "mistral-medium",
          "provider": "mistral",
          "options": {
            "mistral_format": "openai",
            "upstream_url": "https://api.mistral.ai/v1/chat/completions"
          }
        },
        "auth": {
          "header_name": "Authorization",
          "header_value": "Bearer MISTRAL_API_KEY"
        },
        "route_type": "llm/v1/chat"
      }
    }'
```

## AI Semantics plugin

```shell
docker run -it --rm --name redis -p 6379:6379 redis/redis-stack-server
```

```shell
curl -X POST \
"https://eu.api.konghq.com/v2/control-planes/$CONTROL_PLANE_ID/core-entities/routes/$ROUTE_ID/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer KONG_API_KEY" \
    --data '{
          "name": "ai-semantic-prompt-guard",
          "config": {
            "rules": {
              "match_all_conversation_history": true,
              "allow_prompts": ["Questions about StarWars"],
              "deny_prompts": ["Questions about StarTrek"]
            },
            vectordb:
              strategy: redis
              distance_metric: euclidean
              dimensions: 1024
              threshold: 0.2
              redis:
                host: redis
                port: 6379
              }
            }
    '
```

## Tests


```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-medium",
  "messages": [
    {
      "role": "system",
      "content": "You are an IT specialist."
    },
    {
      "role": "user",
      "content": "What does Kong do?"
    }
  ]
  }'
```

## Arguments for

✅ Flexibility → Centralized control over AI requests.

✅ Cost Efficiency → Reduces redundant API calls via caching.

✅ Security → Protects API keys and ensures data privacy.

✅ Scalability → Handles high AI traffic with rate limits and load balancing.

## Resources

- https://redis.io/docs/latest/commands/ft.info/
- https://discuss.konghq.com/t/configurig-mistral-with-kongs-ai-semantic-plugin/13384/5
