from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.agent import app_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from app.core.database import SessionLocal
from app.models.models import HCP, Product

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    text: str
    role: str

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

@router.post("/")
async def chat_with_agent(request: ChatRequest):
    # 1. Fetch Latest Data from DB
    db = SessionLocal()
    try:
        hcps = db.query(HCP).all()
        products = db.query(Product).all()
        hcp_list = [{"name": h.name, "specialty": h.specialty} for h in hcps]
        product_list = [{"name": p.name} for p in products]
    finally:
        db.close()

    # 2. Prepare initial state
    langchain_history = convert_to_langchain(request.history)
    
    initial_state = {
        "messages": langchain_history + [HumanMessage(content=request.message)],
        "form_data": request.form_data,
        "available_hcps": hcp_list,
        "available_products": product_list
    }
    
    # 3. Run the agent
    result = app_agent.invoke(initial_state)
    
    # 4. Extract tool outputs to update form_data
    updated_form_data = request.form_data.copy()
    
    for msg in result['messages']:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call['name'] in ['log_interaction', 'edit_interaction']:
                    args = tool_call['args']
                    if tool_call['name'] == 'log_interaction':
                        for key, value in args.items():
                            if value is not None:
                                clean_key = key.replace('_str', '')
                                updated_form_data[clean_key] = value
                    elif tool_call['name'] == 'edit_interaction':
                        updated_form_data[args['field_name']] = args['new_value']

    final_response = result['messages'][-1].content
    
    new_history = request.history + [ChatMessage(text=request.message, role="user")]
    new_history.append(ChatMessage(text=final_response, role="assistant"))

    return ChatResponse(
        response=final_response,
        form_data=updated_form_data,
        history=new_history
    )
