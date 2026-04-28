import os
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from datetime import date, time
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import HCP, Product, Interaction
from sqlalchemy.orm import Session

# --- State Definition ---

class AgentState(TypedDict):
    """The state of our agent."""
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    form_data: Dict[str, Any]
    available_hcps: List[Dict[str, Any]]
    available_products: List[Dict[str, Any]]

# --- Tools Implementation ---

@tool
def get_hcp_list():
    """Fetches the list of available Healthcare Professionals (HCPs) from the database."""
    db = SessionLocal()
    try:
        hcps = db.query(HCP).all()
        return [{"id": h.id, "name": h.name, "specialty": h.specialty} for h in hcps]
    finally:
        db.close()

@tool
def get_product_list():
    """Fetches the list of available products from the database."""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        return [{"id": p.id, "name": p.name} for p in products]
    finally:
        db.close()

@tool
def log_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    date_str: Optional[str] = None, # YYYY-MM-DD
    time_str: Optional[str] = None, # HH:MM
    attendees: Optional[List[str]] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[List[str]] = None,
    samples_distributed: Optional[List[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[str] = None
):
    """
    Extracts information from a natural language prompt to populate the interaction form.
    Use this when the user describes a new interaction they want to log.
    """
    # This tool is primarily a schema for the LLM to fill.
    # The actual 'filling' happens by the LLM generating the arguments.
    # We return the arguments so they can be merged into the form_data state.
    return {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type,
        "date": date_str,
        "time": time_str,
        "attendees": attendees,
        "topics_discussed": topics_discussed,
        "materials_shared": materials_shared,
        "samples_distributed": samples_distributed,
        "sentiment": sentiment,
        "outcomes": outcomes,
        "follow_up_actions": follow_up_actions
    }

@tool
def edit_interaction(field_name: str, new_value: Any):
    """
    Updates a specific field in the current interaction form.
    Use this when the user wants to correct or change a specific piece of information.
    Field names can be: hcp_name, interaction_type, date, time, attendees, topics_discussed, 
    materials_shared, samples_distributed, sentiment, outcomes, follow_up_actions.
    """
    return {field_name: new_value}

@tool
def submit_interaction(interaction_data: Dict[str, Any]):
    """
    Finalizes and saves the interaction form to the database.
    Use this only when the user explicitly asks to 'save', 'submit', or 'finish' the logging process.
    """
    db = SessionLocal()
    try:
        # Resolve HCP name to ID
        hcp = db.query(HCP).filter(HCP.name == interaction_data.get("hcp_name")).first()
        if not hcp:
            return f"Error: Could not find HCP named {interaction_data.get('hcp_name')}"
        
        new_interaction = Interaction(
            hcp_id=hcp.id,
            interaction_type=interaction_data.get("interaction_type"),
            date=date.fromisoformat(interaction_data.get("date")) if interaction_data.get("date") else None,
            time=time.fromisoformat(interaction_data.get("time")) if interaction_data.get("time") else None,
            attendees=interaction_data.get("attendees", []),
            topics_discussed=interaction_data.get("topics_discussed"),
            materials_shared=interaction_data.get("materials_shared", []),
            samples_distributed=interaction_data.get("samples_distributed", []),
            sentiment=interaction_data.get("sentiment"),
            outcomes=interaction_data.get("outcomes"),
            follow_up_actions=interaction_data.get("follow_up_actions")
        )
        db.add(new_interaction)
        db.commit()
        return "Successfully saved the interaction to the database."
    except Exception as e:
        db.rollback()
        return f"Error saving interaction: {str(e)}"
    finally:
        db.close()

# --- Agent Logic ---

tools = [get_hcp_list, get_product_list, log_interaction, edit_interaction, submit_interaction]
tool_node = ToolNode(tools)

model = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0
).bind_tools(tools)

def call_model(state: AgentState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_agent = workflow.compile()
