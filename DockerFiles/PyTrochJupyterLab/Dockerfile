# Use ARM-compatible Python base image
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install JupyterLab and Python libs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy any local files (optional)
COPY . .

# Expose JupyterLab
EXPOSE 8888

# Run JupyterLab on container start
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]