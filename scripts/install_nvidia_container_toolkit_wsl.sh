#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop for Windows with WSL2 integration enabled."
    exit 1
fi

# Check nvidia-smi (i.e., host GPU is visible)
if ! command -v nvidia-smi &> /dev/null; then
    echo "nvidia-smi not found. Ensure your NVIDIA drivers are installed on Windows and WSL2 integration is working."
    exit 1
fi

echo "Prerequisites met. Proceeding with installation..."

# Add the NVIDIA Docker GPG key and repo
# From official NVIDIA documentation: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker

echo "NVIDIA Container Toolkit installed and configured."

echo "Restarting Docker service..."
if command -v systemctl &> /dev/null; then
    sudo systemctl restart docker
else
    echo "You may need to restart Docker Desktop from Windows for changes to take effect."
fi

# This is the official test command from NVIDIA to verify installation
echo "Done! You can confirm that a Docker container has access to your NVIDIA GPU with an NVIDIA base image:"
echo "docker run --rm --gpus all nvidia/cuda:12.3.2-base-ubuntu22.04 nvidia-smi"
