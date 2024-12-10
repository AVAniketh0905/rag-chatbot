from dotenv import load_dotenv
import faiss

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_cohere import CohereEmbeddings

from load import load_text_files_from_dir
from store import process_with_delay

load_dotenv()

docs = load_text_files_from_dir()

embeddings = CohereEmbeddings(model="embed-english-v3.0")
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
# _ = vector_store.add_documents(documents=all_splits)

process_with_delay(all_splits, vector_store, max_calls=40, max_tokens=100000, delay=30)

print("Finished processing all documents.")

vector_store.save_local("./faiss_index")
