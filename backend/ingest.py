from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from db_manager import DBManager
from constants import CHROMA_SETTINGS
from utils import (
    get_text_from_docx,
    get_text_from_txt,
    get_text_from_pdf,
)

# CONSTANTS
PERSIST_DIRECTORY = "db"
DATABASE_FILE = "db/data.sqlite"
FILE_TYPES = ["pdf", "docx", "txt"]

# Initialize the DBManager
db_manager = DBManager(DATABASE_FILE)


def extract_text(file_content: bytes, file_type: str) -> str:
    if file_type == "pdf":
        return get_text_from_pdf(file_content)
    elif file_type == "docx":
        return get_text_from_docx(file_content)
    elif file_type == "txt":
        return get_text_from_txt(file_content)
    else:
        return ""


def ingest(file_name: str) -> bool:
    try:
        file = db_manager.get_file(file_name)
        file_content = file[2]
        file_type = file_name.split(".")[-1]
        file_text = extract_text(file_content, file_type)
        if file_type not in FILE_TYPES:
            raise Exception("Invalid file type")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
        text = splitter.split_text(file_text)
        document = splitter.create_documents(text)
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma.from_documents(
            document,
            embeddings,
            persist_directory=PERSIST_DIRECTORY,
            client_settings=CHROMA_SETTINGS,
        )
        db.persist()
        db = None
        return True
    except Exception as e:
        print({"error": str(e)})
        return False
