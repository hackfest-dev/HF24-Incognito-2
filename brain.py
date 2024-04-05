#brain of the virtual assistant 
from typing import List, Tuple
import re
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
import faiss


def parse_text(text: str, filename: str) -> List[str]:
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return [text]
