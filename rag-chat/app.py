from fastapi import FastAPI
from pydantic import BaseModel
from rag import run

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


# Define the API endpoint for querying
@app.post("/query/")
async def query(query: QueryRequest):
    try:
        response = run(query)

        # Return the answer
        return {"answer": response["answer"]}
    except Exception as e:
        return {"error": str(e)}
