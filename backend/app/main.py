import json, os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv
load_dotenv()
from .db import Base, engine, get_db
from .models import Incident, Knowledge, Approval, User
from .workflow import run_workflow
from .auth import hash_password, verify_password, create_token, require_auth
from .observability import trace_event
Base.metadata.create_all(bind=engine)
app=FastAPI(title="DevSentry AI",version="2.0.0",description="LangGraph-based local-first AI incident intelligence")
origins=os.getenv("CORS_ORIGINS","http://localhost:5173,http://localhost:8080").split(",")
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=["*"],allow_headers=["*"])
class IncidentIn(BaseModel):
 title:str=Field(min_length=3,max_length=200);logs:str=Field(min_length=3);severity:str="medium"
class KnowledgeIn(BaseModel):
 title:str=Field(min_length=2,max_length=200);content:str=Field(min_length=10)
class DecisionIn(BaseModel):
 decision:str;note:str=""
class RegisterIn(BaseModel):
 email:EmailStr;password:str=Field(min_length=10)
class LoginIn(BaseModel):
 email:EmailStr;password:str
def serialize(x):
 return {"id":x.id,"title":x.title,"severity":x.severity,"status":x.status,"logs":x.logs,"summary":x.summary,"root_cause":x.root_cause,"recommendation":x.recommendation,"agent_trace":json.loads(x.trace or "[]"),"created_at":x.created_at.isoformat()}
@app.get("/api/health")
def health():return {"status":"healthy","mode":"local-first","auth_enabled":os.getenv("AUTH_ENABLED","false").lower()=="true","workflow":"LangGraph"}
@app.post("/api/auth/register")
def register(data:RegisterIn,db:Session=Depends(get_db)):
 email=data.email.lower()
 if db.query(User).filter_by(email=email).first():raise HTTPException(409,"Email already registered")
 u=User(email=email,password_hash=hash_password(data.password));db.add(u);db.commit();db.refresh(u)
 return {"access_token":create_token(u),"token_type":"bearer","email":u.email}
@app.post("/api/auth/login")
def login(data:LoginIn,db:Session=Depends(get_db)):
 u=db.query(User).filter_by(email=data.email.lower()).first()
 if not u or not verify_password(data.password,u.password_hash):raise HTTPException(401,"Invalid credentials")
 return {"access_token":create_token(u),"token_type":"bearer","email":u.email}
@app.get("/api/stats")
def stats(db:Session=Depends(get_db),user=Depends(require_auth)):
 return {"total_incidents":db.query(Incident).count(),"critical_incidents":db.query(Incident).filter_by(severity="critical").count(),"pending_approvals":db.query(Approval).filter_by(decision="pending").count(),"knowledge_documents":db.query(Knowledge).count()}
@app.get("/api/incidents")
def incidents(db:Session=Depends(get_db),user=Depends(require_auth)):return [serialize(x) for x in db.query(Incident).order_by(Incident.id.desc()).all()]
@app.post("/api/incidents")
def create_incident(data:IncidentIn,db:Session=Depends(get_db),user=Depends(require_auth)):
 if data.severity not in ["low","medium","high","critical"]:raise HTTPException(400,"Invalid severity")
 summary,root,recommendation,trace=run_workflow(data.title,data.logs,db.query(Knowledge).all())
 trace.append({"agent":"Human Review Gate","status":"waiting","output":"Recommendations require operator review; no production action is automated."})
 x=Incident(title=data.title,severity=data.severity,logs=data.logs,summary=summary,root_cause=root,recommendation=recommendation,trace=json.dumps(trace))
 db.add(x);db.commit();db.refresh(x);trace_event("incident_analysis",{"incident_id":x.id,"severity":x.severity})
 return serialize(x)
@app.get("/api/incidents/{iid}")
def incident(iid:int,db:Session=Depends(get_db),user=Depends(require_auth)):
 x=db.get(Incident,iid)
 if not x:raise HTTPException(404,"Incident not found")
 return serialize(x)
@app.post("/api/knowledge")
def add_knowledge(data:KnowledgeIn,db:Session=Depends(get_db),user=Depends(require_auth)):
 x=Knowledge(title=data.title,content=data.content);db.add(x);db.commit();db.refresh(x);return {"id":x.id,"title":x.title}
@app.get("/api/knowledge")
def knowledge(db:Session=Depends(get_db),user=Depends(require_auth)):return [{"id":x.id,"title":x.title,"content":x.content} for x in db.query(Knowledge).all()]
@app.post("/api/incidents/{iid}/approval")
def approve(iid:int,data:DecisionIn,db:Session=Depends(get_db),user=Depends(require_auth)):
 if data.decision not in ["approved","rejected"]:raise HTTPException(400,"Decision must be approved or rejected")
 x=db.get(Incident,iid)
 if not x:raise HTTPException(404,"Incident not found")
 x.status=data.decision;db.add(Approval(incident_id=iid,decision=data.decision,note=data.note));db.commit()
 return {"message":"Decision recorded","incident_id":iid}
@app.get("/api/approvals")
def approvals(db:Session=Depends(get_db),user=Depends(require_auth)):
 return [{"id":x.id,"incident_id":x.incident_id,"decision":x.decision,"note":x.note} for x in db.query(Approval).all()]
