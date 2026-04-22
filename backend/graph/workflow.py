from typing import Any, Dict


async def run_workflow(user_query: str) -> Dict[str, Any]:
    """Temporary workflow stub until LangGraph nodes are wired in."""
    cleaned_query = user_query.strip()

    if not cleaned_query:
        return {
            "ok": False,
            "message": "Query is empty. Please provide a shopping request.",
            "products": [],
        }

    return {
        "ok": True,
        "message": "Workflow placeholder response.",
        "query": cleaned_query,
        "products": [],
    }

