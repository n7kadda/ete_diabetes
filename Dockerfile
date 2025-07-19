FROM python:slim
# Use a slim Python image as the base image
# Set environment variables to avoid writing .pyc files and to ensure output is sent straight to the terminal
ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app 

# Copy the requirements file into the container at /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -e .

# Install additional dependencies for the application
RUN python -m pipeline.training_pipeline

# Expose the port the app runs on
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]

