from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, engine
from agent import ask_agent

# Δημιουργία των πινάκων στη βάση κατά την εκκίνηση του API
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Action-Oriented Banking Agent API",
    description="API για τον AI Υπάλληλο Τράπεζας με δυνατότητες Function Calling",
    version="1.0.0"
)

# Pydantic Model για την επαλήθευση του εισερχόμενου JSON αιτήματος
class ChatRequest(BaseModel):
    user_prompt: str
    user_name: str = "Nikos"

# Pydantic Model για τη δομή της απάντησης
class ChatResponse(BaseModel):
    response: str
    user_name: str

@app.get("/")
def read_root():
    return {"message": "Ο Action-Oriented Banking Agent είναι online!"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """Endpoint για την αποστολή μηνυμάτων στον AI Agent."""
    if not request.user_prompt.strip():
        raise HTTPException(status_code=400, detail="Το μήνυμα δεν μπορεί να είναι κενό.")
    
    agent_output = ask_agent(request.user_prompt, request.user_name)
    
    return ChatResponse(
        response=agent_output,
        user_name=request.user_name
    )