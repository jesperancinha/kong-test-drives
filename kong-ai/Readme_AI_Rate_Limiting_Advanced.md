# AI Rate Limiting Advance plugin (under construction)

## Config variables

```properties
CONTROL_PLANE_ID=AAAAA
SERVICE_ID=AAAAA
ROUTE_ID=AAAAA
KONG_API_KEY=AAAAA
MISTRAL_API_KEY=AAAAA
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

## Enable the AI Rate Limiting Advanced plugin

```shell
curl -X POST \
"https://eu.api.konghq.com/v2/control-planes/$CONTROL_PLANE_ID/core-entities/routes/$ROUTE_ID/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $KONG_API_KEY" \
    --data '
{
  "name": "ai-rate-limiting-advanced",
  "config": {
    "llm_providers": [
      {
        "name": "mistral",
        "limit": 10,
        "window_size": 120
      }
    ]
  }
}'
```

## Testing

```shell
curl -i -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "What was the first popular breakthrough of dire straights, which led them to become one of the most known bands in the last decades?"
    }
  ]
  }'
```

```shell
curl -i -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "Who are dire straights?"
    }
  ]
  }'
```

```shell
curl -i -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "Who is Brian May?"
    }
  ]
  }'
```

```shell
curl -i -X POST http://localhost:8000/mistral \
  -H "Content-Type: application/json" \
  -d '{
  "messages": [
    {
        "role": "system",
        "content": "Who is Elvis Costello?"
    }
  ]
  }'
```

## References

- https://docs.konghq.com/kubernetes-ingress-controller/latest/plugins/rate-limiting/#optional-use-secrets-management
- https://docs.konghq.com/hub/kong-inc/ai-rate-limiting-advanced/
- https://stackoverflow.com/questions/67026851/centralized-rate-limiting-in-kong-using-redis
- https://www.linkedin.com/posts/zelarsoft_kong-gateway-advanced-rate-limiting-plugin-activity-7279349239225143296-fQKg
- https://tech.aufomm.com/how-to-use-redis-with-kong-rate-limiting-plugin
