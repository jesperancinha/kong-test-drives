# Kong AI Template Plugin


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
 --data "service.id=$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')"
```

## Enable the AI Plugin:

```shell
curl -i -X POST http://localhost:8001/services/gemini-service/plugins \
--data 'name=ai-proxy' \
--data 'config.auth.param_name=key' \
--data 'config.auth.param_value=GEMINI_API_KEY' \
--data 'config.auth.param_location=query' \
--data 'config.route_type=llm/v1/chat' \
--data 'config.model.provider=gemini' \
--data 'config.model.name=gemini-1.5-flash'
```

```shell
export pluginId=$(curl http://localhost:8001/services/gemini-service/plugins | jq -r '.data[] | select(.name == "ai-proxy") | .id')
curl -X DELETE "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins/$pluginId" \
  --header "accept: application/json"
```

## AI Template Plugin

```shell
curl -X POST http://localhost:8001/services/gemini-service/plugins \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data '
    {
  "name": "ai-prompt-template",
  "config": {
    "allow_untemplated_requests": true,
    "templates": [
      {
        "name": "movie-chat",
        "template": "{\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"You love {{type}} films\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Name the most exciting of {{year}}\"\n    }\n  ]\n}"
      },
      {
        "name": "award-chat",
        "template": "{\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"You are a {{franchise}} fan\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"How many awards did {{film}} won?\"\n    }\n  ]\n}"
      }
    ]
  }
}
    '
```

## Remove

```shell
export pluginId=$(curl http://localhost:8001/services/gemini-service/plugins | jq -r '.data[] | select(.name == "ai-prompt-template") | .id')
curl -X DELETE "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins/$pluginId" \
  --header "accept: application/json"
```


## Test

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
	"messages": "{template://award-chat}",
	"properties": {
		"franchise": "Star Wars",
		"film": "The Return of the Jedi"
	}
}'
```

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
	"messages": "{template://movie-chat}",
	"properties": {
		"type": "action",
		"year": "1990"
	}
}'
```

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
    {"role": "user", "content": "Who played a song called \"Stay on These Roads\" in 1988"}
    ]
  }'
```
