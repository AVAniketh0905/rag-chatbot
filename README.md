# RAG Chatbot

## Custom LLM

### AWS bedrock models

- can use the bedrock models

### Custom LLM Endpoint

- `docker build -t rag-chat-test .`
- `docker run rag-chat-test`

## PDF Extractor

### Next Steps

- extract data into text files
- extract based on topics in index
- extract based on page numbers
- create sep folder for each book
- create seperate text files for each topic

### Notes

- first 3 pdfs are from the same book
- last 2 have no index page

## Deployment

`aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {username}.dkr.ecr.{region}.amazonaws.com`

`aws ecr create-repository --repository-name rag-chat-cohere --region {region}`

`docker tag rag-chat-test:latest {username}.dkr.ecr.{region}.amazonaws.com/rag-chat-cohere`

`docker push {username}.dkr.ecr.{region}.amazonaws.com/rag-chat-cohere`
