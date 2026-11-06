import os, re, requests
from dotenv import load_dotenv
load_dotenv()
PATTERNS={"database":["connection refused","too many connections","database is locked","could not connect","connection pool"],"memory":["out of memory","memoryerror","oomkilled"],"network":["connection reset","dns failure","network unreachable","tls handshake"],"auth":["unauthorized","forbidden","invalid token","authentication failed","401","403"],"application":["traceback","exception","typeerror","valueerror","internal server error","500"]}
FIXES={"database":"Check database health, hostname/port, connection pool saturation, network route and recent configuration changes. Verify secrets through your secret manager.","memory":"Inspect memory metrics, container limits, heap profiles, traffic spikes and recent deployments. Reproduce in a test environment before changing limits.","network":"Check DNS, service health, TLS certificates, firewall rules and network policies. Compare failures across instances.","auth":"Check token expiry, issuer/audience, clock skew and role permissions. Never log or paste access tokens.","application":"Inspect the stack trace and recent code changes. Reproduce in a test environment, add a regression test, then review a minimal fix.","unknown":"Collect timestamped logs, request IDs, service health and recent deployment details before changing production."}
def category_for(logs):
 low=logs.lower(); counts={k:sum(low.count(p) for p in vals) for k,vals in PATTERNS.items()}; best=max(counts,key=counts.get)
 return (best if counts[best] else "unknown"),counts
def retrieve(logs,docs):
 terms=set(re.findall(r"[a-zA-Z_]{3,}",logs.lower())); ranked=[]
 for d in docs:
  words=set(re.findall(r"[a-zA-Z_]{3,}",(d.title+" "+d.content).lower()));score=len(terms&words)
  if score: ranked.append((score,d))
 ranked.sort(key=lambda x:x[0],reverse=True);return [d for _,d in ranked[:3]]
def ollama(prompt):
 if os.getenv("USE_OLLAMA","false").lower()!="true": return None
 try:
  url=os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")+"/api/generate"
  r=requests.post(url,json={"model":os.getenv("OLLAMA_MODEL","qwen2.5:3b"),"prompt":prompt,"stream":False},timeout=120);r.raise_for_status()
  return r.json().get("response","").strip() or None
 except Exception:return None
