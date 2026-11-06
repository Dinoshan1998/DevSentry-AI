# DevSentry AI — முழுமையான தமிழ் Run & Deploy Guide

## 1. தேவையான இலவச software
- Python 3.11+
- Node.js 20+
- VS Code
- Git (GitHub-க்கு upload செய்ய)
- Docker Desktop (விருப்பம்)
- Ollama (Local generative AI விருப்பம்)

Paid API key, paid database அல்லது paid embedding service எதுவும் தேவையில்லை.

## 2. ZIP extract
ZIP file-ஐ Extract All செய்து `DevSentry-AI` folder-ஐ VS Code-ல் Open Folder செய்யவும். இரண்டு terminal திறக்கவும்.

## 3. Backend run
முதல் terminal-ல் project root-இலிருந்து:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
PowerShell activate policy error வந்தால்:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
பிறகு `http://127.0.0.1:8000/docs` திறந்து API இயங்குகிறதா பார்க்கவும்.

## 4. Frontend run
இரண்டாவது terminal:
```powershell
cd frontend
npm install
npm run dev
```
Browser-ல் `http://localhost:5173` திறக்கவும்.

## 5. முதல் demo
1. Overview dashboard திறக்கவும்.
2. Analyze logs கிளிக் செய்யவும்.
3. Default sample logs அப்படியே வைத்து Run AI analysis அழுத்தவும்.
4. Incident detail-ல் AI summary, root cause, recommendation மற்றும் agent trace வரும்.
5. Recommendation-ஐ சரிபார்த்த பிறகே Approve / Reject செய்யவும்.
6. Knowledge base-ல் runbook சேர்த்து புதிய incident analysis செய்யவும்.

## 6. Optional: Ollama local AI setup
1. https://ollama.com இலிருந்து Ollama install செய்யவும்.
2. PowerShell-ல் `ollama pull qwen2.5:3b` run செய்யவும்.
3. Model download ஆனதும் project-ல் `backend/.env` என்ற file உருவாக்கி:
```env
USE_OLLAMA=true
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_BASE_URL=http://localhost:11434
```
4. Backend terminal-ஐ stop செய்து மீண்டும் start செய்யவும்.
Ollama local-ஆக model run செய்கிறது; API கட்டணம் இல்லை. ஆனால் model download-க்கு internet மற்றும் பல GB disk space தேவை. RAM/CPU-ஐப் பொறுத்து வேகம் மாறும். Ollama இயங்காவிட்டால் app fallback analysis-க்கு திரும்பும்.

## 7. Docker run
Docker Desktop install செய்து open செய்யவும். Project root terminal:
```powershell
docker compose up --build
```
Frontend: `http://localhost:8080`
Backend docs: `http://localhost:8000/docs`
Stop: `docker compose down`
Database volume-ஐயும் அழிக்க: `docker compose down -v` (இதனால் saved incidents அழியும்).

## 8. GitHub upload
GitHub-ல் `DevSentry-AI` என்ற புதிய repository உருவாக்கவும். Root terminal:
```powershell
git init
git add .
git commit -m "Initial DevSentry AI platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/DevSentry-AI.git
git push -u origin main
```
`YOUR_USERNAME` இடத்தில் உன் GitHub username இடவும். `.env`, database, tokens அல்லது secrets upload செய்ய வேண்டாம்.

## 9. Free deployment உண்மை நிலை
- உன் சொந்த PC-ல் run செய்வதும் Docker local deployment-மும் முழுமையாக இலவசம்.
- Public cloud free tiers-ல் sleep, RAM, bandwidth, persistent storage limits இருக்கும்; provider terms மாறலாம்.
- Ollama model-ஐ shared free hosting-ல் இயக்குவது பொதுவாக சாத்தியமற்றது/மெதுவானது. Local AI-ஐ உன் PC-ல் வைத்திருப்பதே zero-cost வழி.
- Portfolio-க்கு local live demo, screen recording, GitHub README மற்றும் architecture screenshots நம்பகமான free approach.
- Public backend deploy செய்தால் `VITE_API_URL`-ஐ public API URL-ஆக frontend build செய்ய வேண்டும்; backend CORS-ல் frontend domain சேர்க்க வேண்டும். இந்த Docker config localhost demo-க்காக.
- Free hosting-ல் SQLite data அழியக்கூடும்; persistent disk இல்லாமல் deploy செய்ய வேண்டாம்.

## 10. Test
Backend terminal:
```powershell
cd backend
pytest
```

## 11. Interview-ல் project-ஐ explain செய்வது
- FastAPI + React + SQLite கொண்டு local-first incident intelligence platform உருவாக்கினேன்.
- Log classification, local knowledge retrieval, root-cause hypothesis மற்றும் remediation planning கொண்ட multi-step agent workflow உருவாக்கினேன்.
- Optional local inference-க்கு Ollama பயன்படுத்தினேன்; paid LLM API dependency இல்லை.
- Human approval flow சேர்த்தேன்; production commands தானாக execute ஆகாது.
- தற்போதைய retrieval keyword-overlap baseline; இது இன்னும் production-grade vector RAG அல்ல. இது limitation என்பதை தெளிவாகச் சொல்ல வேண்டும்.

## 12. அடுத்த development upgrades
1. JWT authentication மற்றும் role-based access.
2. Local sentence-transformers + FAISS embeddings.
3. LangGraph orchestration.
4. Langfuse tracing மற்றும் RAG evaluation dataset.
5. ML anomaly detection-க்கு labelled sample data.
6. MCP server-ல் allowlisted read-only tools.
7. Unit/integration tests, rate limiting, audit log, secure file upload.
