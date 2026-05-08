FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir asyncpg fastapi uvicorn sse-starlette
COPY brain_mcp_server.py /app/server.py
EXPOSE 8080
CMD ["python", "/app/server.py"]
