# Kong's AI Response Transformer Plugin(Under Development...)

## Start Service

```shell
curl -Ls https://get.konghq.com/quickstart | bash
```

## Create Service

```shell
curl -i -X POST http://localhost:8001/services \
 --data "name=gemini-service" \
 --data "url=https://generativelanguage.googleapis.com"
```

## Create a route

```shell
curl -i -X POST http://localhost:8001/routes \
 --data "paths[]=/gemini" \
 --data "name=gemini-route" \
 --data "service.id=$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')"
```

## Enable the AI Plugin:

```shell
curl -i -X POST http://localhost:8001/services/gemini-service/plugins \
  --header "Content-Type: application/json" \
  --data '{
    "name": "ai-proxy",
    "config": {
      "auth": {
        "param_name": "key",
        "param_value": "GEMINI_KEY",
        "param_location": "query"
      },
      "route_type": "llm/v1/chat",
      "model": {
        "provider": "gemini",
        "name": "gemini-1.5-flash"
      }
    }
  }'
```

```shell
export pluginId=$(curl http://localhost:8001/services/gemini-service/plugins | jq -r '.data[] | select(.name == "ai-proxy") | .id')
curl -X DELETE "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins/$pluginId" \
  --header "accept: application/json"
```

## Enable the AI Request Transformer Plugin

```shell
curl -X POST "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins" \
   --header "accept: application/json" \
   --header "Content-Type: application/json" \
   --data '
   {
     "name": "ai-response-transformer",
     "config": {
       "prompt": "Replace any email addresses in the ''message'' field with ''[REDACTED]''.",
       "llm": {
          "route_type": "llm/v1/chat",
          "auth": {
            "header_name": "Authorization",
            "header_value": "Bearer GEMINI_KEY"
          },
          "logging": {
            "log_statistics": true,
            "log_payloads": false
          },
          "model": {
            "provider": "gemini",
            "name": "gemini-2.0-flash",
            "options": {
          "max_tokens": 1024
        }
         }
       }
     }
    }
   '
```

## Remove

```shell
export pluginId=$(curl http://localhost:8001/services/gemini-service/plugins | jq -r '.data[] | select(.name == "ai-response-transformer") | .id')
curl -X DELETE "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins/$pluginId" \
  --header "accept: application/json"
```

## Test

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Harrison Ford"
  }'
```
