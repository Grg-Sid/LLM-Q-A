from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

from db_manager import DBManager
from qa_chat import LLMProcessor
from ingest import ingest

load_dotenv()


class Response(BaseModel):
    result: str | None


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

allowed_file_types = [
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/pdf",
    "text/plain",
]

DATABASE_FILE = "db/data.sqlite"
db_manager = DBManager(DATABASE_FILE)
llm_processor = LLMProcessor()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type not in allowed_file_types:
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})

    db_manager.insert_file(file.filename, await file.read(), file.content_type)
    if ingest(file.filename):
        print("File uploaded")
        return JSONResponse(status_code=200, content={"message": "File uploaded"})
    else:
        return JSONResponse(status_code=500, content={"error": "An error occurred"})


@app.post("/predict", response_model=Response)
def predict(instruction: str) -> Any:
    answer, generated_text = llm_processor.process_answer(instruction)
    return JSONResponse(status_code=200, content={"result": answer})
