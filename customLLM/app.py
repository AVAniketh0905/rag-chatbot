from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, AutoModel

# Load LLaMA 2-Chat for text generation
model_name = "distilbert/distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
text_model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="auto", torch_dtype="float16"
)

# Load Embedding Model (use a separate embedding model, e.g., SentenceTransformers)
embedding_model_name = (
    "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight embedding model
)
embedding_model = AutoModel.from_pretrained(embedding_model_name)
embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)

# Initialize FastAPI app
app = FastAPI()


# Define request models
class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 200
    temperature: float = 0.7


class EmbedRequest(BaseModel):
    text: str


# Define endpoints
@app.post("/generate/")
def generate_text(request: GenerateRequest):
    """Generate text from the prompt."""
    try:
        chat_pipeline = pipeline(
            "text-generation", model=text_model, tokenizer=tokenizer, max_length=1024
        )
        output = chat_pipeline(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
        )
        return {"response": output[0]["generated_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embed/")
def embed_text(request: EmbedRequest):
    """Generate embeddings for the given text."""
    try:
        inputs = embedding_tokenizer(request.text, return_tensors="pt", truncation=True)
        embeddings = (
            embedding_model(**inputs).last_hidden_state.mean(dim=1).squeeze().tolist()
        )
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
