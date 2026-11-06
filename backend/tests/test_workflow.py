from app.workflow import run_workflow
def test_langgraph_pipeline():
    summary,root,recommendation,trace=run_workflow("DB outage","database connection refused",[])
    assert "database" in root.lower()
    assert recommendation
    assert len(trace)>=4
