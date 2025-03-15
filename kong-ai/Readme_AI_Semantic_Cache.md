# Kong's AI Semantic Cache Configuration (Under Development...)

## Config variables

```properties
CONTROL_PLANE_ID=AAAAA
SERVICE_ID=AAAAA
ROUTE_ID=AAAAA
KONG_API_KEY=AAAAA
```

## Start Service

```shell
curl -Ls https://get.konghq.com/quickstart | bash
```

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
  --data "name=my-service" \
      --data "url=http://localhost:32000"
```

## Create a route

```shell
curl -i -X POST http://localhost:8001/routes \
  --data "name=my-route" \
  --data "paths[]=/mistral" \
  --data "service.name=my-service"
```

## Enable the AI Plugin:

```shell
curl -X POST \
"https://eu.api.konghq.com/v2/control-planes/$CONTROL_PLANE_ID/core-entities/routes/$ROUTE_ID/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $KONG_API_KEY" \
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
          "header_value": "Bearer '$MISTRAL_API_KEY'"
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
    --header "Authorization: Bearer $KONG_API_KEY" \
    --data '
{
  "name": "ai-semantic-cache",
  "config": {
    "embeddings": {
      "auth": {
        "header_name": "Authorization",
        "header_value": "Bearer '$MISTRAL_API_KEY'"
      },
      "model": {
        "provider": "mistral",
        "name": "mistral-embed",
        "options": {
          "upstream_url": "https://api.mistral.ai/v1/embeddings"
        }
      }
    },
    "vectordb": {
      "strategy": "redis",
      "distance_metric": "euclidean",
      "dimensions": 1024,
      "threshold": 0.2,
      "redis": {
        "host": "'$REDIS_HOST'",
        "port": 6379
      }
    }
  }
}
'
```

## Tests


```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "tell me the color of the sun"
    }
  ]
  }'
```


```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What color best describes the color of the sun?"
    }
  ]
  }'
```

```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "Is the sun white yellow?"
    }
  ]
  }'
```

```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What is the color of Mars"
    }
  ]
  }'
```

```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What is the color of a car"
    }
  ]
  }'
```

```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What is the color of a red rose"
    }
  ]
  }'
```
```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "Is red rose colored red?"
    }
  ]
  }'
```

```shell
curl -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What is the color of earth?"
    }
  ]
  }'
```


## Final notes

Make sure to copy/paste these commands to the command line having previously exported these variables with the adjusted value:

```shell
export CONTROL_PLANE_ID=AAAAA
export SERVICE_ID=AAAAA
export ROUTE_ID=AAAAA
export KONG_API_KEY=AAAAA
export MISTRAL_API_KEY=AAAAA
export REDIS_HOST=AAAAA
```

## Resources

- https://redis.io/docs/latest/commands/ft.info/
- https://discuss.konghq.com/t/configurig-mistral-with-kongs-ai-semantic-plugin/13384/5
