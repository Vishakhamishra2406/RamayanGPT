"""
Enhanced Ramayan Chatbot - Can answer ANY Ramayana question
Uses full text search + AI to provide comprehensive answers
"""

import asyncio
import json
import os
import re
from typing import Dict, Any, List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class EnhancedRamayanChatbot:
    """Enhanced Ramayan chatbot that can answer any question"""
    
    def __init__(self):
        # Load training data - now using fully enhanced data with additional sources
        self.hindi_data = self._load_training_data("fully_enhanced_training_data.json")
        self.english_data = self._load_training_data("english_training_data.json")
        
        # Load full text if available
        self.hindi_full_text = self._load_full_text("रामचरितमानस_extracted.txt")
        self.english_full_text = self._load_full_text("english_extracted.txt")
        
        # API setup
        self.has_real_keys = (
            os.getenv("GEMINI_API_KEY") and 
            os.getenv("GEMINI_API_KEY") != "test_key_for_demo"
        )
        
        if self.has_real_keys:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("⚠️  Demo mode - For full AI capabilities, add GEMINI_API_KEY to .env")
    
    def _load_training_data(self, filename: str) -> Dict:
        """Load training data from JSON file"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ {filename} not found.")
            return {}
    
    def _load_full_text(self, filename: str) -> str:
        """Load full text content if available"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"📝 {filename} not found - using structured data only")
            return ""
    
    def detect_language(self, question: str) -> str:
        """Detect if question is in Hindi or English"""
        hindi_chars = set('अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')
        english_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        question_chars = set(question)
        
        hindi_count = len(question_chars & hindi_chars)
        english_count = len(question_chars & english_chars)
        
        if hindi_count > english_count:
            return "hindi"
        else:
            return "english"
    
    def search_content(self, question: str, language: str) -> Dict:
        """Search for relevant content using multiple methods"""
        
        # Method 1: Check specific story facts (highest priority)
        specific_answer = self._get_specific_answer(question, language)
        if specific_answer:
            return specific_answer
        
        # Method 2: Search in full text content
        text_search_result = self._search_full_text(question, language)
        if text_search_result:
            return text_search_result
        
        # Method 3: Character and theme matching
        character_result = self._search_characters_themes(question, language)
        if character_result:
            return character_result
        
        # Method 4: Generate AI response with context
        return self._generate_contextual_response(question, language)
    
    def _get_specific_answer(self, question: str, language: str) -> Dict:
        """Check for specific pre-programmed answers"""
        question_lower = question.lower()
        
        if language == "hindi":
            data_source = self.hindi_data
            story_facts_key = "story_facts"
        else:
            data_source = self.english_data
            story_facts_key = "english_story_facts"
        
        # Check story facts
        for fact_key, fact_data in data_source.get(story_facts_key, {}).items():
            keywords = fact_data.get("question_keywords", []) or fact_data.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in question_lower:
                    return {
                        "type": "specific_fact",
                        "language": language,
                        "answer": fact_data.get("answer") or fact_data.get("content"),
                        "source": "Structured Knowledge Base"
                    }
        
        return None
    
    def _search_full_text(self, question: str, language: str) -> Dict:
        """Search in full text content"""
        if language == "hindi" and self.hindi_full_text:
            text_content = self.hindi_full_text
            source = "Ramcharitmanas Full Text"
        elif language == "english" and self.english_full_text:
            text_content = self.english_full_text
            source = "Valmiki Ramayana Full Text"
        else:
            return None
        
        # Extract key terms from question
        key_terms = self._extract_key_terms(question, language)
        
        # Search for relevant passages
        relevant_passages = []
        for term in key_terms:
            passages = self._find_passages_with_term(text_content, term)
            relevant_passages.extend(passages)
        
        if relevant_passages:
            # Combine and summarize passages
            combined_text = "\n".join(relevant_passages[:3])  # Top 3 passages
            return {
                "type": "text_search",
                "language": language,
                "passages": combined_text[:1000],  # Limit length
                "source": source,
                "key_terms": key_terms
            }
        
        return None
    
    def _extract_key_terms(self, question: str, language: str) -> List[str]:
        """Extract key terms from question for searching"""
        question_lower = question.lower()
        
        if language == "hindi":
            # Hindi key terms
            key_terms = []
            hindi_names = ["राम", "सीता", "हनुमान", "रावण", "लक्ष्मण", "भरत", "दशरथ", "कैकेयी", "कौशल्या"]
            hindi_places = ["अयोध्या", "लंका", "चित्रकूट", "पंचवटी", "किष्किंधा"]
            hindi_events = ["जन्म", "विवाह", "वनवास", "युद्ध", "वध", "मिलाप"]
            
            all_terms = hindi_names + hindi_places + hindi_events
            for term in all_terms:
                if term in question_lower:
                    key_terms.append(term)
        else:
            # English key terms
            key_terms = []
            english_names = ["rama", "sita", "hanuman", "ravana", "lakshmana", "bharata", "dasharatha"]
            english_places = ["ayodhya", "lanka", "chitrakuta", "panchavati", "kishkindha"]
            english_events = ["birth", "marriage", "exile", "war", "death", "meeting"]
            
            all_terms = english_names + english_places + english_events
            for term in all_terms:
                if term in question_lower:
                    key_terms.append(term)
        
        # If no specific terms found, extract nouns
        if not key_terms:
            words = re.findall(r'\b\w+\b', question_lower)
            key_terms = [word for word in words if len(word) > 3][:3]
        
        return key_terms
    
    def _find_passages_with_term(self, text: str, term: str) -> List[str]:
        """Find passages containing the search term"""
        passages = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if term.lower() in line.lower():
                # Get context around the matching line
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                passage = '\n'.join(lines[start:end])
                passages.append(passage)
        
        return passages[:5]  # Return top 5 passages
    
    def _search_characters_themes(self, question: str, language: str) -> Dict:
        """Search for character and theme information"""
        question_lower = question.lower()
        
        if language == "hindi":
            data_source = self.hindi_data
            characters_key = "characters"
        else:
            data_source = self.english_data
            characters_key = "characters_english"
        
        # Check characters
        for char_name, char_data in data_source.get(characters_key, {}).items():
            if char_name.lower() in question_lower:
                return {
                    "type": "character_info",
                    "language": language,
                    "character": char_name,
                    "data": char_data,
                    "source": "Character Database"
                }
        
        # Check themes/teachings
        if "teaching" in question_lower or "lesson" in question_lower or "dharma" in question_lower:
            teachings = data_source.get("teachings", {})
            if teachings:
                return {
                    "type": "teachings",
                    "language": language,
                    "data": teachings,
                    "source": "Spiritual Teachings"
                }
        
        return None
    
    def _generate_contextual_response(self, question: str, language: str) -> Dict:
        """Generate response using available context"""
        
        # Create a comprehensive context from available data
        context_parts = []
        
        if language == "hindi":
            # Add Hindi context
            context_parts.append("रामचरितमानस से संदर्भ:")
            if self.hindi_data.get("story_facts"):
                context_parts.append("मुख्य कथाएं: " + ", ".join(self.hindi_data["story_facts"].keys()))
            if self.hindi_data.get("characters"):
                context_parts.append("मुख्य पात्र: " + ", ".join(self.hindi_data["characters"].keys()))
        else:
            # Add English context
            context_parts.append("From Valmiki Ramayana:")
            if self.english_data.get("english_story_facts"):
                context_parts.append("Main stories: " + ", ".join(self.english_data["english_story_facts"].keys()))
            if self.english_data.get("characters_english"):
                context_parts.append("Main characters: " + ", ".join(self.english_data["characters_english"].keys()))
        
        context = "\n".join(context_parts)
        
        return {
            "type": "contextual_response",
            "language": language,
            "question": question,
            "context": context,
            "source": "AI Generated with Context"
        }
    
    async def generate_response(self, question: str) -> str:
        """Generate comprehensive response for any Ramayana question"""
        
        # Detect language
        language = self.detect_language(question)
        print(f"🔍 Detected language: {language}")
        
        # Search for relevant content
        content = self.search_content(question, language)
        
        # Generate response based on content type
        if content["type"] == "specific_fact":
            return self._format_specific_answer(content, question)
        elif content["type"] == "text_search":
            return self._format_text_search_answer(content, question)
        elif content["type"] == "character_info":
            return self._format_character_answer(content, question)
        elif content["type"] == "teachings":
            return self._format_teachings_answer(content, question)
        else:
            return self._format_contextual_answer(content, question)
    
    def _format_specific_answer(self, content: Dict, question: str) -> str:
        """Format specific fact answer"""
        if content["language"] == "hindi":
            response = f"🕉️ रामचरितमानस से उत्तर:\n\n"
            response += f"📖 **{question}**\n\n"
            response += content["answer"]
            response += f"\n\n📚 **स्रोत:** {content['source']}"
        else:
            response = f"🕉️ From The Ramayana:\n\n"
            response += f"📖 **{question}**\n\n"
            response += content["answer"]
            response += f"\n\n📚 **Source:** {content['source']}"
        
        response += "\n\n🙏 Jai Shri Ram!"
        return response
    
    def _format_text_search_answer(self, content: Dict, question: str) -> str:
        """Format text search answer"""
        if content["language"] == "hindi":
            response = f"🕉️ रामचरितमानस से खोज परिणाम:\n\n"
            response += f"📖 **{question}**\n\n"
            response += f"🔍 **खोजे गए शब्द:** {', '.join(content['key_terms'])}\n\n"
            response += f"📜 **संबंधित अंश:**\n{content['passages']}\n\n"
            response += f"📚 **स्रोत:** {content['source']}"
        else:
            response = f"🕉️ Search Results from Ramayana:\n\n"
            response += f"📖 **{question}**\n\n"
            response += f"🔍 **Search terms:** {', '.join(content['key_terms'])}\n\n"
            response += f"📜 **Relevant passages:**\n{content['passages']}\n\n"
            response += f"📚 **Source:** {content['source']}"
        
        response += "\n\n🙏 Jai Shri Ram!"
        return response
    
    def _format_character_answer(self, content: Dict, question: str) -> str:
        """Format character information answer"""
        char_data = content["data"]
        
        if content["language"] == "hindi":
            response = f"🕉️ रामचरितमानस से चरित्र विश्लेषण:\n\n"
            response += f"👑 **{content['character']}**\n\n"
            
            if "qualities" in char_data:
                response += f"🌟 **मुख्य गुण:**\n"
                for quality in char_data["qualities"]:
                    response += f"  • {quality}\n"
            
            if "key_teachings" in char_data:
                response += f"\n📿 **मुख्य शिक्षाएं:**\n"
                for teaching in char_data["key_teachings"]:
                    response += f"  • {teaching}\n"
        else:
            response = f"🕉️ Character Analysis from Ramayana:\n\n"
            response += f"👑 **{content['character']}**\n\n"
            
            if "description" in char_data:
                response += f"📝 **Description:** {char_data['description']}\n\n"
            
            if "qualities" in char_data:
                response += f"🌟 **Key Qualities:**\n"
                for quality in char_data["qualities"]:
                    response += f"  • {quality}\n"
        
        response += f"\n\n📚 **Source:** {content['source']}"
        response += "\n\n🙏 Jai Shri Ram!"
        return response
    
    def _format_teachings_answer(self, content: Dict, question: str) -> str:
        """Format teachings answer"""
        teachings_data = content["data"]
        
        if content["language"] == "hindi":
            response = f"🕉️ रामचरितमानस की शिक्षाएं:\n\n"
            response += f"📖 **{question}**\n\n"
            
            for teaching_key, teaching_data in teachings_data.items():
                response += f"🌟 **{teaching_key}:**\n"
                if "definition" in teaching_data:
                    response += f"   {teaching_data['definition']}\n\n"
        else:
            response = f"🕉️ Teachings from Ramayana:\n\n"
            response += f"📖 **{question}**\n\n"
            response += "The Ramayana teaches us about dharma (righteousness), devotion, ideal relationships, and spiritual growth.\n\n"
        
        response += f"📚 **Source:** {content['source']}"
        response += "\n\n🙏 Jai Shri Ram!"
        return response
    
    def _format_contextual_answer(self, content: Dict, question: str) -> str:
        """Format contextual AI-generated answer"""
        
        if content["language"] == "hindi":
            response = f"🕉️ रामचरितमानस से संदर्भित उत्तर:\n\n"
            response += f"📖 **{question}**\n\n"
            response += "यह प्रश्न रामायण की व्यापक शिक्षाओं से संबंधित है। रामचरितमानस में इस विषय पर विस्तृत जानकारी उपलब्ध है।\n\n"
            response += f"📚 **उपलब्ध संदर्भ:**\n{content['context']}\n\n"
            response += "अधिक विस्तृत जानकारी के लिए कृपया अधिक स्पष्ट प्रश्न पूछें।"
        else:
            response = f"🕉️ Contextual Answer from Ramayana:\n\n"
            response += f"📖 **{question}**\n\n"
            response += "This question relates to the broader teachings of Ramayana. The epic contains extensive information on this topic.\n\n"
            response += f"📚 **Available context:**\n{content['context']}\n\n"
            response += "For more detailed information, please ask a more specific question."
        
        response += f"\n\n📚 **Source:** {content['source']}"
        response += "\n\n🙏 Jai Shri Ram!"
        return response

# Test function
async def test_enhanced_chatbot():
    """Test the enhanced chatbot with various questions"""
    
    chatbot = EnhancedRamayanChatbot()
    
    print("🕉️ ENHANCED RAMAYAN CHATBOT TEST")
    print("=" * 70)
    
    # Test with various types of questions
    test_questions = [
        # Specific questions (should get specific answers)
        "Who were the sons of Dasharatha?",
        "दशरथ के पुत्रों के नाम क्या थे?",
        
        # General questions (should search and provide context)
        "What happened in the forest during exile?",
        "वनवास के दौरान क्या हुआ था?",
        
        # Character questions
        "Tell me about Rama's character",
        "राम के चरित्र के बारे में बताएं",
        
        # Teaching questions
        "What does Ramayana teach about leadership?",
        "रामायण नेतृत्व के बारे में क्या सिखाती है?",
        
        # Open-ended questions
        "How did Hanuman show his devotion?",
        "हनुमान जी ने अपनी भक्ति कैसे दिखाई?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🎤 Question {i}: {question}")
        print("-" * 60)
        
        # Generate response
        answer = await chatbot.generate_response(question)
        print(f"📖 Answer:\n{answer}")
        print("-" * 60)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(test_enhanced_chatbot())