import time
from tqdm import tqdm


# Function to calculate total tokens in a batch
def calculate_tokens(batch):
    return sum(len(doc.page_content.split()) for doc in batch)


# Process chunks with delay
def process_with_delay(
    all_splits, vector_store, max_calls=40, max_tokens=100000, delay=60
):
    print(f"Processing {len(all_splits)} documents in chunks...")
    batch = []
    current_tokens = 0

    # Initialize tqdm progress bar
    with tqdm(total=len(all_splits), desc="Processing Documents") as pbar:
        for doc in all_splits:
            doc_tokens = len(doc.page_content.split())  # Count tokens in the document

            # Add to batch if within limits
            if len(batch) < max_calls and (current_tokens + doc_tokens) <= max_tokens:
                batch.append(doc)
                current_tokens += doc_tokens
            else:
                # Process the batch
                vector_store.add_documents(documents=batch)
                print(
                    f"Processed batch with {len(batch)} documents and {current_tokens} tokens."
                )

                # Update the progress bar
                pbar.update(len(batch))

                # Reset for the next batch
                batch = [doc]
                current_tokens = doc_tokens
                time.sleep(delay)  # Delay before next batch

        # Process remaining documents
        if batch:
            vector_store.add_documents(documents=batch)
            print(
                f"Processed final batch with {len(batch)} documents and {current_tokens} tokens."
            )
            pbar.update(len(batch))
