from dotenv import load_dotenv
from typing_extensions import List, TypedDict

from langgraph.graph import START, StateGraph
from langchain_core.prompts import PromptTemplate

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from langchain_cohere import CohereEmbeddings, ChatCohere

load_dotenv()


prompt_template = """Human: You are a helpful assistant that answers questions directly and only using the information provided in the context below.
    Guidance for answers:
        - Always use English as the language in your responses.
        - In your answers, always use a professional tone.
        - Begin your answers with "Based on the context provided: "
        - Simply answer the question clearly and with lots of detail using only the relevant details from the information below. If the context does not contain the answer, say "Sorry, I didn't understand that. Could you rephrase your question?"
        - Use bullet-points and provide as much detail as possible in your answer.
        - Always provide a summary at the end of your answer.
    Now read this context below and answer the question at the bottom.
    Context: {context}
    Question: {question}
    Assistant:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

embeddings = CohereEmbeddings(model="embed-english-v3.0")

# load local index
index_dir = "./faiss_index"
vector_store = FAISS.load_local(
    index_dir, embeddings=embeddings, allow_dangerous_deserialization=True
)

llm = ChatCohere(model="command-r-plus")


# Define state for the application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    # Perform similarity search to retrieve context
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    # Combine document content into a string to pass to the LLM
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


def run(query):
    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    return graph.invoke(query)
