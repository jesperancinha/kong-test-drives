# Kong's AI Prompt Guard Configuration

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

## Enable AI Prompt Guard

```shell
curl -X POST "http://localhost:8001/services/$(curl -s http://localhost:8001/services/gemini-service | jq -r '.id')/plugins" \
    --header "accept: application/json" \
    --header "Content-Type: application/json" \
    --data '
    {
  "name": "ai-prompt-guard",
  "config": {
    "allow_all_conversation_history": true,
    "allow_patterns": [
      ".*R\\.E\\.M.*"
    ],
    "deny_patterns": [
      ".*(C|c)ar.*",
      ".*(J|j)acket.*"
    ]
  }
}
    '
```

## Test

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
    {"role": "user", "content": "What are the colors of the roses"},
    {"role": "user", "content": "When was the inception year of The Smashing Pumpkins?"}
    ]
  }'
```

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
    {"role": "user", "content": "Can you give me a json of something interesting?"}
    ]
  }'
```

```shell
curl -X POST http://localhost:8000/gemini \
  -H "Content-Type: application/json" \
  -d '{
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
