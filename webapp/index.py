from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import json

from api.models import get_code, run_code, compile_code, save_code_mongodb, save_student_info

class Code(BaseModel):
    id: str
    label: str

class StudentCode(BaseModel):
    id: str
    label: str
    student_id: str
    hints: list

class Student(BaseModel):
    student_id: str
    student_name: str
    class_id: str

app = FastAPI()

app.mount(
    "/templates",
    StaticFiles(directory="templates"),
    name="templates",
)

templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def root(request: Request):
    response = RedirectResponse(url='/templates/home/index.html')
    return response

@app.get("/api/get_code")
def get_code_from_db():
    return json.dumps(get_code())

@app.post("/api/code/{action}")
def save_label(code: StudentCode, action: str):
    submit = False
    if action == 'submit':
        submit = True
    return json.dumps(run_code(code.id, code.label, code.student_id, code.hints, submit))

@app.post("/api/compile")
def save_label(code: Code):
    return json.dumps(compile_code(code.id, code.label))

@app.post("/api/save_code_mongodb")
def save_label(codes: list):
    return save_code_mongodb(codes)


@app.post("/api/save_student_info")
def save_label(st: Student):
    return save_student_info(st.student_id.strip(), st.student_name.strip(), st.class_id.strip())
