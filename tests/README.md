# Testing

## Sonar Cloud

### CLI Testing

```bash
export SONAR_TOKEN=<TOKEN>
sonar-scanner \
  -Dsonar.organization=spicyparrot \
  -Dsonar.projectKey=spicyparrot_pr-comment \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.sources=./src \
  -Dsonar.python.coverage.reportPaths=tests/reports/coverage.xml \
  -Dsonar.coverage.exclusions=tests/*
```

