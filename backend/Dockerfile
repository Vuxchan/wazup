## build stage ##
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY src/ ./src/

## run stage ##
FROM python:3.12-slim

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /app/src ./src

RUN chown -R appuser:appgroup /app

ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "fastapi run src/main.py --host 0.0.0.0 --port ${PORT:-8000}"]