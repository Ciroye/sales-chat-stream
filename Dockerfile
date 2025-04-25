FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default port to 8080 as Cloud Run requires this to be configured
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]