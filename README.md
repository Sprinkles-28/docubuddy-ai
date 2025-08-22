# 📄 DocuBuddy AI

DocuBuddy AI is an **AI-powered assistant** designed to help employees quickly find answers to queries from their company’s internal documents.  
Built during the **AI Agent Hackathon (2025) by Product Space**, it leverages **GPT-3.5** and **Natural Language Processing (NLP)** to deliver context-aware responses.

---

## Features
- 🔍 **Smart Query Handling**: Ask natural language questions, get precise answers from internal docs.  
- 📂 **Document Ingestion**: Supports PDFs, DOCX, and TXT for knowledge base creation.  
- ⚡ **AI-Powered**: Uses GPT-3.5 with NLP preprocessing for accurate, context-driven responses.  
- 🌐 **User-Friendly UI**: Simple React frontend for seamless interaction.  
- 🔑 **Secure Backend**: API key handling and query processing with Python (Flask).  

---

##  Tech Stack
- **Frontend**: React + Tailwind CSS  
- **Backend**: Python (Flask/FastAPI)  
- **AI Model**: OpenAI GPT-3.5  
- **NLP Tools**: spaCy, NLTK (for preprocessing)    
- **Authentication**: API key handling  

---

## Project Structure
```
DocuBuddyAI/
│── frontend/               # React UI
│── backend/                # Flask/FastAPI backend
│ ├── app.py/               # Endpoints, Query and NLP Logic
│── company_policies.txt/   # Sample documents
│── README.md               # Project documentation
```

##  Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/docubuddy-ai.git
cd docubuddy-ai
```

### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm start
```

### 4. Add OpenAI API Key
Create a .env file in backend/:
```
OPENAI_API_KEY=your_api_key_here
```

## Future Enhancements
✅ Multi-language document support

✅ Role-based access for enterprise use

✅ Integration with Slack / Teams

✅ Fine-tuning with domain-specific data


## 🏆 Acknowledgement
Built during AI Agent Hackathon 2025 as a solo project to explore AI + NLP for workplace productivity.
