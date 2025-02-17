# AI Video Processing System

## 🚀 Overview
This project is an **AI-powered video processing system** that runs entirely **locally** on your machine. It includes:
- ✅ **CUDA-optimized video processing** for **scene detection**.
- ✅ **Speech transcription** with Whisper AI.
- ✅ **AI-based summarization** using an open-source LLM.
- ✅ **AI-generated thumbnails** using **CLIP**.
- ✅ **Local storage and caching** with Redis and PostgreSQL.
- ✅ **Streamlit-based UI** for video upload & analysis.
- ✅ **Docker for containerized local deployment.**

---
## 🛠️ Tech Stack
### **Core Technologies**
- **Python** (FastAPI, Streamlit)
- **CUDA (GTX 1080 Support, Local Processing)**
- **OpenAI Whisper** (Speech-to-Text)
- **CLIP** (AI-based Thumbnail Generation)
- **Transformers** (LLM Summarization)
- **OpenCV & FFmpeg** (Video Processing)
- **Redis, PostgreSQL** (Local Storage & Caching)
- **Docker** (Local Deployment)

---
## 🔥 Features
### ✅ AI-Powered Video Processing
- **Scene Detection**: Uses **CUDA-optimized OpenCV** to find scene transitions.
- **Speech Transcription**: Converts **audio to text** with **Whisper AI**.
- **AI-Based Summarization**: Uses **LLM (Facebook BART-Large-CNN)** for summarization.
- **AI-Based Thumbnail Generation**: Uses **CLIP** to find the best frame for thumbnails.

### ✅ Local-First Infrastructure
- **FastAPI Backend** for real-time AI processing.
- **Streamlit UI** for easy video upload & results visualization.
- **PostgreSQL** for storing processed video metadata locally.
- **Redis** for fast caching of video analysis results.

### ✅ Local Deployment & Optimization
- **Runs completely offline (No cloud dependencies).**
- **Optimized for GTX 1080 / CUDA-based processing**
- **Docker for easy setup & isolation.**

---
## 📦 Installation
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-video-processing.git
cd ai-video-processing
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Run FastAPI Backend Locally**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4️⃣ **Run Streamlit UI Locally**
```bash
streamlit run main.py
```

---
## 🐳 Local Docker Deployment
### **Build & Run Docker Container**
```bash
docker build -t ai-video-processing .
docker run -p 8000:8000 ai-video-processing
```

---
## 📌 API Endpoints
### 🎬 **Process Video**
**POST** `/process_video/`
#### **Request**
```bash
curl -X 'POST' \
  'http://localhost:8000/process_video/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_video.mp4'
```
#### **Response**
```json
{
  "key_moments": [10.2, 34.8, 120.5],
  "transcript": "This is a sample transcript...",
  "summary": "Key highlights of the video...",
  "thumbnail": "thumbnail.jpg"
}
```

---
## 📜 License
This project is licensed under the **Apache 2.0 License**.

---
## 👥 Contributors
- **[John Alvarado](https://github.com/jpalvarado101)** - Creator & Maintainer

---
## ⭐ Support
If you like this project, **please ⭐ star the repository** and contribute! 🚀

