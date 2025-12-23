"""
Bilingual Ramayan Server - Hindi + English
Complete server supporting both Ramcharitmanas (Hindi) and Valmiki Ramayana (English)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import os
from enhanced_ramayan_chatbot import EnhancedRamayanChatbot

app = FastAPI(
    title="🕉️ Bilingual Ramayan AI Chatbot",
    description="Complete bilingual chatbot supporting Hindi Ramcharitmanas and English Valmiki Ramayana"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize enhanced chatbot
chatbot = EnhancedRamayanChatbot()

class BilingualQuestion(BaseModel):
    question: str
    preferred_language: str = "auto"  # "hindi", "english", or "auto"

class LanguageQuery(BaseModel):
    text: str

@app.get("/")
async def serve_ui():
    """Main web interface"""
    return FileResponse('ramayan_gpt_ui.html')

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    return {"message": "No favicon configured"}

@app.post("/ask-bilingual")
async def ask_bilingual_question(request: BilingualQuestion):
    """Ask question to bilingual Ramayan AI"""
    try:
        print(f"🌐 Bilingual Question: {request.question}")
        print(f"🔤 Preferred Language: {request.preferred_language}")
        
        # Generate bilingual response
        answer = await chatbot.generate_response(request.question)
        
        # Detect language
        detected_language = chatbot.detect_language(request.question)
        
        return {
            "question": request.question,
            "answer": answer,
            "detected_language": detected_language,
            "preferred_language": request.preferred_language,
            "sources": {
                "hindi": "श्री रामचरितमानस - गोस्वामी तुलसीदास जी",
                "english": "The Ramayana - Sage Valmiki (Griffith Translation)"
            },
            "training_data": {
                "hindi_pages": "1054 pages from Ramcharitmanas PDF",
                "english_pages": "1960 pages from English Ramayana PDF",
                "total_content": "Over 2 million characters extracted"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-language")
async def detect_language(request: LanguageQuery):
    """Detect language of input text"""
    try:
        language = chatbot.detect_language(request.text)
        
        return {
            "text": request.text,
            "detected_language": language,
            "confidence": "high" if len(request.text) > 10 else "medium"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/training-status")
async def get_training_status():
    """Get bilingual training data status"""
    
    files_status = {}
    
    # Check all training files
    training_files = [
        "ramcharitmanas_training_data.json",
        "english_training_data.json",
        "english_extracted.txt",
        "रामचरितमानस_extracted.txt"
    ]
    
    for file in training_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            files_status[file] = {
                "exists": True,
                "size_bytes": size,
                "size_mb": round(size / (1024*1024), 2)
            }
        else:
            files_status[file] = {"exists": False}
    
    return {
        "bilingual_support": True,
        "languages": ["Hindi (Devanagari)", "English"],
        "hindi_source": {
            "title": "श्री रामचरितमानस",
            "author": "गोस्वामी तुलसीदास जी",
            "language": "अवधी हिंदी",
            "pages": 1054
        },
        "english_source": {
            "title": "The Ramayana",
            "author": "Sage Valmiki",
            "translator": "Ralph T.H. Griffith",
            "language": "English",
            "pages": 1960
        },
        "training_files": files_status,
        "features": [
            "Automatic language detection",
            "Bilingual responses",
            "Cross-language references",
            "Story fact matching",
            "Character analysis in both languages"
        ]
    }

@app.get("/sample-questions-bilingual")
async def get_bilingual_sample_questions():
    """Get sample questions in both languages"""
    return {
        "hindi_questions": {
            "story_facts": [
                "दशरथ के पुत्रों के नाम क्या थे?",
                "रावण ने सीता को कहाँ रखा था?",
                "राम का वनवास क्यों हुआ?",
                "हनुमान जी ने लंका कैसे जलाई?"
            ],
            "character_questions": [
                "राम के मुख्य गुण क्या थे?",
                "सीता माता का चरित्र कैसा था?",
                "हनुमान जी की भक्ति कैसी थी?",
                "लक्ष्मण जी के गुण बताइए।"
            ],
            "teaching_questions": [
                "धर्म क्या है रामचरितमानस के अनुसार?",
                "भक्ति का महत्व क्या है?",
                "त्याग की शिक्षा क्या मिलती है?"
            ]
        },
        "english_questions": {
            "story_facts": [
                "Who were the sons of King Dasharatha?",
                "Where did Ravana keep Sita captive?",
                "Why did Rama go into exile?",
                "How did Hanuman burn Lanka?"
            ],
            "character_questions": [
                "What are the main qualities of Rama?",
                "Describe Sita's character",
                "Tell me about Hanuman's devotion",
                "What are Lakshmana's virtues?"
            ],
            "general_questions": [
                "What is the Ramayana about?",
                "Who wrote the original Ramayana?",
                "What lessons does the Ramayana teach?",
                "How many books are in the Ramayana?"
            ]
        },
        "mixed_language_examples": [
            "Tell me about राम के गुण in English",
            "Explain Hanuman's devotion in Hindi",
            "Compare Valmiki and Tulsidas versions"
        ]
    }

@app.get("/language-comparison")
async def get_language_comparison():
    """Compare Hindi and English versions"""
    return {
        "comparison": {
            "hindi_ramcharitmanas": {
                "author": "गोस्वामी तुलसीदास जी",
                "period": "16वीं शताब्दी",
                "language": "अवधी हिंदी",
                "style": "दोहे और चौपाई",
                "focus": "भक्ति और आध्यात्म",
                "kands": 7
            },
            "english_valmiki": {
                "author": "Sage Valmiki",
                "translator": "Ralph T.H. Griffith",
                "period": "Ancient (translated 1870-1874)",
                "language": "English verse",
                "style": "Epic poetry",
                "focus": "Complete narrative",
                "books": 7
            }
        },
        "key_differences": [
            "Tulsidas focuses more on devotion (bhakti)",
            "Valmiki provides more detailed narrative",
            "Different cultural contexts and interpretations",
            "Tulsidas uses Awadhi Hindi, Valmiki uses Sanskrit"
        ],
        "common_elements": [
            "Same core story of Rama",
            "Seven main sections/books",
            "Focus on dharma and righteousness",
            "Character development of main figures"
        ]
    }

@app.get("/health-bilingual")
async def health_check_bilingual():
    """Complete bilingual system health check"""
    
    # Check training data
    hindi_loaded = bool(chatbot.hindi_data)
    english_loaded = bool(chatbot.english_data)
    
    # Check files
    hindi_files = os.path.exists("ramcharitmanas_training_data.json")
    english_files = os.path.exists("english_training_data.json")
    
    return {
        "status": "स्वस्थ / Healthy",
        "message": "🕉️ Bilingual Ramayan AI Chatbot Ready",
        "languages": {
            "hindi": {
                "status": "active" if hindi_loaded else "inactive",
                "source": "रामचरितमानस",
                "training_loaded": hindi_loaded,
                "files_available": hindi_files
            },
            "english": {
                "status": "active" if english_loaded else "inactive", 
                "source": "Valmiki Ramayana",
                "training_loaded": english_loaded,
                "files_available": english_files
            }
        },
        "features": [
            "Automatic language detection",
            "Bilingual response generation",
            "Cross-language story references",
            "Character analysis in both languages",
            "Story fact matching",
            "Cultural context preservation"
        ],
        "api_endpoints": [
            "POST /ask-bilingual - Bilingual questions",
            "POST /detect-language - Language detection",
            "GET /training-status - Training data status",
            "GET /sample-questions-bilingual - Sample questions",
            "GET /language-comparison - Version comparison"
        ],
        "total_content": {
            "hindi_pages": 1054,
            "english_pages": 1960,
            "total_characters": "2M+ characters extracted",
            "languages_supported": 2
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Bilingual Ramayan AI Server...")
    print("Languages: Hindi (Ramcharitmanas) + English (Valmiki Ramayana)")
    print("Training: 1054 + 1960 pages = 3014 total pages")
    print("Auto language detection enabled")
    print("Server: http://localhost:8001")
    print("API Docs: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)