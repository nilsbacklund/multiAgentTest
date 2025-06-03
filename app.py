import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from attacker_agent import AttackerAgent
from honeypot_agent import HoneypotAgent

app = FastAPI()
templates = Jinja2Templates(directory="templates")

attacker = AttackerAgent()
honeypot = HoneypotAgent()
logs: list[dict] = []

def label_mitre_phase(phase: str) -> str:
    return phase

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/simulate")
async def simulate() -> JSONResponse:
    phase, command = attacker.generate_command()
    response = honeypot.generate_response(command)
    timestamp = time.time()
    input_tokens = len(attacker.tokenizer.encode(command))
    output_tokens = len(honeypot.tokenizer.encode(response))
    entry = {
        "timestamp": timestamp,
        "phase": label_mitre_phase(phase),
        "command": command,
        "response": response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "attacker_model": attacker.tokenizer.name_or_path,
        "honeypot_model": honeypot.tokenizer.name_or_path,
    }
    logs.append(entry)
    return JSONResponse(entry)

@app.get("/logs")
async def get_logs() -> list[dict]:
    return logs