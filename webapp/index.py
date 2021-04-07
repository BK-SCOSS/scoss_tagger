from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import json

from api.models import get_code, save_code

class Code(BaseModel):
    id: str
    label: str

app = FastAPI()

app.mount(
    "/templates",
    StaticFiles(directory="templates"),
    name="templates",
)

templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def root(request: Request):
    response = RedirectResponse(url='/templates/index.html')
    return response

@app.get("/api/get_code")
def get_code_from_db():
    return json.dumps(get_code())

@app.post("/api/save_label")
def save_label(code: Code):
    return json.dumps(save_code(code.id, code.label))
