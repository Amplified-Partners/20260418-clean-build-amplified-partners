FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY config/ /app/config/
COPY agents/ /app/agents/
COPY rubrics/ /app/rubrics/
COPY templates/ /app/templates/
COPY orchestrator.py /app/
COPY api.py /app/

# Create output directory
RUN mkdir -p /app/outputs/clients

# Default: run all clients
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
