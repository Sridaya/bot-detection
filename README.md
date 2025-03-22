# bot-detection
# Twitter Bot Detection Tool

## 📌 Overview
This project is a **Real-Time Twitter Bot Detection Tool** that uses **Machine Learning** to identify whether a Twitter account is a bot or a human. The tool fetches tweets using **Twitter API v1.1**, processes the account's activity, and predicts bot behavior using an ML model. It comes with a **FastAPI backend** and a **Streamlit-based GUI**.

## 🚀 Features
- Fetches Twitter data in **real-time**.
- Uses **Machine Learning (RandomForestClassifier)** for bot detection.
- Provides a **REST API** via FastAPI.
- User-friendly **Streamlit GUI**.
- **Deployed on Render** for 24/7 availability.

## 🏗️ Project Structure
```
Twitter-Bot-Detection/
├── twitter_fetch.py   # Fetch tweets from Twitter API
├── ml_model.py        # Machine Learning model for bot detection
├── main.py            # FastAPI backend
├── app.py             # Streamlit GUI
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
```

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd Twitter-Bot-Detection
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Twitter API Keys
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)
2. Create an **App** and get API keys
3. Add them to `twitter_fetch.py`

```python
API_KEY = "your_api_key"
API_SECRET_KEY = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"
```

### 4️⃣ Run the Backend API
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

### 5️⃣ Run the Streamlit UI
```bash
streamlit run app.py
```

## 🎯 Usage
- Open the **Streamlit UI** and enter a Twitter username.
- The tool will fetch the account’s data, analyze it, and predict whether it's a **bot** or a **human**.

## 🌍 Deployment on Render
### **1️⃣ Push Code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

### **2️⃣ Deploy FastAPI on Render**
- Go to **Render.com** → New Web Service
- Connect GitHub Repo
- Start command: `uvicorn main:app --port 10000`

### **3️⃣ Deploy Streamlit on Render**
- Go to **Render.com** → New Web Service
- Connect GitHub Repo
- Start command: `streamlit run app.py --server.port 8501`

## 🔥 Tech Stack
- **Python** 🐍
- **FastAPI** 🚀 (Backend API)
- **Streamlit** 🎨 (GUI)
- **Tweepy** 🐦 (Twitter API)
- **Scikit-Learn** 🤖 (Machine Learning)
- **Render** 🌐 (Deployment)

## 💡 Future Enhancements
✅ Improve ML model with **Deep Learning** (e.g., LSTMs).  
✅ Add **Sentiment Analysis** to detect fake news bots.  
✅ Optimize API calls to handle **real-time streaming**.

---

### 🛠 Developed by Dayasri K
Got any suggestions? Feel free to **open an issue** or **contribute!** 😃

