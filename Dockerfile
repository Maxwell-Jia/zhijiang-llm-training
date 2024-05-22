# Use a base image with CUDA 12.3
FROM nvidia/cuda:12.3.0-base-ubuntu22.04

# Set up environment
RUN sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list \
    && sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Update pip for Python 3.11 and set mirror to Alibaba Cloud
RUN python3 -m pip install --upgrade pip

# Copy project files
COPY . /app

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose any necessary ports
# EXPOSE 8080

# Command to run the application
# CMD ["python3", "app.py"]
