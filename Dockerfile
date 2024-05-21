# Use a base image with CUDA 12.3
FROM nvidia/cuda:12.3.0-base-ubuntu20.04

# Set up environment
RUN sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list \
    && sed -i 's|http://security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y wget build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.11
RUN wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz \
    && tar xzf Python-3.11.0.tgz \
    && cd Python-3.11.0 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.11.0 Python-3.11.0.tgz

# Make python3.11 as the default python
RUN ln -sf /usr/local/bin/python3.11 /usr/bin/python3

# Update pip for Python 3.11 and set mirror to Alibaba Cloud
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

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
