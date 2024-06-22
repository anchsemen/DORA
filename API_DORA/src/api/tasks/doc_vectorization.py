import time
import math
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

load_dotenv()
OPENAI_TOKEN = 'YOUR_TOKEN'


def check_embedding_class(embedding):
    if embedding == 'OpenAIEmbeddings':
        return OpenAIEmbeddings(openai_api_key=OPENAI_TOKEN)
    else:
        pass


def get_vector_db(filepath: str, embeddings_model: str, format: str, destination_filename: str,
                  chunk_size=1500) -> None:
    function_start = time.time()

    if format == 'markdown':
        loader = UnstructuredMarkdownLoader(filepath)
        data = loader.load()
        total_length = len(data[0].page_content)
        chunk_overlap = math.ceil(total_length / chunk_size)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_splits = text_splitter.split_documents(data)
    elif format == 'pdf':
        loader = PyPDFLoader(filepath)
        all_splits = loader.load_and_split()
    elif format == 'docx':
        loader = Docx2txtLoader(filepath)
        data = loader.load()
        total_length = len(data[0].page_content)
        chunk_overlap = math.ceil(total_length / chunk_size)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_splits = text_splitter.split_documents(data)

    vectorization_start = time.time()
    Chroma.from_documents(documents=all_splits, embedding=embeddings_model, persist_directory=destination_filename)
    vectorization_end = time.time() - vectorization_start
    function_end = time.time() - function_start
    print(f"Время выполнения векторизации файла: {vectorization_end}")
    print(f"Время выполнения функции: {function_end}")


# # Пример использования функции
# filepath = 'C:/Users/anchs/api_digitaldoubles — копия/СЕКСТИНГ__ЗАКОНЧИЛА_ТРЕНИРОВКУ__2.pdf'  # Укажите путь к вашему файлу
# embeddings_model = check_embedding_class('OpenAIEmbeddings')
# format = 'pdf'  # Укажите формат файла: 'markdown', 'pdf', 'docx'
# destination_filename = 'C:/Users/anchs/api_digitaldoubles — копия/temp_chroma'
#
# get_vector_db(filepath, embeddings_model, format, destination_filename)
