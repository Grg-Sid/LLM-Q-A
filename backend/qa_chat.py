import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

from constants import CHROMA_SETTINGS


class LLMProcessor:
    def __init__(self):
        self.checkpoint = "LaMini-T5-738M"
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.base_model = AutoModelForSeq2SeqLM.from_pretrained(
            self.checkpoint,
            device_map="auto",
            torch_dtype=torch.float32,
        )

    def llm_pipeline(self):
        pipe = pipeline(
            "text2text-generation",
            model=self.base_model,
            tokenizer=self.tokenizer,
            max_length=256,
            do_sample=True,
            temperature=0.3,
            top_p=0.95,
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)
        return local_llm

    def qa_llm(self):
        llm = self.llm_pipeline()
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(
            persist_directory="db",
            embedding_function=embeddings,
            client_settings=CHROMA_SETTINGS,
        )
        retriever = db.as_retriever()
        qa = RetrievalQA.from_chain_type(
            retriever=retriever,
            llm=llm,
            chain_type="stuff",
            return_source_documents=True,
        )
        return qa

    def process_answer(self, instruction):
        response = ""
        instruction = instruction.strip()
        qa = self.qa_llm()
        generated_text = qa(instruction)
        answer = generated_text["result"]
        return answer, generated_text

    def main(self):
        instruction = "What is the title and what is the name of all the characters?"
        answer, generated_text = self.process_answer(instruction)


if __name__ == "__main__":
    processor = LLMProcessor()
    processor.main()
