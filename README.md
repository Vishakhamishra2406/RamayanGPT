# 🕉️ RamayanGPT - AI-Powered Spiritual Guide

A modern, bilingual AI chatbot that brings the timeless wisdom of Ramayana to life through intelligent conversations. Ask questions in Hindi or English and receive detailed answers from both Tulsidas's Ramcharitmanas and Valmiki's Ramayana.

![Ramayan GPT](https://img.shields.io/badge/Language-Hindi%20%7C%20English-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![AI](https://img.shields.io/badge/AI-Powered-blue)

---

## ✨ Features

### 🌍 **Bilingual Support**
- **Hindi (हिंदी)**: Based on Tulsidas's Ramcharitmanas
- **English**: Based on Valmiki's Ramayana
- Automatic language detection
- Seamless language switching

### 📚 **Comprehensive Knowledge Base**
- **20+ Hindi Story Facts**: Detailed answers about key events and characters
- **15+ English Story Facts**: Comprehensive Ramayana episodes
- **Character Analysis**: Rama, Sita, Hanuman, Ravana, and more
- **Spiritual Teachings**: Dharma, devotion, righteousness

### 🎨 **Modern Web Interface**
- Beautiful ChatGPT-like design
- Real-time chat interface
- Connection status indicators
- Mobile-responsive design

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Launch RamayanGPT**
```bash
python start_ramayan_gpt.py
```

This will:
- ✅ Start the server on port 8001
- ✅ Open the web interface in your browser
- ✅ Display usage instructions

### **3. Start Asking Questions!**

**English:**
- "Who were the sons of Dasharatha?"
- "Where did Ravana keep Sita?"
- "Tell me about Hanuman"

**Hindi:**
- "दशरथ के पुत्रों के नाम क्या थे?"
- "रावण ने सीता को कहाँ रखा था?"
- "हनुमान जी के बारे में बताएं"

---

## 📁 Project Structure

```
RamayanGPT/
├── ramayan_gpt_ui.html              # Modern web interface
├── bilingual_ramayan_server.py      # FastAPI server
├── enhanced_ramayan_chatbot.py      # Core AI logic
├── ramcharitmanas_training_data.json # Hindi knowledge base
├── english_training_data.json       # English knowledge base
├── start_ramayan_gpt.py            # Easy launcher
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
├── Gemini_Generated_Image_k7j7n8k7j7n8k7j7.png # Logo
└── README.md                        # This file
```

---

## Screenshots
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/6968d424-5c29-4c92-9dd5-b8834b5f6fde" />
<img width="1910" height="914" alt="image" src="https://github.com/user-attachments/assets/9dc16041-3ed5-44ec-bb81-7d5da6bfdeae" />
<img width="1910" height="905" alt="image" src="https://github.com/user-attachments/assets/3e4d3021-5ccc-45a0-b902-82d4bfa09cea" />
<img width="1906" height="914" alt="image" src="https://github.com/user-attachments/assets/89fd5e39-1904-432e-90c4-25a2d9db0ad2" />





### **Web Interface**
1. Run `python start_ramayan_gpt.py`
2. Open the web interface in your browser
3. Type your question in the chat input
4. Press Enter or click the send button

### **Direct Server Access**
```bash
python bilingual_ramayan_server.py
```
Then visit: `http://localhost:8001`

### **API Usage**
```python
import requests

response = requests.post('http://localhost:8001/ask-bilingual', json={
    "question": "Who were the sons of Dasharatha?",
    "preferred_language": "auto"
})

print(response.json()['answer'])
```

---

## 🧠 Knowledge Base

### **Hindi (Ramcharitmanas) - 20+ Facts**
- Birth stories (Rama, Hanuman)
- Exile and forest life
- Sita's abduction
- Lanka war
- Character qualities
- Spiritual teachings

### **English (Valmiki Ramayana) - 15+ Facts**
- Dasharatha's sons
- Sita's swayamvara
- Bridge to Lanka
- Ravana's death
- Rama's coronation
- Devotional episodes

---

## 🔧 Configuration

### **Environment Variables** (`.env`)
```bash
GEMINI_API_KEY=your_api_key_here  # Optional - works without it
```

### **Server Settings**
- **Port**: 8001
- **Host**: localhost
- **CORS**: Enabled for all origins

---

## 🎨 UI Features

- **Clean Design**: Orange gradient theme with spiritual aesthetics
- **Chat Interface**: Real-time messaging
- **Status Indicators**: Connection status with visual feedback
- **Bilingual Input**: Supports both Hindi and English
- **Mobile Responsive**: Works on all devices

---

## 📊 Technical Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Keyword-based matching with optional Gemini integration
- **Data**: JSON knowledge bases
- **Server**: Uvicorn ASGI

---

## 🔧 API Endpoints

- `GET /` - Web interface
- `POST /ask-bilingual` - Ask questions
- `POST /detect-language` - Language detection
- `GET /health-bilingual` - Health check
- `GET /training-status` - Training data status
- `GET /sample-questions-bilingual` - Sample questions

---

## 🙏 Spiritual Context

This project aims to make the profound wisdom of Ramayana accessible through technology. The Ramayana teaches:

- **Dharma** (Righteousness)
- **Devotion** and **Surrender**
- **Ideal Relationships**
- **Leadership** and **Governance**
- **Faith** and **Determination**

---

## 🆘 Troubleshooting

**Server won't start?**
- Check if port 8001 is available
- Install dependencies: `pip install -r requirements.txt`

**Connection refused error?**
- Ensure server is running: `python bilingual_ramayan_server.py`
- Check browser console for errors
- Try refreshing the page

**No responses?**
- Verify server is running on port 8001
- Check if training data files exist
- Try asking specific questions about Ramayana

---

## 📝 Contributing

Contributions welcome! You can:
- Add more story facts to JSON files
- Improve the UI/UX design
- Enhance language detection
- Add new features
- Fix bugs

---

## 📄 License

This project is created for educational and spiritual purposes. The Ramayana texts are in the public domain.

---

**🕉️ Jai Shri Ram! May this digital seva spread the eternal wisdom of Ramayana worldwide. 🙏**

---

*Built with ❤️ for seekers of spiritual wisdom*
