import json
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.src.schemas import ResearchRequest, ResearchResponse
from backend.src.graph import build_aura_graph
from backend.src.db.session import get_db
from backend.src.db.models import ResearchRun

router = APIRouter()

# Instantiate the compiled LangGraph workflow once at module level
aura_graph = build_aura_graph()


@router.get("/health")
async def health_check():
    """Health check probe to verify the backend server is running and ready."""
    return {
        "status": "online",
        "service": "AURA Multi-Agent Research Assistant",
        "version": "1.0.0"
    }


@router.post("/research")
async def conduct_research(payload: ResearchRequest, db: Session = Depends(get_db)):
    """
    Main research endpoint:
    1. Receives user query.
    2. Runs the multi-agent LangGraph workflow.
    3. Measures execution duration.
    4. Automatically saves run to SQLite history database.
    5. Returns full structured report and telemetry.
    """
    start_time = time.time()
    
    initial_state = {
        "original_query": payload.query,
        "plan": None,
        "subtasks": [],
        "research_results": [],
        "analysis": "",
        "evaluation": None,
        "iteration_count": 0,
        "final_answer": ""
    }
    
    try:
        # Execute the autonomous graph workflow
        final_state = aura_graph.invoke(initial_state)
        duration = round(time.time() - start_time, 2)
        
        # Serialize structured components
        plan_obj = final_state.get("plan")
        plan_dict = plan_obj.model_dump() if hasattr(plan_obj, "model_dump") else plan_obj
        
        eval_obj = final_state.get("evaluation")
        eval_dict = eval_obj.model_dump() if hasattr(eval_obj, "model_dump") else eval_obj
        
        sources_list = final_state.get("research_results", [])
        final_ans = final_state.get("final_answer", "")
        iters = final_state.get("iteration_count", 1)

        # Save record to SQLite
        db_run = ResearchRun(
            query=final_state["original_query"],
            response=final_ans,
            plan_json=json.dumps(plan_dict) if plan_dict else None,
            sources_json=json.dumps(sources_list) if sources_list else None,
            evaluation_json=json.dumps(eval_dict) if eval_dict else None,
            iteration_count=iters
        )
        db.add(db_run)
        db.commit()
        db.refresh(db_run)

        return {
            "id": db_run.id,
            "query": final_state["original_query"],
            "plan": plan_dict,
            "subtasks": final_state.get("subtasks", []),
            "sources": sources_list,
            "research_results": sources_list,
            "analysis": final_state.get("analysis", ""),
            "response": final_ans,
            "final_answer": final_ans,
            "evaluation": eval_dict,
            "iteration_count": iters,
            "execution_time_seconds": duration,
            "created_at": db_run.created_at.isoformat() if db_run.created_at else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-agent workflow execution failed: {str(e)}"
        )


@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """Retrieve all past research runs ordered chronologically (newest first)."""
    runs = db.query(ResearchRun).order_by(ResearchRun.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "query": r.query,
            "iteration_count": r.iteration_count,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in runs
    ]


@router.get("/history/{run_id}")
async def get_history_item(run_id: str, db: Session = Depends(get_db)):
    """Retrieve full details of a specific past research run."""
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Research run not found")
    
    return {
        "id": run.id,
        "query": run.query,
        "response": run.response,
        "final_answer": run.response,
        "plan": json.loads(run.plan_json) if run.plan_json else None,
        "sources": json.loads(run.sources_json) if run.sources_json else [],
        "evaluation": json.loads(run.evaluation_json) if run.evaluation_json else None,
        "iteration_count": run.iteration_count,
        "created_at": run.created_at.isoformat() if run.created_at else None,
    }


@router.delete("/history/{run_id}")
async def delete_history_item(run_id: str, db: Session = Depends(get_db)):
    """Delete a past research run."""
    run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Research run not found")
    db.delete(run)
    db.commit()
    return {"deleted": True, "id": run_id}
