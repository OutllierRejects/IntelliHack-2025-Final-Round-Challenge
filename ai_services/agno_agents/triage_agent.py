# ai_services/agno_agents/triage_agent.py

def triage_incident(description: str) -> str:
    """Simple triage based on keywords — simulate AI agent."""
    if any(word in description.lower() for word in ["urgent", "fire", "injury", "explosion"]):
        return "high"
    elif any(word in description.lower() for word in ["delay", "minor", "slow", "confused"]):
        return "low"
    return "medium"
