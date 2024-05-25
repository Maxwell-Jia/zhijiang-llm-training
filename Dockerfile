# Use the NVIDIA CUDA runtime base image with Ubuntu 22.04
FROM nvidia/cuda:12.3.0-base-ubuntu22.04

RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update

# Install Python 3.10, pip, and git
RUN apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Ensure python3 points to python3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Set pip source to aliyun
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip

# Install torch, transformers, and other required packages
RUN pip3 install torch==2.3.0 \
    transformers==4.41.0 \
    datasets==2.19.1 \
    evaluate==0.4.2 \
    peft==0.11.1 \
    trl==0.8.6 \
    xformers \
    "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git" \
    accelerate \
    bitsandbytes

# Clean up pip cache to reduce image size
RUN rm -rf /root/.cache/pip

# Set environment variables
ENV HF_ENDPOINT=https://hf-mirror.com
