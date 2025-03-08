# Kong's AI Prompt Decorator

## Config variables

```properties
CONTROL_PLANE_ID=AAAAA
SERVICE_ID=AAAAA
ROUTE_ID=AAAAA
MISTRAL_API_KEY=AAAAA
KONG_API_KEY=AAAAA
REDIS_HOST=AAAAA
```

## Start Service

```shell
curl -Ls https://get.konghq.com/quickstart | bash
```

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
  --data "name=my-service" \
      --data "url=https://your-upstream-ai-model-endpoint"
```

## Create a route

```shell
curl -i -X POST http://localhost:8001/routes \
  --data "name=my-route" \
  --data "paths[]=/my-route" \
  --data "service.name=my-service"
```

## Enable the AI Proxy Plugin:

```shell
curl -i -X POST http://localhost:8001/services/my-service/plugins \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
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

## Enable AI Prompt Decorator

```shell
curl -X POST "http://localhost:8001/services/my-service/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data '
    {
  "name": "ai-prompt-decorator",
  "config": {
    "prompts": {
      "prepend": [
        {
          "role": "system",
          "content": "Tell me about a band that inspired this one."
        },
        {
          "role": "user",
          "content": "Make sure to name the founder."
        },
        {
          "role": "assistant",
          "content": "Name one band that were inspired by this band."
        }
      ],
      "append": [
        {
          "role": "user",
          "content": "Give some credit to JESPROTECH."
        }
      ]
    }
  }
}
    '
```

## Remove

```shell
export pluginId=$(curl http://localhost:8001/services/my-service/plugins | jq -r '.data[] | select(.name == "ai-prompt-decorator") | .id')
curl -X DELETE "http://localhost:8001/services/$(curl -s http://localhost:8001/services/my-service | jq -r '.id')/plugins/$pluginId" \
  --header "accept: application/json"
```

## Test

```shell
curl -X POST http://localhost:8000/my-route \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "Tell me in short something about Metallica"
    }
  ]
}'
```
```shell
curl -X POST http://localhost:8000/my-route \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
      "role": "assistant",
      "content": "Tell me in short something about Metallica"
    }
  ]
}'
```
