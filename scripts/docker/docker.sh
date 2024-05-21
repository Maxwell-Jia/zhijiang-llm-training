#!/bin/bash

docker build --build-arg DOCKER_OPTS="--registry-mirror=https://registry.docker-cn.com" -t huggingface .