
## Example

```yaml
    - name: ai-semantic-cache
      config:
        embeddings:
          auth:
            header_name: "Authorization"
            header_value: "MISTRAL_API_KEY"
          model:
            provider: mistral
            name: mistral-embed
        vectordb:
          strategy: redis
          distance_metric: euclidean
          dimensions: 1024
          threshold: 0.2
          redis:
            host: redis
            port: 6379
```

## References

- https://discuss.konghq.com/t/configurig-mistral-with-kongs-ai-semantic-plugin/13384/5
