import os
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from datetime import date, time
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import HCP, Product, Interaction

# --- State Definition ---

class AgentState(TypedDict):
    """The state of our agent."""
    # add_messages ensures that new messages are appended to the list instead of replacing it
    messages: Annotated[List[BaseMessage], add_messages]
    form_data: Dict[str, Any]
    available_hcps: List[Dict[str, Any]]
    available_products: List[Dict[str, Any]]

# --- System Prompt ---
SYSTEM_PROMPT = """You are an Autonomous CRM Assistant. You control a web form on the left side of the screen via tools.

YOUR MISSION:
1. Extract interaction details from user text and auto-fill the form.
2. Perform surgical edits to specific form fields when requested.
3. Answer questions about available HCPs (Doctors) and Products.

STRICT RULES:
- TOOL USAGE: You MUST use tools to perform actions. 
- GETTING DATA: If asked "Who are the doctors?" or "What products?", call 'get_hcp_list' or 'get_product_list' IMMEDIATELY. Do not answer from memory.
- LOGGING: If a user describes an interaction (e.g. "I met Dr. Smith..."), you MUST call 'log_interaction'.
- EDITING: If a user wants to change one thing (e.g. "Change sentiment to positive"), you MUST call 'edit_interaction'.
- SUBMITTING: If the user says "Save", "Submit", or "I'm done", you MUST call 'submit_interaction'.

CONTEXT:
Current Form State: {form_state}
Available HCPs in DB: {hcp_list}
Available Products in DB: {product_list}

NEVER hallucinate data. If you don't know something, ask. If you have called a tool, tell the user what you updated."""

# --- Tools Implementation ---

@tool
def get_hcp_list():
    """Fetches the list of available Healthcare Professionals (HCPs) from the database."""
    db = SessionLocal()
    try:
        hcps = db.query(HCP).all()
        return [{"name": h.name, "specialty": h.specialty} for h in hcps]
    finally:
        db.close()

@tool
def get_product_list():
    """Fetches the list of available products from the database."""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        return [{"name": p.name} for p in products]
    finally:
        db.close()

@tool
def log_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    date_str: Optional[str] = None, 
    time_str: Optional[str] = None, 
    attendees: Optional[List[str]] = None,
    topics_discussed: Optional[str] = None,
    materials_shared: Optional[List[str]] = None,
    samples_distributed: Optional[List[str]] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    follow_up_actions: Optional[str] = None
):
    """Call this when the user provides details about a meeting, call, or interaction to auto-fill the form."""
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
    """Call this to update exactly ONE specific field in the form when the user wants to correct a mistake."""
    return {field_name: new_value}

@tool
def submit_interaction(interaction_data: Dict[str, Any]):
    """Call this to save the finalized interaction data into the database."""
    db = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name == interaction_data.get("hcp_name")).first()
        if not hcp:
            return f"Error: HCP '{interaction_data.get('hcp_name')}' not found. Please select a valid HCP."
        
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
        return "SUCCESS: Interaction has been saved to the database."
    except Exception as e:
        db.rollback()
        return f"DATABASE ERROR: {str(e)}"
    finally:
        db.close()

# --- Agent Logic ---

tools = [get_hcp_list, get_product_list, log_interaction, edit_interaction, submit_interaction]
tool_node = ToolNode(tools)

model = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    openai_api_key=settings.OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
).bind_tools(tools)

def call_model(state: AgentState):
    # Construct dynamic system prompt with current state
    formatted_prompt = SYSTEM_PROMPT.format(
        form_state=str(state['form_data']),
        hcp_list=str(state['available_hcps']),
        product_list=str(state['available_products'])
    )
    
    # We create a clean list of messages for this specific call
    # System Prompt + History
    messages = [SystemMessage(content=formatted_prompt)] + state['messages']
        
    response = model.invoke(messages)
    return {"messages": [response]}

# --- Graph Construction ---

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

app_agent = workflow.compile()
