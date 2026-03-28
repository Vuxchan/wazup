## build stage ## 
FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY src/ ./src/

## run stage ##
FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/src ./src

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
