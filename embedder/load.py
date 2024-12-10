# Directory where your text files are stored
import os
from langchain_core.documents import Document


directory = "./data"


# Function to load text files from a directory (and subdirectories)
def load_text_files_from_dir():
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):  # Adjust file extension filter if needed
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append(
                        Document(page_content=content, metadata={"source": file_path})
                    )
    return documents


if __name__ == "__main__":
    documents = load_text_files_from_dir()
    print(len(documents))
