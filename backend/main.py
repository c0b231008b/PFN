from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS設定（Reactとローカル開発するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProofreadRequest(BaseModel):
    text: str


@app.post("/proofread")
async def proofread(request: ProofreadRequest):
    corrected = f"校正済みのテキストです: {request.text}"
    return {"corrected_text": corrected}
