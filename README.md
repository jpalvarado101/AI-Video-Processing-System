# **AI-Powered Video Clipping & Summarization Tool 🎥🚀**

🚨 **License Notice:**  
This project is under a **strict Read-Only License**.  
✔️ You may **view** the code, but  
❌ You **cannot copy, modify, use, or distribute** any part of it.  
Violations may result in legal action. See the [LICENSE](LICENSE) file for details.

An **AI-driven video processing** tool that extracts the **most engaging moments** from long-form videos **locally** using **Whisper, CLIP, OpenCV, Kafka, Redis, and Kubernetes**.  

🔹 **No OpenAI API required!** Uses **free open-source models** instead.  
🔹 **Deployable on Minikube/K3s** (Kubernetes-ready)  
🔹 **Real-time Kafka & Redis Processing**  
🔹 **GPU-Optimized (GTX 1080 Recommended, but CPU works too)**  

---

## **📌 Features**
✅ **AI-Powered Video Highlight Detection** (CLIP Model)  
✅ **Scene Segmentation** (SceneDetect + OpenCV)  
✅ **Speech & Emotion Analysis** (Whisper ASR + Sentiment Analysis)  
✅ **LLM-Based Auto Captioning** (Llama 3 / Falcon)  
✅ **FFmpeg for Video Processing**  
✅ **Kafka + Redis for Real-Time Processing**  
✅ **Kubernetes (Minikube/K3s) for Scalability**  
✅ **Streamlit UI for User Interaction**  

---

## **📂 Project Structure**
```
AI-Video-Clipping/
├── backend/
│   ├── app.py                 # FastAPI Backend
│   ├── requirements.txt        # Python Dependencies
│   ├── Dockerfile              # Dockerized Backend
│   ├── k8s/                    # Kubernetes Configurations
│   │   ├── deployment.yaml      # K8s Deployment
│   │   ├── service.yaml         # K8s Service
│   ├── models/                  # AI Models
│   │   ├── clip_model.py         # CLIP-based scene selection
│   │   ├── speech_analysis.py    # Whisper ASR + Sentiment Analysis
│   │   ├── summarization.py      # Llama 3 / Falcon AI Summarization
│   ├── utils/                    # Utility Functions
│   │   ├── video_processing.py   # Scene detection (SceneDetect + OpenCV)
│   │   ├── kafka_producer.py     # Kafka Producer
│   │   ├── redis_cache.py        # Redis Caching
├── frontend/
│   ├── app.py                 # Streamlit Frontend
│   ├── requirements.txt        # Streamlit Dependencies
├── kafka_setup/
│   ├── docker-compose.yml      # Kafka + Zookeeper Setup
└── README.md                   # Documentation
```

---

## **⚡ Installation & Setup**
### **🔹 1. Start Kafka & Redis**
Ensure **Kafka and Redis** are running before executing the backend:

```sh
cd kafka_setup
docker-compose up -d
```

Start Redis:

```sh
docker run -d -p 6379:6379 redis
```

### **🔹 2. Install Dependencies**
#### **Backend Setup**
```sh
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

#### **Frontend Setup (Streamlit)**
```sh
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## **🎯 How It Works**
1. **Upload a video via the Streamlit UI.**  
2. The **backend processes the video**:  
   - Detects **scene changes** using **OpenCV & SceneDetect**.  
   - Extracts **audio & transcribes** it via **Whisper ASR**.  
   - Runs **sentiment analysis** to detect **high-emotion moments**.  
   - Uses **CLIP to score each scene** and selects the most engaging one.  
   - Generates **automatic captions & summaries** via **Llama 3 / Falcon**.  
3. **Kafka sends events** to simulate **A/B testing**.  
4. **Redis caches results** for faster retrieval.  
5. **The best-scoring clip is displayed** with a generated caption.  

---

## **🖥️ Backend API (FastAPI)**
### **🔹 Endpoint: Process Video**
```http
POST /process_video
```
#### **Request:**
Upload a video file (`.mp4`, `.mov`, `.avi`).
```sh
curl -X POST "http://localhost:8000/process_video" -F "file=@your_video.mp4"
```
#### **Response:**
```json
{
  "caption": "The speaker passionately discusses the importance of AI...",
  "best_scene": [10.5, 15.2],  # Start & End time of the best scene
  "sentiments": "Positive"
}
```

---

## **🖥️ Streamlit UI (Frontend)**
1. **Upload a video**  
2. Click **Process Video**  
3. The AI will **find the best scene, transcribe speech, and generate a caption.**  
4. The **output video and text** are displayed.

---

## **☸️ Deployment (Kubernetes - Minikube/K3s)**
### **🔹 Deploy the Backend**
```sh
kubectl apply -f backend/k8s/deployment.yaml
kubectl apply -f backend/k8s/service.yaml
```
### **🔹 Expose the Service**
```sh
minikube service ai-video-backend-service --url
```
### **🔹 Run Kubernetes Dashboard**
```sh
minikube dashboard
```

---

## **🛠️ Key Technologies Used**
### **🔹 AI Models**
- **Whisper ASR** → **Transcribes video speech** into text.  
- **CLIP** → **Finds the most visually engaging scene**.  
- **Hugging Face Sentiment Analysis** → Detects emotional moments.  
- **Llama 3 / Falcon** → Generates **video captions & summaries**.  

### **🔹 Backend (FastAPI)**
- Handles **AI processing requests**.  
- Communicates with **Kafka & Redis**.  
- Serves **AI-generated captions and summaries**.  

### **🔹 Frontend (Streamlit)**
- **User uploads video** and receives the **best-scoring clip**.  

### **🔹 Infrastructure**
- **Kafka** → Simulates **real-time A/B testing**.  
- **Redis** → Caches results for **faster video retrieval**.  
- **Kubernetes** → Deploys backend with **auto-scaling & load balancing**.  

---

## **📌 Sample Output**
**Uploaded Video:** `"example_video.mp4"`  
**Best Scene:** `Start: 10.5s → End: 15.2s`  
**Generated Caption:** `"The speaker passionately discusses the importance of AI..."`  
**Sentiment Analysis:** `"Positive"`  

🎥 **The best scene is clipped and ready for sharing!**  

---

## **🚀 Future Improvements**
✅ **AI-Powered Auto-Cropping** (Adjust framing dynamically)  
✅ **Multi-Modal Learning** (Combine **video, speech, and facial expressions**)  
✅ **GPU-Optimized Pipelines** (TensorRT for faster inference)  
✅ **Realtime Engagement Prediction** (Train models to **predict virality**)  

---

## **💡 FAQ**
### **❓ Can I run this without a GPU?**
Yes! All models run **on CPU**, but for **faster processing**, a **GPU (GTX 1080 or better) is recommended**.

### **❓ Do I need OpenAI’s API?**
No! This project **only uses free, open-source models** (Whisper, CLIP, Llama 3, etc.).

### **❓ How does Kafka improve this system?**
Kafka simulates **real-time event processing**, allowing **A/B testing of different AI-generated video clips**.

### **❓ Why use Redis?**
Redis caches the **best scenes and captions**, so users don’t need to reprocess the same video.

---

## **📜 License**
This project is licensed under my **Custom Read-Only License**.

---

## **🔥 Conclusion**
This **AI Video Clipping System** makes you **the perfect candidate for OpusClip** by showcasing:
✅ **AI-Driven Video Processing**  
✅ **Backend Engineering & API Development**  
✅ **Data Pipelines (Kafka & Redis)**  
✅ **Cloud Deployment (Kubernetes / Minikube)**  
✅ **Real-World Scalability**  

