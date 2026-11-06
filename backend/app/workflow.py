from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from .engine import category_for, retrieve, FIXES, ollama
class IncidentState(TypedDict, total=False):
    title:str; logs:str; docs:list; category:str; counts:dict; retrieved:list
    root_cause:str; summary:str; recommendation:str; trace:list
def log_analysis(s:IncidentState):
    cat,counts=category_for(s["logs"])
    return {"category":cat,"counts":counts,"trace":[{"agent":"Log Analysis Agent","status":"completed","output":f"Detected {cat}; pattern counts {counts}"}]}
def knowledge_retrieval(s:IncidentState):
    docs=retrieve(s["logs"],s.get("docs",[]))
    return {"retrieved":docs,"trace":[{"agent":"Knowledge Retrieval Agent","status":"completed","output":f"Retrieved {len(docs)} matching runbooks."}]}
def root_cause(s:IncidentState):
    labels={"database":"Database connectivity or pool saturation is suspected.","memory":"Memory pressure or out-of-memory is suspected.","network":"Network, DNS or TLS connectivity is suspected.","auth":"Authentication or authorization failure is suspected.","application":"An application exception is suspected.","unknown":"Evidence is insufficient for a confident root-cause hypothesis."}
    return {"root_cause":labels[s["category"]],"trace":[{"agent":"Root Cause Agent","status":"completed","output":labels[s["category"]]}]}
def llm_synthesis(s:IncidentState):
    context="\n".join(d.title+": "+d.content[:600] for d in s.get("retrieved",[])) or "No runbook match."
    prompt=f"Act as cautious SRE. Give evidence-based incident summary and actions. Do not invent facts. Title:{s['title']}\nLogs:{s['logs'][:6000]}\nRunbooks:{context}"
    generated=ollama(prompt)
    summary=generated or f"{s['title']}. Rule-based analysis detected {s['category']}. Validate using metrics and deployment history."
    rec=FIXES[s["category"]]
    if s.get("retrieved"): rec += "\nRelated runbook:\n"+context
    return {"summary":summary,"recommendation":rec,"trace":[{"agent":"LLM Synthesis Agent","status":"completed","output":"Local Ollama" if generated else "Transparent deterministic fallback"}]}
def build_graph():
    g = StateGraph(IncidentState)

    g.add_node("log_analysis", log_analysis)
    g.add_node("knowledge_retrieval", knowledge_retrieval)
    g.add_node("root_cause_agent", root_cause)
    g.add_node("llm_synthesis", llm_synthesis)

    g.set_entry_point("log_analysis")

    g.add_edge("log_analysis", "knowledge_retrieval")
    g.add_edge("knowledge_retrieval", "root_cause_agent")
    g.add_edge("root_cause_agent", "llm_synthesis")
    g.add_edge("llm_synthesis", END)

    return g.compile()
GRAPH=build_graph()
def run_workflow(title,logs,docs):
    result=GRAPH.invoke({"title":title,"logs":logs,"docs":docs,"trace":[]})
    return result["summary"],result["root_cause"],result["recommendation"],result["trace"]
