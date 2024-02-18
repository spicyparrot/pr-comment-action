# Minimal python
FROM python:3.10-slim AS builder

# Add repo code & install dependencies
WORKDIR /app
ADD src src

RUN python3 -m pip install --quiet -r ./src/requirements.txt

# Start command
ENTRYPOINT ["python3"]
ENV PYTHONPATH /app
CMD ["/app/src/main.py"]