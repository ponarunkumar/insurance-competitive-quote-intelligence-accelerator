FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY src/ ./src/
COPY agent.yaml ./

EXPOSE 8080

CMD ["python", "-m", "src.main"]
