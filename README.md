# 🧠 On-Prem Phi-3.5 AI Image Captioning

A high-performance, on-premises FastAPI application for image captioning using Microsoft's cutting-edge [Phi-3.5 Vision Instruct](https://huggingface.co/microsoft/Phi-3.5-vision-instruct) model. Designed for local inference with GPU acceleration, model caching, and scalable architecture.

---

## 📚 Table of Contents
- [Introduction](#introduction)
- [System Requirements](#system-requirements)
- [Running the App with Docker](#running-the-app-with-docker)
- [Sample Output](#sample-output)

---

## 🚀 Introduction

This app loads the Phi-3.5 Vision model once at startup and exposes an `/infer` REST endpoint via FastAPI. You can send image files as POST requests or through FastAPI's browser based Swagger UI and receive intelligent captions in response.

Key features:
- 🔥 GPU-accelerated inference with PyTorch + CUDA
- 📦 Efficient Hugging Face model caching
- 🧩 Modular architecture (FastAPI, async, singleton pattern)
- 🐳 Fully containerized with Docker and Docker Compose

---

## 🛠️ System Requirements

- NVIDIA GPU that can support **CUDA 12.6**
    -  According to the Phi-3.5 model card, it was tested on A100, A6000 and H100 gpus
    - My local machine only has a Quadro P1000 (4 GB RAM) and it's able to successfully run the inference. However, I had to adjust several model parameters to reduce memory usage to avoid out-of-memory issues (as currently set in this repo, i.e. max_tokens, number of patches etc...). As a result, my machine can only handle 1 image at a time and inference is quite slow... but it works.
- Correct NVIDIA driver based on your gpu: https://www.nvidia.com/en-us/drivers/
- Docker Engine that runs a Linux kernel: https://docs.docker.com/engine/install/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- Docker Compose v2


---

## 🐳 Running the App with Docker

### 1. Clone the repo
```bash
git clone https://github.com/JustinToribio/onprem-phi3.5-ai-captioning.git
cd onprem-phi3.5-ai-captioning
```

### 2. Start the app using Docker Compose
```bash
docker compose up
```

> ✅ On first run, the Docker Image will be built (~6.8GB) and then Docker will start the container app from that image.  The Phi-3.5 model (~7.8GB) will be downloaded and cached at `~/.cache/huggingface/hub`.  
> ✅ On subsequent runs, assuming nothing has changed, the containerized app will run from that same Docker image and the Phi-3.5 model will be loaded from the cache.
* Wait for the model to finish loading

### 3. Test the endpoint

From a different command line shell, send a POST request with an image using `curl`:

```bash
curl -X POST http://localhost:8000/infer \
  -H "Content-Type: multipart/form-data" \
  -F "file=@<path_to_local_image>.jpg"
```

Or use FastAPI's browser based Swagger UI:
* In your browser, go to: http://localhost:8000/docs
* Select "Try it out"
* Attach an image file from your local system and then select "Execute"

After you're done testing...

### 4. Shut down the app

```
CTRL+C   # From the terminal where you launched the app and can see the live logs
```

### 5. Stop and remove the Docker Container

```bash
docker compose down
```

---

## 🧪 Sample Output

Example image sent to the `/infer` endpoint:

![Sample Output](images/nba_2.jpg)

Response:
```json
{
  "caption": "The image captures a moment from a basketball game between the Los Angeles Lakers and the Golden State Warriors. The players are in the midst of a play, with the Lakers in purple and the Warriors in white. The crowd is visible in the background, and the game is being broadcasted on TNT."
}
```

Example image sent to the `/infer` endpoint:

![Sample Output](images/car.jpg)

Response:
```json
{
  "caption": "The image shows a silver BMW i8 sports car parked in a parking lot. The car has a distinctive design with a low and wide stance, a large front grille, and a futuristic look with sharp angles and a sleek body. The BMW logo is visible on the front of the car."
}
```
