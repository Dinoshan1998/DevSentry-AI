"""Read-only MCP tools for DevSentry. Start with: python mcp_server.py"""
import os, json
from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
DB=os.getenv("DATABASE_URL","sqlite:///devsentry.db")
engine=create_engine(DB)
mcp=FastMCP("DevSentry Read-only Operations")
@mcp.tool()
def list_incidents(limit:int=10)->str:
    """List recent incidents. Read-only; limit is capped at 50."""
    n=max(1,min(limit,50))
    with engine.connect() as c:
        rows=c.execute(text("SELECT id,title,severity,status,created_at FROM incidents ORDER BY id DESC LIMIT :n"),{"n":n}).mappings().all()
    return json.dumps([dict(r) for r in rows],default=str)
@mcp.tool()
def get_incident(incident_id:int)->str:
    """Read a single incident by ID. Does not execute remediation."""
    with engine.connect() as c:
        row=c.execute(text("SELECT id,title,severity,status,summary,root_cause,recommendation FROM incidents WHERE id=:id"),{"id":incident_id}).mappings().first()
    return json.dumps(dict(row),default=str) if row else "Incident not found"
if __name__=="__main__":mcp.run()
