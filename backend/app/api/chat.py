from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.agent import app_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    text: str
    role: str # user or assistant

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    form_data: Dict[str, Any] = {}

class ChatResponse(BaseModel):
    response: str
    form_data: Dict[str, Any]
    history: List[ChatMessage]

def convert_to_langchain(history: List[ChatMessage]) -> List[BaseMessage]:
    messages = []
    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.text))
        else:
            messages.append(AIMessage(content=msg.text))
    return messages

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    # 1. Prepare initial state
    langchain_history = convert_to_langchain(request.history)
    langchain_history.append(HumanMessage(content=request.message))
    
    initial_state = {
        "messages": langchain_history,
        "form_data": request.form_data,
        "available_hcps": [], # Can be populated if needed
        "available_products": []
    }
    
    # 2. Run the agent
    result = app_agent.invoke(initial_state)
    
    # 3. Extract tool outputs to update form_data
    # We look through the messages added by the 'tools' node
    updated_form_data = request.form_data.copy()
    
    # In a real scenario, we would parse tool outputs. 
    # For now, let's assume the agent suggests updates in its final message 
    # or we extract them from tool call results in the graph.
    
    # Simplification: If a tool was called, merge its result into form_data
    for msg in result['messages']:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            # This is complex to extract perfectly without more graph logic, 
            # but we can look at the messages following tool calls.
            pass

    # Better approach for this demo: The agent's tools return dicts, 
    # and we can find those in the message history or use a specific node.
    # For Step 3, we'll return the AI's response and the updated state.
    
    # Extract final AI response
    final_response = result['messages'][-1].content
    
    # Extract updated form data (logic to be refined as we see tool outputs)
    # We will refine this in the integration step.
    
    # Convert history back for frontend
    new_history = request.history + [ChatMessage(text=request.message, role="user")]
    new_history.append(ChatMessage(text=final_response, role="assistant"))

    return ChatResponse(
        response=final_response,
        form_data=updated_form_data, # This will be fully dynamic in Step 6
        history=new_history
    )
