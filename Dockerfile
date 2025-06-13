# Use an official Python image
FROM python:3.10.16

# Set working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI runs on (matches --port below)
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]