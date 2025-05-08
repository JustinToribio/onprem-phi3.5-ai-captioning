FROM pytorch/pytorch:2.7.0-cuda12.6-cudnn9-runtime

# Set environment variables for consistent behavior and real-time output
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure real-time stdout/stderr logs, useful for debugging
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /workspace

# Leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the correct dir (/workspace/app) in the container
COPY app app

# Expose FastAPI port
EXPOSE 8000

# Launch FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
